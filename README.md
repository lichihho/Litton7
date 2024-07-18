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
python litton7.py IMAGE
```

`IMAGE` 是影像檔案來源，可為資料夾或影像路徑。 可以指定一到多個。 
若為資料夾，程式預設行為是將所有深度的子資料夾裡的影像檔案都收集起來分析。  
若要取消這項行為（僅分析第一層影像檔案），請加上 `--no-recursive` 選項。

預設情況下分析結果會被寫入到一個逗號分隔值檔案內（comma separated values，CSV），
命名為 `litton7_yyyymmdd-HHMMSS.csv`。  
（`yyymmdd-HHMMSS` 為開始分析當下的時間戳記——`年月日-時分秒`）

該檔案會在當前工作路徑底下，可直接使用 Microsoft Excel 開啟。

若希望將檔案存在指定的位置，請將路徑由 `--output` 選項設定，例如：
```console
python litton7.py --output prefered/path/to/result.csv IMAGE
```
但要注意若該路徑已存在檔案，程式會嘗試**覆寫**掉原本的內容。

分析結果內容範例如下：
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



