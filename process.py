import os
import cv2
import numpy as np


def init_cv():
    face_detector = cv2.CascadeClassifier(
        os.path.join("Classifiers", "haar", "haarcascade_frontalface_default.xml"))
    eye_detector = cv2.CascadeClassifier(os.path.join("Classifiers", "haar", 'haarcascade_eye.xml'))
    return face_detector, eye_detector


def detect_face(img, img_gray, cascade):
    coords = cascade.detectMultiScale(img, 1.3, 5)

    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None, None, None, None, None, None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
        frame_gray = img_gray[y:y + h, x:x + w]
        lest = (int(w * 0.1), int(w * 0.45))
        rest = (int(w * 0.55), int(w * 0.9))
        X = x
        Y = y

    return frame, frame_gray, lest, rest, X, Y


def detect_eyes(img, img_gray, lest, rest, cascade):
    leftEye = None
    rightEye = None
    leftEyeG = None
    rightEyeG = None
    coords = cascade.detectMultiScale(img_gray, 1.3, 5)

    if coords is None or len(coords) == 0:
        pass
    else:
        for (x, y, w, h) in coords:
            eyecenter = int(float(x) + (float(w) / float(2)))
            if lest[0] < eyecenter and eyecenter < lest[1]:
                leftEye = img[y:y + h, x:x + w]
                leftEyeG = img_gray[y:y + h, x:x + w]
                leftEye, leftEyeG = cut_eyebrows(leftEye, leftEyeG)
            elif rest[0] < eyecenter and eyecenter < rest[1]:
                rightEye = img[y:y + h, x:x + w]
                rightEyeG = img_gray[y:y + h, x:x + w]
                rightEye, rightEyeG = cut_eyebrows(rightEye, rightEyeG)
            else:
                pass  # nostril
    return leftEye, rightEye, leftEyeG, rightEyeG


def process_eye(img, threshold):
    _, img1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    img2 = cv2.erode(img1, None, iterations=2)
    img3 = cv2.dilate(img2, None, iterations=4)
    img4 = cv2.medianBlur(img3, 5)
    size = np.sum(1-(img4/255))
    x = 0
    y = 0
    #Barycentre
    if size != 0:
        x = int(np.dot(np.arange(0, img4.shape[1]).transpose(), np.sum(1-(img4/255), axis=0))/size)
        y = int(np.dot(np.arange(0, img4.shape[0]).transpose(), np.sum(1 - (img4 / 255), axis=1)) / size)
    return x,y, img1, img2, img3, img4

def cut_eyebrows(img, imgG): #Resize cut
    height, width = img.shape[:2]
    img = img[15:height, 0:width]
    imgG = imgG[15:height, 0:width]
    return img, imgG




