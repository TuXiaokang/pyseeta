
import os
import sys

config = {
    'win32': {
        'detector': 'seeta_fd_lib.dll',
        'aligner': 'seeta_fa_lib.dll',
        'identifier': 'seeta_fi_lib.dll'
    },
    'darwin': {
        'detector': 'libseeta_fd_lib.dylib',
        'aligner': 'libseeta_fa_lib.dylib',
        'identifier': 'libseeta_fi_lib.dylib'
    },
    'linux': {
        'detector': 'libseeta_fd_lib.so',
        'aligner': 'libseeta_fa_lib.so',
        'identifier': 'libseeta_fi_lib.so'
    },
    # Ubuntu 16.04 x64 Python 2.7.12 (default, Nov 19 2016, 06:48:10) sys.platform return 'linux2'
    'linux2': {
        'detector': 'libseeta_fd_lib.so',
        'aligner': 'libseeta_fa_lib.so',
        'identifier': 'libseeta_fi_lib.so'
    }
}

def get_detector_library():
    dir = os.path.dirname(__file__)
    return os.path.join(dir, '../SeetaFaceEngine/Release', config[sys.platform]['detector'])

def get_aligner_library():
    dir = os.path.dirname(__file__)
    return os.path.join(dir, '../SeetaFaceEngine/Release', config[sys.platform]['aligner'])

def get_identifier_library():
    dir = os.path.dirname(__file__)
    return os.path.join(dir, '../SeetaFaceEngine/Release', config[sys.platform]['identifier'])  
