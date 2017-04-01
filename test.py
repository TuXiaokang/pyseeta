""" This is license
"""

from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

def test_detector():
    import cv2
    # load model
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    image_color = cv2.imread('images/test.jpg')
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

    faces = detector.detect(image_gray)

    for face in faces:
        print(face.left, face.top, face.right, face.bottom)
        cv2.rectangle(image_color, (face.left, face.top), (face.right, face.bottom), (0,255,0), 3)
    cv2.imshow('test', image_color)
    cv2.waitKey(0)

    identifier.release()
    aligner.release()
    detector.release()

def test_aligner():
    import cv2
    # load model
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    image_color = cv2.imread('images/test.jpg')
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    
    faces = detector.detect(image_gray)

    for face in faces:
        landmarks = aligner.align(image_gray, faces[0])
        for point in landmarks:
            cv2.circle(image_color, point, 3, (0,255,0), 3)
    
    cv2.imshow('test aligner', image_color)
    cv2.waitKey(0)
    
    identifier.release()
    aligner.release()
    detector.release()

def test_identifier():
    import cv2
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    
    # load image
    image_color_A = cv2.imread('images/Aaron_Peirsol_0001.jpg')
    image_gray_A = cv2.cvtColor(image_color_A, cv2.COLOR_BGR2GRAY)
    image_color_B = cv2.imread('images/Aaron_Peirsol_0004.jpg')
    image_gray_B = cv2.cvtColor(image_color_B, cv2.COLOR_BGR2GRAY)
    # detect face in image
    faces_A = detector.detect(image_gray_A)
    faces_B = detector.detect(image_gray_B)
    if len(faces_A) and len(faces_B):
        landmarks_A = aligner.align(image_gray_A, faces_A[0])
        landmarks_B = aligner.align(image_gray_B, faces_B[0])
        featA = identifier.extract_feature_with_crop(image_color_A, landmarks_A)
        featB = identifier.extract_feature_with_crop(image_color_B, landmarks_B)
        sim = identifier.calc_similarity(featA, featB)
        print('Similarity:', sim)
    identifier.release()
    aligner.release()
    detector.release()

if __name__ == '__main__':
    test_aligner()
