from setuptools import setup, find_packages
import sys, os

dylib_dir = 'SeetaFaceEngine/Release'
dylibs = [os.path.join(dylib_dir, x) for x in os.listdir(dylib_dir) if os.path.isfile(x)]


setup(
    name ='pyseeta',
        
    version = 0.2,
    
    description = 'A simple Python interface for the SeetaFaceEngine',
 
    author = 'Xiaokang Tu',
    
    license = 'MIT',
    
    classifiers = [

        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Embedded Systems',
        
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    
    keywords = 'pyseeta seetaface facedetection facealignment faceidentification',
    
    packages = find_packages(),

    install_requires = ['numpy'],

    include_package_data = True,

    data_files = [(dylib_dir, dylibs)]

)