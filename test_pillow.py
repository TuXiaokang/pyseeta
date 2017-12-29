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

try:
    from PIL import Image, ImageDraw
    import numpy as np
except ImportError:
    raise ImportError('Pillow can not be found!')

def test_detector():
    print('test detector:')
    # load model
    detector = Detector()
    detector.set_min_face_size(30)

    image_color = Image.open('data/chloecalmon.png').convert('RGB')
    image_gray = image_color.convert('L')
    faces = detector.detect(image_gray)
    draw = ImageDraw.Draw(image_color)
    for i, face in enumerate(faces):
        print('({0},{1},{2},{3}) score={4}'.format(face.left, face.top, face.right, face.bottom, face.score))
        draw.rectangle([face.left, face.top, face.right, face.bottom])
    image_color.show()
    detector.release()

def test_aligner():
    print('test aligner:')
    # load model
    detector = Detector()
    detector.set_min_face_size(30)
    aligner = Aligner()

    image_color = Image.open('data/chloecalmon.png').convert('RGB')
    image_gray = image_color.convert('L')
    faces = detector.detect(image_gray)
    draw = ImageDraw.Draw(image_color)
    draw.ellipse ((0,0,40,80), fill=128)
    for face in faces:
        landmarks = aligner.align(image_gray, face)
        for point in landmarks:
            x1, y1 = point[0] - 2, point[1] - 2
            x2, y2 = point[0] + 2, point[1] + 2
            draw.ellipse((x1,y1,x2,y2), fill='red')
    image_color.show()

    aligner.release()
    detector.release()

def test_identifier():
    print('test identifier:')
    detector = Detector()
    aligner = Aligner()
    identifier = Identifier()

    # load image
    image_color_A = Image.open('data/single.jpg').convert('RGB')
    image_gray_A = image_color_A.convert('L')
    image_color_B = Image.open('data/double.jpg').convert('RGB')
    image_gray_B = image_color_B.convert('L')

    # detect face in image
    faces_A = detector.detect(image_gray_A)
    faces_B = detector.detect(image_gray_B)

    draw_A = ImageDraw.Draw(image_color_A)
    draw_B = ImageDraw.Draw(image_color_B)

    if len(faces_A) and len(faces_B):
        landmarks_A = aligner.align(image_gray_A, faces_A[0])
        featA = identifier.extract_feature_with_crop(image_color_A, landmarks_A)
        draw_A.rectangle([(faces_A[0].left, faces_A[0].top), (faces_A[0].right, faces_A[0].bottom)], outline='green')

        sim_list = []
        for face in faces_B:
            landmarks_B = aligner.align(image_gray_B, face)
            featB = identifier.extract_feature_with_crop(image_color_B, landmarks_B)
            sim = identifier.calc_similarity(featA, featB)
            sim_list.append(sim)
        print('sim: {}'.format(sim_list))
        index = np.argmax(sim_list)
        for i, face in enumerate(faces_B):
            color = 'green' if i == index else 'red'
            draw_B.rectangle([(face.left, face.top), (face.right, face.bottom)], outline=color)

    image_color_A.show()
    image_color_B.show()

    identifier.release()
    aligner.release()
    detector.release()

def test_cropface():
    detector = Detector()
    detector.set_min_face_size(30)
    aligner = Aligner()
    identifier = Identifier()

    image_color = Image.open('data/chloecalmon.png').convert('RGB')
    image_gray = image_color.convert('L')
    
    faces = detector.detect(image_gray)
    for face in faces:
        landmarks = aligner.align(image_gray, face)
        crop_face = identifier.crop_face(image_color, landmarks)
        Image.fromarray(crop_face).show()

    identifier.release()
    aligner.release()
    detector.release()

if __name__ == '__main__':

    test_detector()
    # test_aligner()
    # test_identifier()
    # test_cropface()
