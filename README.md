# Litton7：Litton視覺景觀分類深度學習模型

## 摘要
  視覺景觀是整體景觀評估中的一個部分，其著重以視覺特徵進行分類，一個良好的分類系統可以促進後續的規劃設計工作順利地進行，以及讓視覺景觀資源的管理更有效率。Burton Litton自1968年開始在美國林務局進行了一系列的研究，建立起視覺景觀評估的方法，其景觀分類的架構具有相當的代表性。本研究試圖以深度學習進行Litton景觀分類系統的人工智慧模型訓練，目的在降低景觀資源調查的人力需求，同時增加判斷標準的一致性。訓練方法上使用深度學習中的遷移學習進行模型訓練，結果顯示模型實際使用精確度達80%，是可實際運用的分類模型，未來可朝多類別模型的訓練改進，使其更符合人類對環境分類的習慣。

## 模型表現

![圖片 1](https://github.com/lichihho/Litton7/assets/35607785/1d89bcab-2aa1-4c6a-a719-ea361c09ff77)


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

## 引用
citation
文章連結


