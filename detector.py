""" This is license
"""

import copy as cp
from ctypes import *

import numpy as np

from common import Face, _Face, _Image

detect_lib = cdll.LoadLibrary('../SeetaFaceEngine/library/libseeta_fd_lib.dylib')
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
    
    def __init__(self, model_path):
        byte_model_path = bytes(model_path, encoding='utf-8')
        self.detector = detect_lib.get_face_detector(byte_model_path)
        self.set_image_pyramid_scale_factor()
        self.set_min_face_size()
        self.set_score_thresh()
        self.set_window_step() 

    def detect(self, image):
        if np.ndim(image) != 2:
            raise ValueError('The input not a gray scale image!')
        image_data = _Image()
        image_data.height, image_data.width = image.shape
        image_data.channels  = 1
        byte_data = (c_ubyte * image.size)(*image.tobytes())
        image_data.data = cast(byte_data, c_void_p)
        root = detect_lib.detect(self.detector, byref(image_data))
        faces = []
        now = root
        face = Face()
        while now:
            face.left = now.contents.left
            face.top = now.contents.top
            face.right = now.contents.right
            face.bottom = now.contents.bottom
            face.score = now.contents.score
            faces.append(cp.deepcopy(face))
            now = now.contents.next
        detect_lib.free_face_list(root)
        image_data = None
        return faces
    
    def set_image_pyramid_scale_factor(self, scale_factor=0.8):
        detect_lib.set_image_pyramid_scale_factor(self.detector, scale_factor)
    
    def set_min_face_size(self, min_face_size=40):
        detect_lib.set_min_face_size(self.detector, min_face_size)
    
    def set_score_thresh(self, score_thresh=2.0):
        detect_lib.set_score_thresh(self.detector, score_thresh)
    
    def set_window_step(self, window_step=[4,4]):
        detect_lib.set_window_step(self.detector, window_step[0], window_step[1])
    
    def close(self):
        detect_lib.free_detector(self.detector)


if __name__ == '__main__':
            
    def test():
        import cv2
        im_color = cv2.imread('/Users/tuxiaokang/Downloads/2.png')
        im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)

        detector = Detector('../SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
        faces = detector.detect(im_gray)

        for face in faces:
            print(face.left, face.top, face.right, face.bottom, face.score)
            cv2.rectangle(im_color, (face.left,face.top),(face.right, face.bottom), (255,0,0),3)
        cv2.imshow('x', im_color)
        cv2.waitKey(0)
    test()
