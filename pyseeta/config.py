
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

def get_library_raise(name):
    dir = os.path.dirname(__file__)
    platform = get_sys_platform()
    dlib = os.path.join(dir, '../SeetaFaceEngine/Release', config[platform][name])
    if os.path.exists(dlib) and os.path.isfile(dlib):
        return dlib
    dlib = os.path.join(dir, '../SeetaFaceEngine/library', config[platform][name])
    if os.path.exists(dlib) and os.path.isfile(dlib):
        return dlib
    dlib = os.path.join(dir, '../SeetaFaceEngine/library/Release', config[platform][name])
    if os.path.exists(dlib) and os.path.isfile(dlib):
        return dlib
    raise RuntimeError("SeetaFaceEngine %s dynamic library %s can't find"%(name,config[platform][name]))

def get_detector_library():
    return get_library_raise('detector')

def get_aligner_library():
    return get_library_raise('aligner')

def get_identifier_library():
    return get_library_raise('identifier')

