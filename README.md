## python语音识别项目
----------------------------------------------
`python3.5` `语音识别` `百度语音API`

[![Build Status](https://api.travis-ci.org/zthxxx/python-Speech_Recognition.png?branch=master)](https://travis-ci.org/zthxxx/python-Speech_Recognition)
[![Coverage Status](https://coveralls.io/repos/github/zthxxx/python-Speech_Recognition/badge.svg?branch=master)](https://coveralls.io/github/zthxxx/python-Speech_Recognition?branch=master)
[![Code Climate](https://codeclimate.com/github/zthxxx/python-Speech_Recognition/badges/gpa.svg)](https://codeclimate.com/github/zthxxx/python-Speech_Recognition)

### 项目简介

本项目使用 python3.5，包管理使用 pip3.5，用 pyaudio 录音， numpy 计算， scipy 滤波， pylab 绘制波形与频谱。


### 项目环境

推介在与项目根目录同级目录内通过 virtualenv 建立 python 虚拟环境：
```bash?linenums
virtualenv --no-site-packages venv
```
第一次会自动安装一些虚拟环境文件，安装完后再激活虚拟环境，  
Windows 环境下使用：
```bash
venv\Scripts\activate
```
Linux 环境下使用：
```bash
source venv/bin/activate
```

cd 回到项目根目录中，项目依赖都写在 requirements.txt 中，  

#### Windows

在我的 Win 10 环境中 **`numpy 1.11.1+mkl`** 和 **`scipy 0.18.1`** 两个包都不能通过 pip 安装成功，  
因此我去[加利福尼亚大学镜像源](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载了 
[numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/numpy-1.11.2rc1+mkl-cp35-cp35m-win_amd64.whl) 
[scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/dp2ng7en/scipy-0.18.1-cp35-cp35m-win_amd64.whl) 
这两个包的 win 下支持的 .whl 文件并先通过 pip 安装：
```bash
pip install numpy-1.11.1+mkl-cp35-cp35m-win_amd64.whl
pip install scipy-0.18.1-cp35-cp35m-win_amd64.whl
```
然后再用 pip 安装 requirements.txt 的依赖：
```bash
pip install -r requirements.txt
```
全部通过安装后才算是建立好项目环境了  

#### Ubuntu 14.04 trusty

由于项目使用 Travis-CI 的系统是 ubuntu 14.04 trusty，  
因此 ubuntu 下的安装依赖可以参考 `.travis.yml` 中使用 `travis_env_init.sh` 进行安装，  
在上面 virtualenv 环境中，项目根目录下，使用以下命令执行安装：  
```bash
sudo source travis_env_init.sh
```
或者
```bash
sudo ./travis_env_init.sh
```
预安装完成后，再 `pip install -r requirements.txt` 安装剩下的依赖。 
安装脚本本来是针对 Travis 的环境，并非写的兼容的，  
如有其他包安装失败，请手动排查。  


### 配置说明

本项目使用 [百度语音识别 API](http://yuyin.baidu.com/docs/asr/57)，  
所以请先去 [百度语音开放平台](http://yuyin.baidu.com/) 建立工程，申请 API key、 Secret key，  
具体申请过程可参见 [玩转百度语音识别，就是这么简单](http://www.cnblogs.com/bigdataZJ/p/SpeechRecognition.html) 这篇文章。  
`./BaiduSpeech` 目录下的 `BaiduOAuthSample.ini` 是配置示例文件，先复制 `BaiduOAuthSample.ini` 为 `BaiduOAuth.ini`，  
再按照文件示例中对应位置填写自己的 `api_key` `secret_key`，键值间等号左右各空一格，值项无需引号，  
若已有 token 可填写 `access_token` 项。


### 使用说明

根目录中的 `SpeechRecognise.py` 为语音识别启动文件
```bash
python3.5 SpeechRecognise.py
```
启动后对准话筒说话，控制台将输出识别结果。(距离话筒的远近与话筒灵敏度相关)


### 结构说明

根目录中的 `SpeechRecognise.py` 为语音识别启动文件，  
`WaveOperate` 包中封装了一些对声卡的常用操作，如：  
录音、播放、保存文件、读取文件、绘制声波、绘制频谱、声音滤波 等操作。  
`BaiduSpeech` 包中为对 Baidu API 调用的封装，其中 `BaiduOAuth.ini` 为百度 API key 配置文件。  
`UnitTest` 包中为各模块的单元测试文件，
在项目根目录下执行命令 `python3.5 -m nose -vs --with-coverage` 将自动执行单元测试并输出结果和覆盖率。


### 项目思路

本项目语音识别的思路是：  

1. 麦克风阵列录音产生音频流  
2. 语音增强  
    2.1 音频流实时带通滤波，除去低音和高音  
    2.2 通过过零率 ZSR 和短时能量 Ep 进行 VAD 语音端点检测  
    2.3 切分判断有人声说话的音频部分  
3. 去混响(回声)  
    3.1 双麦技术  
    3.2 NLMS 自适应滤波  
4. 背景噪音消除  
    4.1 双麦背景消除  
5. 波束形成  
    5.1 声源信号分离   
6. 语音提取  
    6.1 声纹识别  
7. 语音识别  
    7.1 百度语音 API  
    7.2 Google 语音 API  
    7.3 讯飞语音 API  
8. 语义分析  
    8.1 Hanlp 句法词法依存分析  
    8.2 Boson 句法词法依存分析  
9. 参数化指令  
    9.1 Cortana XML 指令解析  

**当然，以上并没有完全实现。。。**

实现的项目：  

- [x] pyaudio录音  
- [x] 音频流实时带通滤波  
- [x] 短时能量 Ep 判断  
- [x] 切分判断有人声说话的音频部分  
- [x] 语音识别-百度语音 API  
- [x] Hanlp 依存分析  
- [x] Boson 依存分析  








