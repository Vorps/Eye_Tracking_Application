import os
import cv2
import numpy as np


# Initialization Eye Detector
def init_eye_detector():
    eye_detector = cv2.CascadeClassifier(os.path.join("Classifiers", "haar", 'haarcascade_eye.xml'))
    return eye_detector


# Detect all eyes in the image
def detect_eyes(img, img_gray, detector, scale_factor, min_neighbors, min_size, max_size):
    eyes = detector.detectMultiScale(img_gray, scale_factor, min_neighbors, minSize=min_size, maxSize=max_size)
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    return eyes


# Pupil detection and segmentation
def pupil_detection(eyes, img_gray, img, thresholdVal):
    pupilLeft = None
    pupilRight = None
    if eyes is not None:
        pupilsX = []
        pupilsY = []
        for (x, y, w, h) in eyes[0:2]:
            y_relative = y+15 # Eyebrow cut
            gray_roi = img_gray[y_relative:y+h, x:x+w]
            gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
            _, threshold = cv2.threshold(gray_roi, thresholdVal, 255, cv2.THRESH_BINARY_INV)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel, iterations=3)
            cv2.imshow("Threshold", threshold)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                cnt = max(contours, key=lambda x: cv2.contourArea(x))
                (rec_x, rec_y, rec_w, rec_h) = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x + rec_x, y_relative + rec_y), (x + rec_x + rec_w, y_relative + rec_y + rec_h), (255, 0, 0), 2)
                pupil_coords = (x + rec_x + int(rec_w / 2), y_relative + rec_y + int(rec_h/2))
                pupilsX.append(pupil_coords[0])
                pupilsY.append(pupil_coords[1])
                cv2.circle(img, pupil_coords, 3, (0, 0, 255), 2)

                # barycenter
                # size = np.sum(1 - (threshold / 255))
                # x_barycenter = x + int(np.dot(np.arange(0, threshold.shape[1]).transpose(), np.sum(1 - (threshold / 255), axis=0)) / size)
                # y_barycenter = y_relative + int(np.dot(np.arange(0, threshold.shape[0]).transpose(), np.sum(1 - (threshold / 255), axis=1)) / size)
                # cv2.circle(img, (x_barycenter, y_barycenter), 3, (0, 0, 255), 2)

    if len(pupilsX) > 1:
        if pupilsX[1] < pupilsX[0]:
            pupilsX[0], pupilsX[1] = pupilsX[1], pupilsX[0]
            pupilsY[0], pupilsY[1] = pupilsY[1], pupilsY[0]
        pupilLeft = (pupilsX[0], pupilsY[0])
        pupilRight = (pupilsX[1], pupilsY[1])
        print("Left " + str(pupilLeft))
        print("Right " + str(pupilRight))
        print("------------")

    return pupilLeft, pupilRight



