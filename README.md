# Litton7：Litton視覺景觀分類深度學習模型
何立智、李沁築、邱浩修(2024)。Litton7：Litton視覺景觀分類深度學習模型。戶外遊憩研究，37(2)。

## 摘要
  視覺景觀是整體景觀評估中的一個部分，其著重以視覺特徵進行分類，一個良好的分類系統可以促進後續的規劃設計工作順利地進行，以及讓視覺景觀資源的管理更有效率。Burton Litton自1968年開始在美國林務局進行了一系列的研究，建立起視覺景觀評估的方法，其景觀分類的架構具有相當的代表性。本研究試圖以深度學習進行Litton景觀分類系統的人工智慧模型訓練，目的在降低景觀資源調查的人力需求，同時增加判斷標準的一致性。訓練方法上使用深度學習中的遷移學習進行模型訓練，結果顯示模型實際使用精確度達80%，是可實際運用的分類模型，未來可朝多類別模型的訓練改進，使其更符合人類對環境分類的習慣。


## 安裝

1. 請先下載完整檔案內容，並放置於本地端資料夾中。
2. 安裝 Anaconda。
3. 進入資料夾目錄中，使用 Conda 套件管理器安裝

Windows 作業系統的使用者使用以下指令安裝：
```console
conda env create
```

MacOS 的使用者請使用 `environment-mac.yml` 建立虛擬環境：
```zsh
conda env create --file environment-mac.yml
```

若沒有 GPU 裝置，無論任何作業系統，都可用 `environment-cpu.yml` 安裝純 CPU 運算版本：
```console
conda env create --file environment-cpu.yml
```
CPU 版本的運算速度在處理大資料量時較 GPU 版本慢上許多。若須分析大量資料，建議使用 GPU 版。

預設的虛擬環境名稱為「Litton7」。

## 使用

本程式是一個命令列腳本，使用以下指令進行批次預測及分類。

首先，我們需要先進入虛擬環境：

```console
conda activate Litton7
```

接著執行腳本：

```console
python prediction_Image(Litton-7type-visual-landscape-model).py ROOTFOLDER
```

`ROOTFOLDER` 是影像檔案群的頂層資料夾。此資料夾底下只能放置要分析的一或多個子資料夾，不可包含檔案，而每個子資料夾包含影像檔案。例如以下檔案、資料夾結構的 `root` 資料夾：
```console
root
├── sub1
│   ├── 00001.jpg
│   ├── 00002.jpg
│   ├── 00003.jpg
│   ...
├── sub2
│   ├── 00004.jpg
│   ├── 00005.jpg
│   ├── 00006.jpg
│   ...
├── sub3
│   ├── 00007.jpg
│   ├── 00008.jpg
│   ├── 00009.jpg
│   ...
...
```

程式成功執行完成之後，原始的 `root` 資料夾內的所有影像會被移動至原所屬子資料夾下新建立的 Littion 分類子資料夾內，例如 `root/sbu1` 底下的資料會被異動為（`root/sub2`、`root/sub3` 等等所有子資料夾亦若是）：
```console
root
├── sub1
│   ├── 0.Panoramic-landscape
│   │   ├── 00013.jpg
│   │   ├── 00403.jpg
│   │   ...
│   ├── 1.Feature-landscape
│   │   ├── 00033.jpg
│   │   ├── 00059.jpg
│   │   ...
│   ├── 2.Detail-landscape
│   │   ├── 00031.jpg
│   │   ├── 00555.jpg
│   │   ...
│   ├── 3.Enclosed-landscape
│   │   ├── 00082.jpg
│   │   ├── 00101.jpg
│   │   ...
│   ├── 4.Focal-landscape
│   │   ├── 00002.jpg
│   │   ├── 00077.jpg
│   │   ...
│   ├── 5.Ephemeral-landscape
│   │   ├── 00003.jpg
│   │   ├── 00332.jpg
│   │   ...
│   └── 6.Canopied-landscape
│       ├── 00001.jpg
│       ├── 00006.jpg
│       ...
...
```
`root` 底下的每個子資料夾均獨立被分析與移動資料。

預設情況下，預測資料會被放在當前工作路徑底下的 `output` 資料夾內。
我們可以使用 `--output` 選項指定其他路徑。

輸出資料夾 `output` 底下的內容會是：
```console
OUTPUTFOLDER
├── sub1-Litton-7type-visual-landscape-predict_result.csv
├── sub2-Litton-7type-visual-landscape-predict_result.csv
├── sub3-Litton-7type-visual-landscape-predict_result.csv
...
```

每個檔案的內容架構均為以 `imgname`、`predict_label`、`predict_label_num`、`probability` 為欄位的表格檔案（`.csv`），例如：
| imgname | predict_label | predict_label_num | probability
|:-------:|---------------|-------------------|-------------
00000924.jpg | 1.Feature-landscape | 1 | 1.0
00001923.jpg | 1.Feature-landscape | 1 | 0.9999349117279053
00016154.jpg | 2.Detail-landscape | 2 | 0.654981791973114
...（以下略）... | | |



[trained weight]: https://drive.google.com/file/d/1177rxfD7Yx5F5ZzEqDGBeAIYHTLU3lj9/view?usp=drive_link


## 引用
citation：
何立智、李沁築、邱浩修(2024)。Litton7：Litton視覺景觀分類深度學習模型。戶外遊憩研究，37(2)。



