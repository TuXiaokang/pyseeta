
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
    }
}

def get_sys_platform():
    sp = sys.platform
    if sp.startswith('win'):
        return 'win32'
    elif sp.startswith('linux'):
        return 'linux'
    elif sp.startswith('darwin'):
        return 'darwin'
    else:
        raise EnvironmentError('{} is not supproted'.format(sp))

def get_detector_library():
    dir = os.path.dirname(__file__)
    sp = get_sys_platform()
    path = os.path.join(dir, '../SeetaFaceEngine/Release', config[sp]['detector'])
    return path

def get_aligner_library():
    dir = os.path.dirname(__file__)
    sp = get_sys_platform()
    return os.path.join(dir, '../SeetaFaceEngine/Release', config[sp]['aligner'])

def get_identifier_library():
    dir = os.path.dirname(__file__)
    sp = get_sys_platform()
    return os.path.join(dir, '../SeetaFaceEngine/Release', config[sp]['identifier'])  
