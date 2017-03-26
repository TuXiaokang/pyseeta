""" This is license
"""

from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

def test():
    import cv2
    # load model
    detector = Detector('../SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    aligner = Aligner('../SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    identifier = Identifier('../SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    # load image
    im_color = cv2.imread('/Users/tuxiaokang/Downloads/2.png')
    im_gray = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    # detect face in image
    faces = detector.detect(im_gray)
    # extract feature of each face
    for face in faces:
        landmarks = aligner.align(im_gray, face)
        # extract feature in different way
        im_crop = identifier.crop_face(im_color, landmarks)
        # save cropped face
        # cv2.imwrite('image/crop_{}.png'.format(hash(time.time())), im_crop)
        featA = identifier.extract_feature(im_crop)
        featB = identifier.extract_feature_with_crop(im_color, landmarks)
        # calculate similarity of features
        sim = identifier.calc_similarity(featA, featB)
        print('similarity: ', sim)

    # release
    identifier.release()
    aligner.release()
    detector.release()

if __name__ == '__main__':
    test()
