""" This is license
"""


from ctypes import *
from ctypes.util import find_library
from .common import _Face, _LandMarks, _Image
import sys

DYLIB_EXT = {
    'darwin': 'libseeta_fa_lib.dylib',
    'win32' : '/release/libseeta_fa_lib.dll',
    'linux' : 'libseeta_fa_lib.so'
    }

SEETA_LIB_PATH = '../SeetaFaceEngine/library'

if DYLIB_EXT.get(sys.platform) is None:
    raise EnvironmentError('System not support!')

lib_path = find_library('seeta_fa_lib')

if lib_path is not None:
    align_lib = cdll.LoadLibrary(lib_path)
else:
    align_lib = cdll.LoadLibrary('{}/{}'.format(SEETA_LIB_PATH, DYLIB_EXT[sys.platform]))

align_lib.get_face_aligner.restype = c_void_p
align_lib.get_face_aligner.argtypes = [c_char_p]
align_lib.align.restype = POINTER(_LandMarks)
align_lib.align.argtypes = [c_void_p, POINTER(_Image), POINTER(_Face)]
align_lib.free_aligner.restype = None
align_lib.free_aligner.argtypes = [c_void_p]

class Aligner(object):
    """ Class for Face Alignment
    """
    def __init__(self, model_path):
        """
        input\n
        @param model_path: the path of aligner model
        """
        byte_model_path = bytes(model_path, encoding='utf-8')
        self.aligner = align_lib.get_face_aligner(byte_model_path)
    
    def align(self, image, face):
        """
        input:\n 
        @param image: a gray scale image.\n
        @param face: a face object.\n
        output: a list of point(x,y)
        """
        if image.ndim != 2:
            raise ValueError('The input not a gray scale image!')
        #prepare image data
        image_data = _Image()
        image_data.height, image_data.width = image.shape
        image_data.channels = 1
        data = (c_ubyte * image.size)(*image.tobytes())
        image_data.data = cast(data, c_void_p)
        # prepare face data
        face_data = _Face()
        face_data.left   = face.left
        face_data.top    = face.top
        face_data.right  = face.right
        face_data.bottom = face.bottom
        face_data.score  = face.score
        # call align function
        marks_data = align_lib.align(self.aligner, byref(image_data), byref(face_data))
        # read face
        landmarks = [(marks_data.contents.x[i], marks_data.contents.y[i]) for i in range(5)]
        # free landmarks
        align_lib.free_landmarks(marks_data)

        return landmarks

    def release(self):
        """ 
        release aligner memory
        """
        align_lib.free_aligner(self.aligner)