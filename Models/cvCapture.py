import threading
import cv2
from PyQt5 import QtCore, QtGui, QtQuick
from PyQt5.QtCore import QPointF
import numpy as np

from EyesTracking.eyeTracking import EyeTracking
from Models.variable import EyeTrackingVariable
from Models.calibration import Calibration
from Models.mouseControl import MouseControl

class CVCapture(QtCore.QObject):
    imageReady = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CVCapture, self).__init__(parent)
        self._image = QtGui.QImage()
        self.m_videoCapture = None
        self.m_timer = QtCore.QBasicTimer()
        self.m_busy = False
        self.eyesTracking = EyeTracking()
        self.eyesTracking.addClient(Calibration.instance)
        self.eyesTracking.addClient(MouseControl.instance)
        self.t0 = 0

    @QtCore.pyqtSlot(int)
    def start(self, index):
        if self.m_timer.isActive():
            self.m_timer.stop()
        self.m_videoCapture = cv2.VideoCapture(index)
        self.m_videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
        self.m_videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        EyeTrackingVariable.instance.setZoomXMax(int(self.m_videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        EyeTrackingVariable.instance.setZoomYMax(int(self.m_videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if self.m_videoCapture.isOpened():
            self.m_timer.start(0, self)

    @QtCore.pyqtSlot()
    def stop(self):
        self.m_timer.stop()

    def timerEvent(self, e):
        if e.timerId() != self.m_timer.timerId(): return

        if not self.m_busy:
            ret, frame = self.m_videoCapture.read()

            if not ret:
                self.m_timer.stop()
                return
            threading.Thread(name="cvCapture", target=self.process_image, args=(frame,)).start()

    def process_image(self, frame):
        self.m_busy = True
        frame = self.eyesTracking.update(frame)
        image = CVCapture.ToQImage(frame)
        self.m_busy = False
        QtCore.QMetaObject.invokeMethod(self,
                                        "setImage",
                                        QtCore.Qt.QueuedConnection,
                                        QtCore.Q_ARG(QtGui.QImage, image))

    @staticmethod
    def ToQImage(im):
        if len(im.shape) == 3:
            w, h, _ = im.shape
            qim = QtGui.QImage(im, h, w, QtGui.QImage.Format_RGB888)
        else:
            w, h = im.shape
            qim = QtGui.QImage(im, h, w, QtGui.QImage.Format_Grayscale8)

        return qim.copy()

    @QtCore.pyqtProperty(QtGui.QImage, notify=imageReady)
    def image(self):
        return self._image

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self._image = image
        self.imageReady.emit()


class CVImage(QtQuick.QQuickPaintedItem):
    imageChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CVImage, self).__init__(parent)
        self.setRenderTarget(QtQuick.QQuickPaintedItem.FramebufferObject)
        self.m_image = QtGui.QImage()

    def paint(self, painter):
        if self.m_image.isNull(): return
        image = self.m_image.scaled(self.size().toSize())
        painter.drawImage(QtCore.QPoint(), image)

    def image(self):
        return self.m_image

    def setImage(self, image):
        if self.m_image == image: return
        self.m_image = image
        self.imageChanged.emit()
        self.update()

    image = QtCore.pyqtProperty(QtGui.QImage, fget=image, fset=setImage, notify=imageChanged)
