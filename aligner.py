""" This is license
"""


from ctypes import *

from common import _Face, _LandMarks, _Image


align_lib = cdll.LoadLibrary('../SeetaFaceEngine/library/libseeta_fa_lib.dylib')
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
        ptr = align_lib.align(self.aligner, byref(image_data), byref(face_data))
        # read face
        landmarks = [(ptr.contents.x[i], ptr.contents.y[i]) for i in range(5)]
        # free landmarks
        align_lib.free_landmarks(ptr)

        return landmarks

    def release(self):
        align_lib.free_aligner(self.aligner)

if __name__ == '__main__':
    from detector import Detector
    import cv2
    # load model
    detector = Detector('../SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('../SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    # load image
    im_color = cv2.imread('/Users/tuxiaokang/Downloads/2.png')
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    # detect faces in image
    faces = detector.detect(im_gray)
    # detect landmarks for each face    
    for face in faces:
        landmarks = aligner.align(im_gray, face)
        # print content in face
        print('({},{},{},{})=>{}'.format(face.left,face.top,face.right,face.bottom,face.score))
        # draw landmarks
        for point in landmarks:
            cv2.circle(im_color, point, 1, (255,0,0), 3)
        # draw bounding box
        cv2.rectangle(im_color, (face.left,face.top),(face.right, face.bottom), (0,255,255),3)
    # show result
    cv2.imshow('test', im_color)
    cv2.waitKey(0)
    # release
    aligner.release()
    detector.release()