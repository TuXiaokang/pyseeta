# pyseeta: python api for [SeetaFaceEngine](https://github.com/seetaface/SeetaFaceEngine.git)

[![Build Status](https://travis-ci.org/TuXiaokang/pyseeta.svg?branch=master)](https://travis-ci.org/TuXiaokang/pyseeta)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/TuXiaokang/pyseeta/blob/master/LICENSE)

## for detection
<img src="images/chloecalmon_det.jpg" width = '70%'/>

## for alignment
<img src="images/chloecalmon_align.jpg" width = '70%'/>

## for identification
<div align='center'>
    <img src="images/single_id.jpg" width = "300"/>
    <img src="images/double_id.jpg" width = "400"/>
</div>

Installation
---

1. Download pyseeta(https://github.com/TuXiaokang/pyseeta.git)
2. `git submodule update --init --recursive`
3. Build `SeetaFaceEngine` dynamic library.

    on unix
    ```bash
    cd SeetaFaceEngine/
    mkdir Release; cd Release
    cmake ..
    make  
    ```
    on windows

    ```bash
    cd SeetaFaceEngine/
    mkdir Release; cd Release
    cmake -G "Visual Studio 14 2015 Win64" ..
    cmake --build . --config Release
    ```
4. the generated dynamic lib is in `SeetaFaceEngine/Release`

5. run test
    
    ```bash
	python test_opencv.py
    ```
    or
    ```bash
    python test_pillow.py
	```

Uninstallation
---
    
```bash
pip uninstall pyseeta
```

Update Log
---

* **v0.4.0**
  + pretrained model is separate from submodule (`SeetaFaceEngine`) now, which makes clone opreration easier.
  + pretrained model could be automatic downloaded.

* **v0.3.0**
  + support pillow image


