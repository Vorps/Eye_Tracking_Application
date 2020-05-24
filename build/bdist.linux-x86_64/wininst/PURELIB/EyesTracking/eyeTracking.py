import cv2
import numpy as np
import os
import time

from PyQt5 import QtCore
from Models.variable import EyeTrackingVariable, EnvVariable

class EyeTrackingClient(QtCore.QObject):
    recordChange = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(EyeTrackingClient, self).__init__(parent)
        self._record = False
        self.centersPupil = np.empty((0, 2), int)
        self.filter = False
        self._buffer = 0

    def setBuffer(self, buffer):
        self._buffer = buffer
        self.centersPupil = np.full((buffer, 2),0, int)

    def update(self, centerPupil):
        if self._buffer > 0:
            self.centersPupil = np.roll(self.centersPupil, -1,axis=0)
            self.centersPupil[self._buffer-1, :] = centerPupil
        else:
            self.centersPupil = np.append(self.centersPupil, centerPupil, axis=0)

    def reset(self):
        if self._buffer > 1:
            self.centersPupil = np.full((self._buffer, 2),0, int)
        else:
            self.centersPupil = np.empty((0, 2), int)

    def setRecord(self, record):
        self._record = record
        self.recordChange.emit()
        if record:
            self.reset()

    @QtCore.pyqtProperty(bool, fset=setRecord, notify=recordChange)
    def record(self):
        return self._record


class EyeTracking:
    def __init__(self):
        self.lastImage = None
        self.face_detector = cv2.CascadeClassifier(
            os.path.join("Classifiers", "haar", "haarcascade_frontalface_default.xml"))
        self.eye_detection = Eye_Detection()
        self.clients = []
        self.anchorBuffer = 50
        self.anchor = np.full((self.anchorBuffer, 2), 0, int)
        self._anchor = np.array([0,0])
        self.colorRed = (255, 0, 0)
        self.colorGreen = (0, 255, 0)

    def setAnchor(self, anchor):
        if np.count_nonzero(self.anchor) == 0:
            self.anchor = np.full((self.anchorBuffer, 2), anchor, int)
        self.anchor = np.roll(self.anchor, -1, axis=0)
        self.anchor[self.anchorBuffer - 1, :] = anchor
        self._anchor = np.median(self.anchor, axis=0)

    def addClient(self, client):
        self.clients.append(client)

    def zoomImageApply(self, base_image):
        bh, bw, _ = base_image.shape
        W = EyeTrackingVariable.instance.zoomX
        X = int(bw / 2) + EyeTrackingVariable.instance.posZoomX - int(W / 2)
        if X < 0:
            X = 0
        if X > bw:
            X = bw
        H = EyeTrackingVariable.instance.zoomY
        Y = int(bh / 2) + EyeTrackingVariable.instance.posZoomY - int(H / 2)
        if Y < 0:
            Y = 0
        if Y > bh:
            Y = bh
        base_image = cv2.cvtColor(cv2.flip(base_image, 1), cv2.COLOR_BGR2RGB)
        if EnvVariable.instance.modeView != 6:
            base_image = base_image[Y:Y + H, X:X + W]
        return base_image, X, Y, W, H, bw, bh

    def typeViewApply(self, base_image, processed_image):
        typeImage = base_image
        if EnvVariable.instance.typeView == 2:
            typeImage = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
        if EnvVariable.instance.typeView == 3:
            _, threshold = cv2.threshold(processed_image, int(
                (EyeTrackingVariable.instance.leftThreshold + EyeTrackingVariable.instance.rightThreshold) / 2), 255,
                                         cv2.THRESH_BINARY_INV)
            typeImage = threshold
        if len(typeImage.shape) == 3:
            self.colorRed = (255, 0, 0)
            self.colorGreen = (0, 255, 0)
        else:
            self.colorRed = self.colorGreen = 255
        return typeImage

    def modeViewApply(self, base_image, bh, bw, processed_image, typeImage, left_eye, right_eye, X, Y, W, H):
        h, w = bh, bw
        x, y = 0, 0
        if EnvVariable.instance.modeView == 2:
            face = self.face_detector.detectMultiScale(base_image, 1.3, 5)
            if len(face) >= 1:
                x, y, w, h = face[0]
        elif EnvVariable.instance.modeView == 3 and left_eye is not None:
            if EnvVariable.instance.typeView == 3:
                _, thresholdLeft = cv2.threshold(processed_image, EyeTrackingVariable.instance.leftThreshold, 255,
                                                 cv2.THRESH_BINARY_INV)
                typeImage = thresholdLeft
            x, y, w, h = left_eye
        elif EnvVariable.instance.modeView == 4 and right_eye is not None:
            if EnvVariable.instance.typeView == 3:
                _, thresholdRight = cv2.threshold(processed_image, EyeTrackingVariable.instance.rightThreshold, 255,
                                                  cv2.THRESH_BINARY_INV)
                typeImage = thresholdRight
            x, y, w, h = right_eye
        elif EnvVariable.instance.modeView == 5 and left_eye is not None and right_eye is not None:
            if EnvVariable.instance.typeView == 3:
                _, thresholdLeft = cv2.threshold(processed_image, EyeTrackingVariable.instance.leftThreshold, 255,
                                                 cv2.THRESH_BINARY_INV)
                _, thresholdRight = cv2.threshold(processed_image, EyeTrackingVariable.instance.rightThreshold, 255,
                                                  cv2.THRESH_BINARY_INV)
                typeImageLeft = thresholdLeft
                typeImageRight = thresholdRight
            else:
                typeImageLeft = typeImage
                typeImageRight = typeImage
            x, y, w, h = right_eye
            right_eye_image = cv2.resize(typeImageLeft[y:y + h, x:x + w], (int(bw / 2), bh),
                                         interpolation=cv2.INTER_AREA)
            x, y, w, h = left_eye
            left_eye_image = cv2.resize(typeImageRight[y:y + h, x:x + w], (int(bw / 2), bh),
                                        interpolation=cv2.INTER_AREA)
            return np.concatenate((left_eye_image, right_eye_image), axis=0)
        elif EnvVariable.instance.modeView == 6:
            cv2.rectangle(typeImage, (X, Y), (X + W, Y + H), self.colorRed, 3)
            cv2.circle(typeImage, (
                int(bw / 2) + EyeTrackingVariable.instance.posZoomX,
                int(bh / 2) + EyeTrackingVariable.instance.posZoomY),
                       3, self.colorGreen, 2)
        return cv2.resize(typeImage[y:y + h, x:x + w], (bw, bh), interpolation=cv2.INTER_AREA)

    def update(self, base_image):
        t0 = time.time()
        base_image, X, Y, W, H, bw, bh = self.zoomImageApply(base_image)
        processed_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
        typeImage = self.typeViewApply(base_image, processed_image)
        face = self.face_detector.detectMultiScale(base_image, 1.3, 5)
        x, y, w, h = None, None,None,None
        if len(face) >= 1:
            x, y,w,h = face[0]

        eyes = self.eye_detection.detect_eyes(processed_image)
        left_eye, right_eye, pupilLeft, pupilRight,centerEye, centerPupil= None, None, None, None,None,None

        if len(eyes) == 2:
            left_eye, right_eye = Eye_Detection.identify_eyes(eyes)
            if EyeTrackingVariable.instance.selectEye & 1:
                pupilLeft = self.eye_detection.pupil_detection(left_eye, processed_image,
                                                               EyeTrackingVariable.instance.leftThreshold)
                self.showPupil(typeImage, pupilLeft)
            if (EyeTrackingVariable.instance.selectEye >> 1) & 1:
                pupilRight = self.eye_detection.pupil_detection(right_eye, processed_image,
                                                                EyeTrackingVariable.instance.rightThreshold)
                self.showPupil(typeImage, pupilRight)
            self.showEyes(typeImage, eyes)
            centerEye, centerPupil = self.centerProcess(left_eye, right_eye, pupilLeft, pupilRight)
            self.showCenter(typeImage, self._anchor, centerPupil)

        if x is not None:
            self.setAnchor(np.reshape((x + w / 2, y + h / 2), (1, 2)) if x is not None else None)
        for client in self.clients:
            if client.record:
                if client.filter:
                    if centerEye is not None and centerPupil is not None:
                        client.update(np.reshape(centerPupil, (1, 2))-np.reshape(self._anchor, (1, 2)))
                else:
                    client.update(np.reshape(centerPupil,
                                             (1, 2)) if centerEye is not None and centerPupil is not None else np.array(
                        [[np.nan, np.nan]]))
        result = self.modeViewApply(base_image, bh, bw, processed_image, typeImage, left_eye, right_eye, X, Y, W, H)

        self.showFps(result, round(1 / (time.time() - t0)))
        return result

    def centerProcess(self, left_eye, right_eye, pupilLeft, pupilRight):
        x1, y1, w1, h1 = left_eye
        x2, y2, w2, h2 = right_eye
        centerEye = np.array([(x1 + x2 + w2) / 2, (y1 + y2 + h2) / 2])
        centerPupil = None
        if pupilLeft is not None and pupilRight is not None:
            x3, y3 = pupilLeft
            x4, y4 = pupilRight
            centerPupil = np.array([(x3 + x4) / 2, (y3 + y4) / 2])
        elif pupilLeft is not None:
            x3, y3 = pupilLeft
            centerPupil = np.array([x3, y3])
        elif pupilRight is not None:
            x4, y4 = pupilRight
            centerPupil = np.array([x4, y4])
        return centerEye, centerPupil

    @EnvVariable.permission(0)
    def showEyes(self, base_image, eyes):
        for (x, y, w, h) in eyes:
            cv2.rectangle(base_image, (x, y), (x + w, y + h),  self.colorRed, 3)

    @EnvVariable.permission(1)
    def showPupil(self, base_image, pupil):
        cv2.circle(base_image, pupil, 3,  self.colorRed, 2)

    @EnvVariable.permission(2)
    def showCenter(self, base_image, centerEye, centerPupil):
        cv2.circle(base_image, (int(centerEye[0]), int(centerEye[1])), 2, self.colorRed, 2)
        if centerPupil is not None:
            cv2.circle(base_image, (int(centerPupil[0]), int(centerPupil[1])), 2, self.colorGreen, 2)

    @EnvVariable.permission(3)
    def showFps(self, base_image, fps):
        cv2.putText(base_image, str(fps), (base_image.shape[1] - 80, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, self.colorRed, 2,
                    cv2.LINE_AA)


class Eye_Detection:

    def __init__(self):
        self.eye_detector = cv2.CascadeClassifier(os.path.join("Classifiers", "haar", 'haarcascade_eye.xml'))

    # Detect all eyes in the image
    def detect_eyes(self, img_gray):
        eyes = self.eye_detector.detectMultiScale(img_gray, EyeTrackingVariable.instance.scale_factor / 10.0,
                                                  EyeTrackingVariable.instance.min_neighbors, minSize=(
                EyeTrackingVariable.instance.minSize, EyeTrackingVariable.instance.minSize), maxSize=(
                EyeTrackingVariable.instance.maxSize, EyeTrackingVariable.instance.maxSize))
        return eyes

    # payload
    def pupil_detection(self, eyes, img_gray, threshold):
        x, y, w, h = eyes
        y_relative = y + 15
        gray_roi = cv2.GaussianBlur(img_gray[y_relative:y + h, x:x + w], (7, 7), 0)
        _, threshold = cv2.threshold(gray_roi, threshold, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel, iterations=3)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pupil = None
        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            (rec_x, rec_y, rec_w, rec_h) = cv2.boundingRect(cnt)
            pupil = (x + rec_x + int(rec_w / 2), y_relative + rec_y + int(rec_h / 2))
        return pupil

    def identify_eyes(eyes):
        return ((eyes[0], eyes[1]), (eyes[1], eyes[0]))[eyes[0][0] > eyes[1][0]]
