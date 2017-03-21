""" This is license
"""


from ctypes import *

from common import _Face, _LandMarks, _Image


align_lib = cdll.LoadLibrary('../SeetaFaceEngine/library/libseeta_fa_lib.dylib')
align_lib.get_face_aligner.restype = c_void_p
align_lib.get_face_aligner.argtypes = [c_char_p]
align_lib.align.restype = POINTER(_LandMarks)
align_lib.align.argtypes = [c_void_p, POINTER(_Image), POINTER(_Face)]


class Aligner(object):
    """ Class for Face Alignment
    """
    def __init__(self, model_path):
        byte_model_path = bytes(model_path, encoding='utf-8')
        self.aligner = align_lib.get_face_aligner(byte_model_path)
    
    def align(self, image, face):
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
        root = align_lib.align(self.aligner, byref(image_data), byref(face_data))
        # read face
        for i in range(5):
            face.landmarks[i] = (root.contents.x[i], root.contents.y[i]) 
        # free landmarks
        align_lib.free_landmarks(root)

        return face

    def close(self):
        align_lib.free_aligner(self.aligner)

if __name__ == '__main__':
    from detector import Detector
    import cv2
    
    im_color = cv2.imread('/Users/tuxiaokang/Downloads/2.png')
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)

    detector = Detector('../SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('../SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    
    faces = detector.detect(im_gray)
    
    for face in faces:
        aligner.align(im_gray, face)
        #print(face.left, face.top, face.right, face.bottom, face.score)
        #for point in face.landmarks:
        #    cv2.circle(im_color, point, 1, (0,255,0), 1)
        #cv2.rectangle(im_color, (face.left,face.top),(face.right, face.bottom), (255,0,0),3)
    #cv2.imshow('x', im_color)
    #cv2.waitKey(0)