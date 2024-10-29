"""
景觀圖片分類工具 (Landscape Image Classifier)

這個工具可以自動分類景觀圖片為7種不同類型：
0. 全景景觀 (Panoramic-landscape)
1. 特徵景觀 (Feature-landscape)
2. 細節景觀 (Detail-landscape)
3. 封閉景觀 (Enclosed-landscape)
4. 焦點景觀 (Focal-landscape)
5. 短暫景觀 (Ephemeral-landscape)
6. 遮蔽景觀 (Canopied-landscape)

使用方式:
1. 基本使用（處理單一圖片）:
   python litton7_simple.py path/to/image.jpg

2. 處理多個圖片:
   python litton7_simple.py image1.jpg image2.jpg image3.jpg

3. 處理整個資料夾:
   python litton7_simple.py path/to/image/folder

4. 指定輸出CSV檔案:
   python litton7_simple.py input_folder -o results.csv

5. 使用自訂模型和指定GPU:
   python litton7_simple.py input_folder -m custom_model.pth -d cuda

6. 使用CPU運算:
   python litton7_simple.py input_folder -d cpu

參數說明:
- input: 輸入圖片或資料夾路徑（必要參數）
- -o, --output: 輸出CSV檔案路徑（預設: results.csv）
- -m, --model: 自訂模型檔案路徑（預設: 自動下載預訓練模型）
- -d, --device: 運算裝置（預設: auto，可選: cpu, cuda）

輸出CSV檔案格式:
- imgname: 圖片檔案路徑
- predict_label: 預測的景觀類型
- predict_label_num: 預測類型的編號(0-6)
- probability: 預測的信心度(0-1)

需求套件:
- torch
- torchvision
- Pillow
- gdown
"""

from pathlib import Path
import torch
from PIL import Image
from torchvision import transforms
import torch.nn.functional as F
import csv
import gdown

class LandscapeClassifier:
    """景觀圖片分類器"""
    
    LABELS = [
        "0.Panoramic-landscape", "1.Feature-landscape", "2.Detail-landscape",
        "3.Enclosed-landscape", "4.Focal-landscape", "5.Ephemeral-landscape",
        "6.Canopied-landscape"
    ]
    
    def __init__(self, model_path=None, device="auto"):
        # 設定運算裝置
        self.device = ("cuda:0" if torch.cuda.is_available() else "cpu") if device == "auto" else device
        
        # 載入模型
        if model_path is None:
            model_path = "Litton-7type-visual-landscape-model.pth"
            if not Path(model_path).exists():
                gdown.download(id="1177rxfD7Yx5F5ZzEqDGBeAIYHTLU3lj9", output=model_path)
        
        self.model = torch.load(model_path, map_location=self.device)
        if hasattr(self.model, 'module'):
            self.model = self.model.module
        self.model.eval()
        
        # 設定圖片預處理
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def predict(self, image_path):
        """預測單張圖片的類別"""
        try:
            # 載入並預處理圖片
            image = Image.open(image_path).convert("RGB")
            input_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
            
            # 進行預測
            with torch.no_grad():
                logits = self.model(input_tensor)
                probs = F.softmax(logits[:, :7], dim=1)
            
            # 取得最可能的類別
            best_idx = probs[0].argmax().item()
            return {
                "label": self.LABELS[best_idx],
                "label_num": best_idx,
                "probability": probs[0, best_idx].item()
            }
        except Exception as e:
            print(f"處理圖片 {image_path} 時發生錯誤: {str(e)}")
            return None

def process_images(input_paths, output_path="results.csv", model_path=None, device="auto"):
    """處理多張圖片並將結果寫入CSV"""
    
    # 初始化分類器
    classifier = LandscapeClassifier(model_path, device)
    
    # 收集所有圖片路徑
    image_paths = []
    for path in input_paths:
        path = Path(path)
        if path.is_file():
            image_paths.append(path)
        elif path.is_dir():
            image_paths.extend(path.glob("**/*.jpg"))
            image_paths.extend(path.glob("**/*.png"))
    
    # 寫入結果到CSV
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["imgname", "predict_label", "predict_label_num", "probability"])
        writer.writeheader()
        
        # 處理每張圖片
        total = len(image_paths)
        for i, img_path in enumerate(image_paths, 1):
            result = classifier.predict(img_path)
            if result:
                writer.writerow({
                    "imgname": str(img_path),
                    "predict_label": result["label"],
                    "predict_label_num": result["label_num"],
                    "probability": result["probability"]
                })
            print(f"處理進度: {i}/{total}", end='\r')
        print("\n完成!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="景觀圖片分類工具")
    parser.add_argument("input", nargs="+", help="輸入圖片或資料夾路徑")
    parser.add_argument("-o", "--output", default="results.csv", help="輸出CSV檔案路徑")
    parser.add_argument("-m", "--model", help="模型檔案路徑")
    parser.add_argument("-d", "--device", default="auto", help="運算裝置 (auto/cpu/cuda)")
    
    args = parser.parse_args()
    process_images(args.input, args.output, args.model, args.device) 