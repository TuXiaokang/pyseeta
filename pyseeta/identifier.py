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
import os
import sys
from ctypes import *
from ctypes.util import find_library

import numpy as np

from .common import _Face, _Image, _LandMarks
from .config import get_identifier_library

lib_path = find_library('seeta_fi_lib')

if lib_path is None:
    lib_path = get_identifier_library()

identi_lib = cdll.LoadLibrary(lib_path)

c_float_p = POINTER(c_float)

identi_lib.get_face_identifier.restype = c_void_p
identi_lib.get_face_identifier.argtypes = [c_char_p]
identi_lib.extract_feature_with_crop.restype = c_float_p
identi_lib.extract_feature_with_crop.argtypes = [c_void_p, POINTER(_Image), POINTER(_LandMarks)]
identi_lib.crop_face.restype = POINTER(_Image)
identi_lib.crop_face.argtypes = [c_void_p, POINTER(_Image), POINTER(_LandMarks)]
identi_lib.extract_feature.restype = c_float_p
identi_lib.extract_feature.argtypes = [c_void_p, POINTER(_Image)]
identi_lib.calc_similarity.restype = c_float
identi_lib.calc_similarity.argtypes = [c_void_p, c_float_p, c_float_p]
identi_lib.free_feature.restype = None
identi_lib.free_feature.argtypes = [c_float_p]
identi_lib.free_image_data.restype = None
identi_lib.free_image_data.argtypes = [POINTER(_Image)]
identi_lib.free_identifier.restype = None
identi_lib.free_identifier.argtypes = [c_void_p]


class Identifier(object):
    """ Class for Face identification
    """
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = 'SeetaFaceEngine/model/seeta_fr_v1.0.bin'
        assert os.path.isfile(model_path) is True, 'No such file!'

        byte_model_path = model_path.encode('utf-8')
        self.identifier = identi_lib.get_face_identifier(byte_model_path)

    def crop_face(self, image, landmarks):
        """ Crop face image from original image
        Args:
            image: a color image
            landmarks: a list of point (x,y), length is five

        Returns:
            a numpy array image
        """
        # handle pillow image
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        # prepare image data
        image_data = _Image()
        image_data.height, image_data.width = image.shape[:2]
        image_data.channels = 1 if len(image.shape) == 2 else image.shape[2]
        image_data.data = image.ctypes.data
        # prepare landmarks
        marks_data = _LandMarks()
        for i in range(5):
            marks_data.x[i], marks_data.y[i] =  landmarks[i]
        # call crop face function
        crop_data = identi_lib.crop_face(self.identifier, byref(image_data), byref(marks_data))
        # read crop data
        contents = crop_data.contents
        crop_shape = (contents.height, contents.width, contents.channels)
        nb_pixels = np.product(crop_shape)
        byte_data = cast(contents.data, POINTER(c_ubyte))
        byte_data = (c_ubyte * nb_pixels)(*byte_data[:nb_pixels])
        image_crop = np.fromstring(byte_data, dtype=np.uint8).reshape(crop_shape)
        # free crop data
        identi_lib.free_image_data(crop_data)

        return image_crop

    def extract_feature(self, image):
        """ Extract feature of cropped face image
        Args:
            image: a color image

        Returns:
            a list of float, the length is 2048
        """
        # handle pillow image
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        # prepare image data
        image_data = _Image()
        image_data.height, image_data.width = image.shape[:2]
        image_data.channels = 1 if len(image.shape) == 2 else image.shape[2]
        image_data.data = image.ctypes.data
        # call extract_feature function
        root = identi_lib.extract_feature(self.identifier, byref(image_data))
        # read feature
        feat = root[:2048]
        # free feature
        identi_lib.free_feature(root)
        return feat

    def extract_feature_with_crop(self, image, landmarks):
        """ Extract feature of face
        Args:
            image: a color image
            landmarks: a list of point (x,y), length is five
        Returns:
            a list of float, the length is 2048
        """
        # handle pillow image
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        # prepare image data
        image_data = _Image()
        image_data.height, image_data.width = image.shape[:2]
        image_data.channels = 1 if len(image.shape) == 2 else image.shape[2]
        image_data.data = image.ctypes.data
        # prepare landmarks
        marks_data = _LandMarks()
        for i in range(5):
            marks_data.x[i], marks_data.y[i] =  landmarks[i]
        # call extract_feature_with_crop function
        root = identi_lib.extract_feature_with_crop(self.identifier, byref(image_data), byref(marks_data))
        # read feature
        feat = root[:2048]
        # free feature
        identi_lib.free_feature(root)
        return feat

    def calc_similarity(self, featA, featB):
        """ Calculate similarity of 2 feature
        Args:
            featA: a list of float, the length is 2048
            featB: a list of float, the length is 2048
        Returns:
            a list of float, the length is 2048
        """
        # prepare feature array
        feat_a = (c_float * 2048)(*featA)
        feat_b = (c_float * 2048)(*featB)
        # call calc_similarity function
        similarity = identi_lib.calc_similarity(self.identifier, feat_a, feat_b)
        return similarity

    def release(self):
        """
        release identifier memory
        """
        identi_lib.free_identifier(self.identifier)
