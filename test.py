""" This is license
"""

from pyseeta import Detector
from pyseeta import Aligner
from pyseeta import Identifier

def test():
    import cv2, os
    # load model
    detector = Detector('SeetaFaceEngine/model/seeta_fd_frontal_v1.0.bin')
    #aligner = Aligner('SeetaFaceEngine/model/seeta_fa_v1.1.bin')
    #identifier = Identifier('SeetaFaceEngine/model/seeta_fr_v1.0.bin')
    video_dir = '/Users/tuxiaokang/Downloads/Casia/1'
    #video_path_list =[os.path.join(video_dir, x) for x in os.listdir(video_dir)]
    video_path_list = ['/Users/tuxiaokang/Downloads/Casia/train_release/19/HR_1.avi']
    for v in video_path_list:
        cap = cv2.VideoCapture(v)
        i = 0
        while True:
            ret, frame = cap.read()
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect(gray)
            if len(faces) == 0:
                i += 1
            # for face in faces:
            #     print(face.left, face.top, face.right, face.bottom)
            #     cv2.rectangle(frame, (face.left, face.top), (face.right, face.bottom), (0,255,0),3)
            # cv2.imshow('video', frame)
            # cv2.waitKey(3)
        print(i)
        cap.release()
    """
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
    """
    # release
    #identifier.release()
    #aligner.release()
    detector.release()

if __name__ == '__main__':
    test()
