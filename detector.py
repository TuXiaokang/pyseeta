""" This is license
"""

from ctypes import *
from common import *
import numpy as np
import copy as cp

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

class Detector(object):
    """ Class for face detecor
    """
    def __init__(self, model_path):
        self.detector = detect_lib.get_face_detector(model_path)
        self.set_image_pyramid_scale_factor();
        self.set_min_face_size();
        self.set_score_thresh();
        self.set_window_step();

    def detect(self, image):
        if np.ndim(image) != 2:
            raise ValueError('The input not a gray scale image!')
        image_data = _Image()
        image_data.data = image.tobytes()
        image_data.height, image_data.width = np.shape(image)
        image_data.channels = 1
        root = detect_lib.detect(self.detector, byref(image_data))
        faces = []
        if root:
            while not root.contents.null:
                face = Face()
                face.x = root.contents.x
                face.y = root.contents.y
                face.w = root.contents.w
                face.h = root.contents.h
                face.score = root.contents.score
                faces.append(cp.deepcopy(face))
                root = root.contents.next
        image_data = None
        return faces
    
    def set_image_pyramid_scale_factor(self, scale_factor=0.8):
        detect_lib.set_image_pyramid_scale_factor(self.detector, scale_factor)
    
    def set_min_face_size(self, min_face_size=40):
        detect_lib.set_min_face_size(self.detector, min_face_size)
    
    def set_score_thresh(self, score_thresh=2.0):
        detect_lib.set_score_thresh(self.detector, score_thresh)
    
    def set_window_step(self, window_step=[4,4]):
        detect_lib.set_window_step(self.detector, window_step[0], window_step[1]);


if __name__ == '__main__':
    from PIL import Image, ImageDraw
    import cv2
    im_color = Image.open('/Users/tuxiaokang/Downloads/2.png')
    im_gray = im_color.convert('L')
    im_color = cv2.imread('/Users/tuxiaokang/Downloads/2.png')
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)

    detector = Detector(b'../SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
       
    faces = detector.detect(im_gray)
    #draw = ImageDraw.Draw(im_color)
    for face in faces:
        print(face.x, face.y, face.w, face.h, face.score)
        cv2.rectangle(im_color, (face.x,face.y),(face.w+face.x, face.y+face.h), (255,0,0),3)
        #draw.rectangle((face.x, face.y, face.x+face.w, face.y+face.h), fill=(255, 0, 0, 128))
    cv2.imshow('x', im_color)
    cv2.waitKey(0)
    #im_color.show()  

