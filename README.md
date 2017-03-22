# pyseeta
python api for SeetaFaceEngine(https://github.com/seetaface/SeetaFaceEngine.git)
# installation
1. Download SeetaFaceEngine(https://github.com/TuXiaokang/SeetaFaceEngine.git)
2. Build the dynamic library.
>  ```bash
> cd SeetaFaceEngine/
> mkdir build; cd build
> cmake ..
> make  
> ```
3. Add the dynamic path to system environment variables.
> + on linux & macOS, the default is `SeetaFaceEngine/library`
> + on windows, the default is  `SeetaFaceEngine/library/release/`
4. Download pyseeta(https://github.com/TuXiaokang/pyseeta.git)
5. install pyseeta
> ```bash
> python setup.py build
> python setup.py install
> ```

