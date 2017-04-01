# MIT License

# Copyright (c) 2017 Tuxedo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy as cp
import sys
from ctypes import *
from ctypes.util import find_library

from .common import Face, _Face, _Image

DYLIB_EXT = {
    'darwin': 'libseeta_fd_lib.dylib',
    'win32' : 'seeta_fd_lib.dll',
    'linux' : 'libseeta_fd_lib.so'
    }

SEETA_LIB_PATH = 'SeetaFaceEngine/library'


if DYLIB_EXT.get(sys.platform) is None:
    raise EnvironmentError('System not support!')

lib_path = find_library('seeta_fd_lib')

if lib_path is not None:
    detect_lib = cdll.LoadLibrary(lib_path)
else:
    detect_lib = cdll.LoadLibrary('{}/{}'.format(SEETA_LIB_PATH, DYLIB_EXT[sys.platform]))

detect_lib.detect.restype = POINTER(_Face)
detect_lib.detect.argtypes = [c_void_p, POINTER(_Image)]
detect_lib.get_face_detector.restype = c_void_p
detect_lib.get_face_detector.argtypes = [c_char_p]
detect_lib.set_image_pyramid_scale_factor.restype = None
detect_lib.set_image_pyramid_scale_factor.argtypes = [c_void_p, c_float]
detect_lib.set_min_face_size.restype = None
detect_lib.set_min_face_size.argtypes = [c_void_p, c_int]
detect_lib.set_score_thresh.restype = None
detect_lib.set_score_thresh.argtypes = [c_void_p, c_float]
detect_lib.set_window_step.restype = None
detect_lib.set_window_step.argtypes = [c_void_p, c_int, c_int]
detect_lib.free_face_list.argtypes = [POINTER(_Face)]
detect_lib.free_face_list.restype = None
detect_lib.free_detector.argtypes = [c_void_p]
detect_lib.free_detector.restype = None



class Detector(object):
    """ Class for face detecor
    """
    
    def __init__(self, model_path=None):
        """ 
        input: the path of detecor model file
        """
        if model_path is None:
            model_path = 'SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin'
        byte_model_path = bytes(model_path, encoding='utf-8')
        self.detector = detect_lib.get_face_detector(byte_model_path)
        self.set_image_pyramid_scale_factor()
        self.set_min_face_size()
        self.set_score_thresh()
        self.set_window_step() 

    def detect(self, image):
        """ 
        Args:
            image: a gray scale image which can be a PIL image or a opencv image.\n
        Returns:
            a list of Face object
        """
        if image.ndim != 2:
            raise ValueError('The input not a gray scale image!')
        # prepare image data
        image_data = _Image()
        image_data.height, image_data.width = image.shape
        image_data.channels  = 1
        image_data.data = image.ctypes.data
        # call detect function
        face_data = detect_lib.detect(self.detector, byref(image_data))
        # read faces
        faces = []
        now = face_data
        face = Face()
        while now:
            face.left = now.contents.left
            face.top = now.contents.top
            face.right = now.contents.right
            face.bottom = now.contents.bottom
            face.score = now.contents.score
            faces.append(cp.deepcopy(face))
            now = now.contents.next
        # free face data
        detect_lib.free_face_list(face_data)
        image_data = None
        faces.sort(key=lambda i: (i.bottom - i.top) * (i.right - i.left))
        return faces
    
    def set_image_pyramid_scale_factor(self, scale_factor=0.8):
        detect_lib.set_image_pyramid_scale_factor(self.detector, scale_factor)
    
    def set_min_face_size(self, min_face_size=40):
        detect_lib.set_min_face_size(self.detector, min_face_size)
    
    def set_score_thresh(self, score_thresh=2.0):
        detect_lib.set_score_thresh(self.detector, score_thresh)
    
    def set_window_step(self, window_step=[4,4]):
        detect_lib.set_window_step(self.detector, window_step[0], window_step[1])
    
    def release(self):
        """ 
        release detector memory
        """
        detect_lib.free_detector(self.detector)
