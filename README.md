# pyseeta
python api for SeetaFaceEngine(https://github.com/seetaface/SeetaFaceEngine.git)
## for detection
<img src="images/chloecalmon_det.jpg" width = '70%'/>

## for alignment
<img src="images/chloecalmon_align.jpg" width = '70%'/>

## for identification
<div align='center'>
    <img src="images/single_id.jpg" width = "300"/>
    <img src="images/double_id.jpg" width = "400"/>
</div>

# installation
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

    on ubuntu or unix
	```bash
	sudo python setup.py install
	python test.py
	```
    on windows
	```bash
	python setup.py install
	python test.py
	```
# tips
If you want to use function of faceidentification, you need decompress the `seeta_fr_v1.0.part.1.rar` which located in `SeetaFaceEngine/model`
