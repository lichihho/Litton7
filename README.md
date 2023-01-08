## 安裝
### 安裝 PyTorch
請至 PyTorch 官方網站的 [Get Started](https://pytorch.org/get-started/locally/) 選取需要的版本，並依照給出的命令列安裝。  
例如以下設定：
<table>
  <tr>
    <td>PyTorch Build</td> 
    <td><i><b>Stable (1.12.0)</b></i></td> 
    <td>Preview (Nightly)</td> 
    <td>LTS (1.8.2)</td>
    <td />
    <td />
  </tr>
  <tr>
    <td>Your OS</td> 
    <td>Linux</td> 
    <td>Mac</td> 
    <td><i><b>Windows</b></i></td>
    <td />
    <td />
  </tr>
  <tr>
    <td>Package</td> 
    <td><i><b>Conda</b></i></td> 
    <td>Pip</td> 
    <td>LibTorch</td> 
    <td>Source</td>
    <td />
  </tr>
  <tr>
    <td>Language</td> 
    <td><i><b>Python</b></i></td> 
    <td>C++ / Java</td>
    <td />
    <td />
    <td />
  </tr>
  <tr>
    <td>Compute Platform</td> 
    <td>CUDA 10.2</td> 
    <td><i><b>CUDA 11.3</b></i></td> 
    <td>CUDA 11.6</td> 
    <td><del>ROCm 5.1.1</del></td> 
    <td>CPU</td>
  </tr>
</table>


```console
$ conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```

### 安裝其他套件
```console
$ pip install jupyter 
$ pip install numpy==1.19.3 
$ pip install pandas 
$ pip install pillow 
$ pip install matplotlib
```

### 程式功能介紹


