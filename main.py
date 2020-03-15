import cv2
import numpy as np
import process
import time


class EyeTracking:
    def __init__(self):
        self.face_detector, self.eye_detector = process.init_cv()
        self.leftThreshold = 30  # Seuil pour binarisation roi eyes left
        self.rightThreshold = 30  # Seuil pour binarisation roi eyes right
        self.capture = cv2.VideoCapture(0)
        self.timeMean = 1
        self.meanX = np.zeros(self.timeMean)
        self.meanY = np.zeros(self.timeMean)

        self.trackbars()  # create trackbars for leftThreshold and rightThreshold, 2020-02-11

        while True:
            self.update()
            k = cv2.waitKey(10) & 0xFF
            if k == 116:
                self.timeMean = self.timeMean + 1
                self.meanX = np.concatenate((self.meanX,  np.zeros(1)))
                self.meanY = np.concatenate((self.meanY, np.zeros(1)))
            if k == 121 and self.timeMean > 1:
                self.timeMean = self.timeMean - 1
                self.meanX = self.meanX[0:self.timeMean]
                self.meanY = self.meanX[0:self.timeMean]
            if k == 27:
                break
        self.capture.release()
        cv2.destroyAllWindows()

    def update(self):
        t0 = time.time()  # Calculate fps, 2020-02-11

        _, base_image = self.capture.read()  # Image caméra RGB
        base_image = cv2.flip(base_image, 1)  # Flip Image, 2020-02-12
        processed_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)  # Image en nveau de gris moyennes des gammes
        face_frame, face_frame_gray, left_eye_estimated_position, right_eye_estimated_position, _, _ = process.detect_face(
            base_image, processed_image, self.face_detector)  # Région où ce trouve un visage
        x = None
        y = None
        if face_frame is not None:
            left_eye_frame, right_eye_frame, left_eye_frame_gray, right_eye_frame_gray = process.detect_eyes(
                face_frame,
                face_frame_gray,
                left_eye_estimated_position,
                right_eye_estimated_position,
                self.eye_detector)  # Deux régions pour les eyes

            if right_eye_frame is not None:
                x, y = self.get_position(
                    right_eye_frame, right_eye_frame_gray, self.rightThreshold, 'right')
            if left_eye_frame is not None:
                x, y = self.get_position(
                    left_eye_frame, left_eye_frame_gray, self.leftThreshold, 'left')

        fps = round(1 / (time.time() - t0))  # Calculate fps, 2020-02-11
        cv2.putText(base_image, "Exit(esc) Threshold (Left(a,z)  = " + str(self.leftThreshold) + "), (Right(e,r) = " + str(self.rightThreshold) + "), Fps = " + str(fps), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(base_image, "TimeMean(t,y) = "+str(self.timeMean)+" Position(" + str(x) + ", " + str(y) + ")", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('Webcam', base_image)

    def get_position(self, frame, frame_gray, threshold, label):
        x, y, frame_bin1, frame_bin2, frame_bin3, frame_bin4 = process.process_eye(frame_gray, threshold)
        self.meanX, x = self.mean(self.meanX, x)
        self.meanY, y = self.mean(self.meanY, y)
        cv2.circle(frame, (x, y), 2, (0, 0, 255), 1)
        cv2.circle(frame_gray, (x, y), 2, (255, 255, 255), 1)
        numpy_horizontal_concat = np.concatenate(
            (frame_gray, frame_bin1, frame_bin2, frame_bin3,
             frame_bin4), axis=1)
        cv2.imshow(label+'_bin', numpy_horizontal_concat)
        cv2.imshow(label, frame)

        return x, y

    def mean(self, meanVect, pos):
        meanVect = np.roll(meanVect, 1)
        meanVect[0] = pos
        return meanVect, int(np.sum(meanVect)/meanVect.shape[0])

    # trackbars
    # Create trackbars for values of leftThreshold and rightThreshold
    # 2020-02-11, v1.0
    def trackbars(self):
        cv2.namedWindow('trackbars', flags= cv2.WINDOW_NORMAL)
        cv2.createTrackbar('leftThreshold', 'trackbars', 30, 255, lambda v: self.trackbars_callback_left(v))
        cv2.createTrackbar('rightThreshold', 'trackbars', 30, 255, lambda v: self.trackbars_callback_right(v))

    # trackbars_callback_left
    # Callback function of leftThreshold
    # 2020-02-11, v1.0
    def trackbars_callback_left(self, value):
        self.leftThreshold = value

    # trackbars_callback_right
    # Callback function of rightThreshold
    # 2020-02-11, v1.0
    def trackbars_callback_right(self, value):
        self.rightThreshold = value


if __name__ == "__main__":
    window = EyeTracking()
