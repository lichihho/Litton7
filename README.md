## 安裝
### 安裝 PyTorch
請至 PyTorch 官方網站的 [Get Started](https://pytorch.org/get-started/locally/) 選取需要的版本，並依照給出的命令列安裝。  
建議安裝指令:
```console
$ conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

### 安裝所需套件
```console
$ pip install jupyter 
$ pip install numpy==1.19.3 
$ pip install pandas 
$ pip install pillow 
$ pip install matplotlib
```

### 程式使用
1. target path setting: 設定需檢測的圖片位置
2. output path setting: 設定輸出CSV結果位置
3. model path setting: 設定Litton七類景觀分類型位置

### 程式功能與結果
1.target path內，依照圖片被分類到的結果放入相對應的資料夾內。
2.獲得所有圖片分析後的CSV表格，表格內容包含類別與分類機率。
