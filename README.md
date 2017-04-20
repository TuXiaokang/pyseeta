# pyseeta
python api for SeetaFaceEngine(https://github.com/seetaface/SeetaFaceEngine.git)
# installation
1. Download pyseeta(https://github.com/TuXiaokang/pyseeta.git)
2. `git submodule update --init --recursive`
3. Build `SeetaFaceEngine` dynamic library.

    on unix
    ```bash
    cd SeetaFaceEngine/
    mkdir build; cd build
    cmake ..
    make  
    ```
    on windows

    ```bash
    cd SeetaFaceEngine/
    mkdir build; cd build
    cmake -G "Visual Studio 14 2015 Win64" ..
    cmake --build . --config Release
    ```
4.  Add the dynamic lib path to system environment variables.
    + on linux & macOS, the default is `SeetaFaceEngine/library`
    + on windows, the default is  `SeetaFaceEngine/library/Release`
5. run test
    ```bash
    python test.py
    ```
# tips
If you want to use function of faceidentification, you need decompress the `seeta_fr_v1.0.part.1.rar` which located in `SeetaFaceEngine/model`
