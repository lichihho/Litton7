#library
from __future__ import print_function, division
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from PIL import *
import pandas as pd
import torch.nn.functional as F
import shutil
import csv
plt.ion()

#target path 
folderpath = r"D:\\iamge\\testing\\testing2\\"

#output path
csvpath = r"D:\\iamge\\testing\\testing_csv\\"

#model path
model_path = r"D:\model\Litton-7type-visual-landscape-model.pth"
labels = ['0.Panoramic-landscape', '1.Feature-landscape', '2.Detail-landscape', '3.Enclosed-landscape', '4.Focal-landscape', '5.Ephemeral-landscape', '6.Canopied-landscape']


labelsnum=[]
for i in range(len(labels)):
    labelsnum.append(str(i))
img_type = [".jpg",".bmp",".png"]

model = torch.load(model_path)
model.eval()
model.cuda()
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize])

def main(imgpath):
    imgname = []
    imglabel = []
    imglabelnum = []
    rate = []
    error = []
    bset_out = number = checknumber = i = 0
    check = num = point = 0

    print("total " + str(len(os.listdir(imgpath))) + " images" )
    imagepath_list = os.listdir(imgpath)
    imagepath_list.sort()
    for infile in imagepath_list :
        try:
            for i in range(len(labels)):
                if infile == labels[i]:
                    continue
                fpath = imgpath + labels[i]
                if not os.path.isdir(fpath):
                    os.mkdir(fpath) 
            for check in img_type:
                if infile.find(check) == -1:
                    continue
            name = imgpath + infile
            img_pil = Image.open(name).convert('RGB')
            img_tensor = preprocess(img_pil).cuda()
            img_tensor = img_tensor.unsqueeze_(0)
            fc_out = model(Variable(img_tensor))
            fc_out = F.softmax(fc_out, dim=1)
            fc_out.tolist()

        except:
            print("error: " + name)
            error.append(name)
            
        else:
            transfer_list=[]
            for out in fc_out:
                for x in range (len(labelsnum)):
                    transfer_list.append(fc_out[0][x].item())
            best_out = max(transfer_list) 
            i = transfer_list.index(best_out)        
            label = labels[i]
            labelnum = labelsnum[i]
            rate.append(best_out)
            imgname.append(infile)
            imglabel.append(label)
            imglabelnum.append(labelnum)
            newpath = imgpath + label + "\\" + infile
            shutil.move(name, newpath)      
    dict = {'imgname':imgname, 'predict_label':imglabel, 'predict_label_num':imglabelnum,'probability':rate}
    df = pd.DataFrame(dict) 
    df.to_csv( csv_path, encoding = "utf_8_sig", index = False)
    if error :
        dict = {'error_imgname':error}
        df = pd.DataFrame(dict) 
        df.to_csv(error_csv_path, encoding = "utf_8_sig", index = False)  
        print("error: " + error_csv_path + " has been created !")
        error = []

folderpath_list = os.listdir(folderpath)
folderpath_list.sort()
for f in folderpath_list:
    start = time.time()
    imgpath = folderpath + f + '\\'
    
    csv_path = csvpath + f + "-Litton-7type-visual-landscape-predict_result.csv"
    error_csv_path = csvpath + f + "-predict_error.csv"
    print(csv_path)
    main(imgpath)
    end = time.time()
    print("Costing " + str(end-start) + " sec") 
    print("---------------------------------------------------------------------")
print("done")
