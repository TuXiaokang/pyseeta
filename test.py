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



from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

def test_detector():
    import cv2
    # load model
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    detector.set_min_face_size(30)

    image_color = cv2.imread('images/chloecalmon.png')
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

    faces = detector.detect(image_gray)

    for i, face in enumerate(faces):
        print('({0},{1},{2},{3}) score={4}'.format(face.left, face.top, face.right, face.bottom, face.score))
        cv2.rectangle(image_color, (face.left, face.top), (face.right, face.bottom), (0,255,0), thickness=2)
        cv2.putText(image_color, str(i), (face.left, face.bottom),cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), thickness=1)
    cv2.imshow('test', image_color)
    cv2.waitKey(0)
 
    detector.release()

def test_aligner():
    import cv2
    # load model
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    detector.set_min_face_size(30)
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    
    image_color = cv2.imread('images/chloecalmon.png')
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    
    faces = detector.detect(image_gray)

    for face in faces:
        landmarks = aligner.align(image_gray, face)
        for point in landmarks:
            cv2.circle(image_color, point, 1, (0,255,0), 2)
    
    cv2.imshow('test aligner', image_color)
    cv2.waitKey(0)
   
    aligner.release()
    detector.release()

def test_identifier():
    import cv2
    import numpy as np
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    
    # load image
    image_color_A = cv2.imread('images/single.jpg')
    image_gray_A = cv2.cvtColor(image_color_A, cv2.COLOR_BGR2GRAY)
    image_color_B = cv2.imread('images/double.jpg')
    image_gray_B = cv2.cvtColor(image_color_B, cv2.COLOR_BGR2GRAY)
    # detect face in image
    faces_A = detector.detect(image_gray_A)
    faces_B = detector.detect(image_gray_B)

    if len(faces_A) and len(faces_B):
        landmarks_A = aligner.align(image_gray_A, faces_A[0])
        featA = identifier.extract_feature_with_crop(image_color_A, landmarks_A)
        cv2.rectangle(image_color_A, (faces_A[0].left, faces_A[0].top), (faces_A[0].right, faces_A[0].bottom), (0,255,0), thickness=2)
        sim_list = []
        for face in faces_B:
            landmarks_B = aligner.align(image_gray_B, face)
            featB = identifier.extract_feature_with_crop(image_color_B, landmarks_B)
            sim = identifier.calc_similarity(featA, featB)
            sim_list.append(sim)
        print('sim: {}'.format(sim_list))
        index = np.argmax(sim_list)
        for i, face in enumerate(faces_B):
            color = (0,255,0) if i == index else (0,0,255)
            cv2.rectangle(image_color_B, (face.left, face.top), (face.right, face.bottom), color, thickness=2)
    cv2.imshow('single', image_color_A)
    cv2.imshow('double', image_color_B)
    cv2.waitKey(0)

    identifier.release()
    aligner.release()
    detector.release()

if __name__ == '__main__':
    test_identifier()
