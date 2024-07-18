from datetime import datetime
from pathlib import Path

import argparse
import sys


##########################################################################
# Parse Arguments
##########################################################################
class PrintHelpBeforeLeaveArgumentParser(argparse.ArgumentParser):
    "An argument parser with helpful error message."

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
            print("-" * 75)
        if status:
            self.print_help()
        sys.exit(status)

    def error(self, message):
        args = {"prog": self.prog, "message": message}
        self.exit(2, ("%(prog)s: error: %(message)s\n") % args)


parser = PrintHelpBeforeLeaveArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify images and save the results to a CSV file.",
)
parser.add_argument("target", type=Path, nargs="+", help="Path(s) to an image or a directory contains image(s).")
parser.add_argument("-m", "--model", type=Path, help="Specify the model path explicitly")
parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default=Path(datetime.now().strftime("litton7_%Y%m%d-%H%M%S.csv")),
    help="Path for the output CSV (default: ./litton7_yyyymmdd-HHMMSS.csv)",
)
parser.add_argument(
    "-b", "--batch-size", type=int, default=8,
    help="inference number of images per iteration (default: 8)"
)
parser.add_argument("--no-recursive", action="store_true", help="Do not collect images under sub-directories")
parser.add_argument(
    "-d",
    "--device",
    help=(
        "Use CPU or which GPU. (default: auto) "
        "`auto` to automatically choose device, "
        "`cpu` for pure CPU, "
        "0, 1, 2, ... to specify which GPU device. "
    ),
    default="auto",
)
parser.add_argument(
    "--log",
    help="Path to store log messages. If given 'stderr', log to stderr."
)

args = parser.parse_args()

##########################################################################
# Loading Libraries & Transform Arguments
##########################################################################
print("Loading libraries...")


from PIL import Image
from torchvision import transforms

import csv
import logging
import os
import platform
import queue
import threading
import time
import traceback

import gdown
import torch
import torch.nn.functional as F


args.batch_size = 1 if args.batch_size < 1 else args.batch_size

if args.model is None:
    if not Path("Litton-7type-visual-landscape-model.pth").exists():
        gdown.download(
            id="1177rxfD7Yx5F5ZzEqDGBeAIYHTLU3lj9",
            output="Litton-7type-visual-landscape-model.pth",
        )
    args.model = Path("Litton-7type-visual-landscape-model.pth")
else:
    if not args.model.exists():
        print(
            f"the model you have specifyed, {args.model}, do not exists",
            file=sys.stderr,
        )
        sys.exit(1)
    if not args.model.is_file():
        print(
            f"the model you have specifyed, {args.model}, is not a file.",
            file=sys.stderr,
        )
        sys.exit(1)

if args.device.lower() == "auto":
    if platform.system() == "Darwin":
        args.device = "mps" if torch.backends.mps.is_available() else "cpu"
    else:
        args.device = "cuda:0" if torch.cuda.is_available() else "cpu"
elif args.device.lower() == "cpu":
    args.device = "cpu"
else:
    if not args.device.isdigit():
        print(
            "--device must be one of 'cpu', 'auto', or an integer number.",
            file=sys.stderr,
        )
        sys.exit(1)

    if platform.system() == "Darwin":
        print(
            "MacOS (MPS backend) do not support specify GPU by index", file=sys.stderr
        )
        sys.exit(1)

    args.device = f"cuda:{args.device}"

if args.log == "stderr":
    logging.basicConfig(encoding="utf_8_sig", level=logging.WARNING)
elif args.log:
    logging.basicConfig(filename=args.log, encoding="utf_8_sig", level=logging.WARNING)
else:
    logging.disable()

##########################################################################
# Collection & Validation Image files
##########################################################################
print("Collecting images...")

  
def is_image(path: Path) -> Path | None:
    try:
        with Image.open(path) as f:
            f.verify()
    except Exception as exc:
        logging.warning(f"skip entry '{path}' due to exception: {exc.__class__.__name__}")
        return None
    return path


def load_image_to_queue(paths: list[Path], out_queue: queue.Queue):
    "Thread worker function to simply loading image files into queue"
    for path in paths:
        out_queue.put((path, Image.open(path)))


image_files = []
for path in args.target:
    if path.is_file():
        if is_image(path):
            image_files.append(path)
    if path.is_dir():
        entries = path.iterdir() if args.no_recursive else path.glob("**/*")
        for path in entries:
            if not path.is_file():
                continue
            if is_image(path):
                image_files.append(path)
    else:
        logging.warning(f"skip collecting from '{path}' because this is not a file nor a directory")
        
if not image_files:
    print("No image founded, Abort.")
    exit()

print("Start a background thread to loading image...")
# every items in `image_queue` will be `tuple(image_path: Path, image: PIL.Image.Image)`
image_queue = queue.Queue(maxsize=args.batch_size * 3)
threading.Thread(target=load_image_to_queue, args=(image_files, image_queue)).start()

##########################################################################
# Loading Model & Initialize Output File
##########################################################################
print("Loading model...")
try:
    model: torch.nn.DataParallel = torch.load(args.model, map_location=torch.device(args.device))
    model: torch.nn.Module = model.module.to(args.device).eval()
except Exception as exc:
    msg = (
        f"Could not load model, `{args.model}`, "
        f"due to exception: {exc.__class__.__name__}. "
        f"For details, please check `.{os.sep}litton7-traceback.log`."
    )
    logging.critical(msg)
    if args.log != "stderr":
        print(msg, file=sys.stderr)
    with open("litton7-traceback.log", "w") as ftrace:
        traceback.print_exception(exc, file=ftrace)
    sys.exit(2)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
preprocess = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ]
)

try:
    outfile = args.output.open("w", encoding="utf-8-sig", newline="")
except Exception as exc:
    msg = (
        f"Could not create output file, `{args.output}`, "
        f"due to exception: {exc.__class__.__name__}. Abort."
    )
    logging.error(msg)
    if args.log != "stderr":
        print(msg, file=sys.stderr)
    sys.exit(3)

writer = csv.DictWriter(
    outfile,
    fieldnames=["imgname", "predict_label", "predict_label_num", "probability"],
)
writer.writeheader()

##########################################################################
# Classify & Write Results to Output File
##########################################################################
LABELS = [
    "0.Panoramic-landscape",
    "1.Feature-landscape",
    "2.Detail-landscape",
    "3.Enclosed-landscape",
    "4.Focal-landscape",
    "5.Ephemeral-landscape",
    "6.Canopied-landscape",
]

# show progress
start_time = time.time()
current_for_print = " " * (len(str(len(image_files))) - 1) + "0"
print(f" {current_for_print} / {len(image_files)} (  0.00%)", end="", flush=True)

current_done = 0
while current_done < len(image_files):
    image_paths = []
    features: list[torch.Tensor] = []
    if (len(image_files) - current_done) < args.batch_size:
        bsize = len(image_files) - current_done
    else:
        bsize = args.batch_size
    for _ in range(bsize):
        imgpath, imgobj = image_queue.get()
        image_paths.append(imgpath)
        features.append(preprocess(imgobj.convert("RGB")))
    feature = torch.stack(features)  # shape: (batch_size, 3, 224, 224)

    feature = feature.to(args.device)
    with torch.no_grad():
        logits = model(feature)
        probs = F.softmax(logits[:, :7], dim=1)  # shape: (batch_size, 7)

    probs = probs.to("cpu")
    for i in range(probs.shape[0]):
        i_best_match = probs[i].argmax().item()
        writer.writerow(
            {
                "imgname": image_paths[i],
                "predict_label": LABELS[i_best_match],
                "predict_label_num": i_best_match,
                "probability": probs[i, i_best_match].item(),
            }
        )

    current_done += bsize

    # show progress
    elapsed_seconds = time.time() - start_time
    ratio = current_done / len(image_files)
    secs_per_image = elapsed_seconds / current_done
    eta_total_secs = secs_per_image * (len(image_files) - current_done)
    eta_hours = int(eta_total_secs // (60 * 60))
    eta_mins = int(eta_total_secs % (60 * 60) // 60)
    eta_seconds = int(eta_total_secs % 60)
    current_for_print = (
        " " * (len(str(len(image_files))) - len(str(current_done))) + str(current_done)
    )
    if secs_per_image > 1:
        freq = secs_per_image
        freq_unit = "s/img"
    else:
        freq = 1 / secs_per_image
        freq_unit = "img/s"
    print(
        f"\r {current_for_print} / {len(image_files)} "
        f"({ratio * 100:6.2f}%) "
        f"| {freq:.2f} {freq_unit} ETA "
        f"{eta_hours}:{eta_mins:02}:{eta_seconds:02}",
        end="",
        flush=True,
    )

outfile.close()