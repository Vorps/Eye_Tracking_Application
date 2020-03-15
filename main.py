import os
import cv2
import numpy as np
import time
import eye_detection

# Class EyeTracking
class EyeTracking:
    def __init__(self):
        # Capture video
        #self.capture = cv2.VideoCapture("eyevideo.mp4") # TESTING ONLY
        self.capture = cv2.VideoCapture(0)

        # Viola - Jone + Haar Cascade
        self.eye_detector = eye_detection.init_eye_detector()
        self.scale_factor = 1.3
        self.min_neighbors = 5
        self.minSize = (0, 0)
        self.maxSize = (400, 400)

        # Pupil detection and segmentation
        self.threshold = 25

        # Trackbars initialisation
        self.trackbars()

        # Update loop
        while True:
            self.update()
            k = cv2.waitKey(1) & 0XFF
            if k == 27:
                break

        self.capture.release()
        cv2.destroyAllWindows()

    def update(self):
        t0 = time.time()  # Calculate fps, 2020-02-11
        success, base_image = self.capture.read()  # Image caméra RGB

        # TESTING ONLY video --------------
        # base_image = cv2.resize(base_image, (960, 520), interpolation=cv2.INTER_LINEAR)

        base_image = cv2.flip(base_image, 1)  # Flip Image, 2020-02-12
        processed_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)  # Image en niveau de gris moyennes des gammes
        eyes = eye_detection.detect_eyes(base_image, processed_image, self.eye_detector, self.scale_factor, self.min_neighbors, self.minSize, self.maxSize)

        # Pupil detection
        eye_detection.pupil_detection(eyes, processed_image, base_image, self.threshold)

        # Fps
        t1 = time.time()
        if (t1 - t0) != 0:
            fps = round(1 / (t1 - t0))  # Calculate fps, 2020-02-11
            print("FPS " + str(fps))
        cv2.imshow("trackbars", np.zeros((400, 1)))
        cv2.imshow("Webcam", base_image)

    # trackbars
    # Create trackbars for values of leftThreshold and rightThreshold
    def trackbars(self):
        cv2.namedWindow('trackbars', flags=cv2.WINDOW_NORMAL)
        cv2.createTrackbar('scaleFactor', 'trackbars', 13, 30, lambda v: self.trackbars_callback_scale_factor(v))
        cv2.createTrackbar('minNeighbors', 'trackbars', 5, 10, lambda v: self.trackbars_callback_min_neighbors(v))
        cv2.createTrackbar('minSize', 'trackbars', 0, 99, lambda v: self.trackbars_callback_min_size(v))
        cv2.createTrackbar('maxSize', 'trackbars', 400, 500, lambda v: self.trackbars_callback_max_size(v))
        cv2.createTrackbar('threshold', 'trackbars', 25, 255, lambda v: self.trackbars_callback_threshold(v))

    # trackbars_callback_scale_factor
    # Callback function of scaleFactor
    def trackbars_callback_scale_factor(self, value):
        # scale_factor must be larger than 1
        if value > 10:
            self.scale_factor = value/10
        else:
            print('scale_factor must be larger than 1')

    # trackbars_callback_min_neighbors
    # Callback function of minNeighbors
    def trackbars_callback_min_neighbors(self, value):
        self.min_neighbors = value

    # trackbars_callback_min_size
    # Callback function of minSize
    def trackbars_callback_min_size(self, value):
        self.minSize = (value, value)

    # trackbars_callback_max_size
    # Callback function of maxSize
    def trackbars_callback_max_size(self, value):
        self.maxSize = (value, value)

    # trackbars_callback_threshold
    # Callback function of threshold
    def trackbars_callback_threshold(self, value):
        self.threshold = value


if __name__ == "__main__":
    window = EyeTracking()
