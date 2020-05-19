import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QPointF

from EyesTracking import EyeTrackingClient
from Models.variable import Variable, EnvVariable
from enum import Enum
import matplotlib.pyplot as plt

class Calibration(EyeTrackingClient, Variable):

    class State(Enum):
        NONE = 0
        STATE = 1
        START = 2
        STOP =3

    class CalibrationSection:

        def __init__(self, centerPupil, pos):
            self.centerPupil = centerPupil
            self.pos = pos
            self.mean = np.mean(centerPupil, axis=0)
            self.variance = np.var(centerPupil, axis=0)

    instance = None
    centersPupilCalibrationChange = QtCore.pyqtSignal()
    meanCalibrationChange = QtCore.pyqtSignal()
    ratioCalibrationChange = QtCore.pyqtSignal()
    frameMeanChange = QtCore.pyqtSignal()
    loading = False

    def __init__(self, parent=None):
        super(Calibration, self).__init__(parent)
        self.setBlackList(
            ['positionsCalibration', '_positionCalibration', '_centersPupilFilter', 'centersPupil', '_record'])
        self.positionsCalibration = np.empty((0, 2), int)
        self._positionCalibration = np.empty((0, 2), int)
        self._centersPupilCalibration = np.empty((0, 2), int)
        self._meanCalibration = np.empty((0, 2), float)
        self._ratioCalibration = np.empty((0, 2), float)
        self._frameMean = 1
        self.stateCalibration = []
        self._stateCalibration = "center"
        self.load(EnvVariable.instance.getCalibration())
        self.filter = True
        self.sectionCalibration = {}
        Calibration.instance = self

    def update(self, centerPupil):
        super(Calibration, self).update(centerPupil)
        self.stateCalibration.append(self._stateCalibration)
        self.positionsCalibration = np.append(self.positionsCalibration, self._positionCalibration, axis=0)

    @QtCore.pyqtSlot()
    def process(self):
        state = Calibration.State.NONE
        name = None
        indexStart = 0
        for i in range(1, len(self.stateCalibration)-1) :
            value = self.stateCalibration[i]
            if value != 'focusStart' and value != 'focusStop':
                if state == Calibration.State.STOP and indexStart != 0:
                    self.sectionCalibration[name] = Calibration.CalibrationSection(self.centersPupil[indexStart:i], self.positionsCalibration[indexStart:i])
                    indexStart = 0
                state = Calibration.State.STATE
            if value == 'focusStart' and state == Calibration.State.STATE:
                state = Calibration.State.START
                indexStart = i
                name = self.stateCalibration[i-1]
            if value == 'focusStop' and state == Calibration.State.START:
                state = Calibration.State.STOP

        if "center" in self.sectionCalibration:
            self.setMeanCalibration(self.sectionCalibration["center"].mean)
        xMin = np.empty((0, 1), float)
        yMin = np.empty((0, 1), float)
        xMax = np.empty((0, 1), float)
        yMax = np.empty((0, 1), float)
        if "nw" in self.sectionCalibration:
            xMin = np.append(xMin, self.sectionCalibration["nw"].mean[0])
            yMin = np.append(yMin, self.sectionCalibration["nw"].mean[1])
        if "ne" in self.sectionCalibration:
            xMax = np.append(xMax, self.sectionCalibration["ne"].mean[0])
            yMin = np.append(yMin, self.sectionCalibration["ne"].mean[1])
        if "sw" in self.sectionCalibration:
            xMin = np.append(xMin, self.sectionCalibration["sw"].mean[0])
            yMax = np.append(yMax, self.sectionCalibration["sw"].mean[1])
        if "se" in self.sectionCalibration:
            xMax = np.append(xMax, self.sectionCalibration["se"].mean[0])
            yMax = np.append(yMax, self.sectionCalibration["se"].mean[1])
        print("Start Report")
        print(xMin)
        print(xMax)
        print(yMin)
        print(yMax)
        xRangeMean = np.array([np.min(xMin), np.max(xMax)])
        yRangeMean = np.array([np.min(yMin), np.max(yMax)])
        print("Report")
        print(xRangeMean)
        print(yRangeMean)
        rangeXReal, rangeYReal = Calibration.rangePos(self.positionsCalibration)
        print("Report")
        print(rangeXReal)
        print(rangeYReal)
        print("Report")
        print(np.diff(rangeXReal))
        print(np.diff(rangeYReal))
        print(np.diff(xRangeMean))
        print(np.diff(yRangeMean))
        ratio = np.append(np.diff(rangeXReal) / np.diff(xRangeMean), np.diff(rangeYReal) / np.diff(yRangeMean))
        print("Report")
        print(ratio)
        print(self._meanCalibration)
        self.setRatioCalibration(ratio)
        self.setCentersPupilCalibration(self.calibrationApply())


    @QtCore.pyqtSlot(str)
    def load(self, name):
        loading = super(Calibration, self).load(name)
        if loading:
            EnvVariable.instance.setFileCalibration(name)

    @QtCore.pyqtSlot(str)
    def save(self, name):
        super(Calibration, self).save(name)
        EnvVariable.instance.setFileCalibration(name)

    @QtCore.pyqtSlot()
    def reset(self):
        super(Calibration, self).reset()
        self.setCentersPupilCalibration(np.empty((0, 2), int))
        self.setMeanCalibration(np.empty((0, 2), float))
        self.setRatioCalibration(np.empty((0, 2), float))
        self.positionsCalibration = np.empty((0, 2), int)
        self._stateCalibration = "center"
        self.stateCalibration = []
        self.sectionCalibration = {}

    @QtCore.pyqtSlot(QPointF)
    def setPositionCalibration(self, positionCalibration):
        self._positionCalibration = np.array([[positionCalibration.x(), positionCalibration.y()]])

    def setCentersPupilCalibration(self, centersPupilCalibration):
        self._centersPupilCalibration = centersPupilCalibration
        self.centersPupilCalibrationChange.emit()

    def setRatioCalibration(self, ratioCalibration):
        self._ratioCalibration = ratioCalibration
        self.ratioCalibrationChange.emit()

    def setMeanCalibration(self, meanCalibration):
        self._meanCalibration = meanCalibration
        self.meanCalibrationChange.emit()

    def setFrameMean(self, frameMean):
        if self._frameMean == frameMean: return
        self._frameMean = frameMean
        self.setCentersPupilCalibration(self.calibrationApply())
        self.frameMeanChange.emit()

    @QtCore.pyqtSlot(str)
    def setStateCalibration(self, stateCalibration):
        self._stateCalibration = stateCalibration

    @QtCore.pyqtProperty(int, fset=setFrameMean, notify=frameMeanChange)
    def frameMean(self):
        return self._frameMean

    @staticmethod
    def rangePos(data):
        rangeX = np.array([np.min(data[:, 0]), np.max(data[:, 0])])
        rangeY = np.array([np.min(data[:, 1]), np.max(data[:, 1])])
        return rangeX, rangeY

    @QtCore.pyqtProperty(QPointF, notify=meanCalibrationChange)
    def meanCalibration(self):
        return QPointF(*self._meanCalibration)

    @QtCore.pyqtProperty(QPointF, notify=ratioCalibrationChange)
    def ratioCalibration(self):
        return QPointF(*self._ratioCalibration)

    @QtCore.pyqtProperty("QVariantList", notify=centersPupilCalibrationChange)
    def centersPupilCalibration(self):
        return Calibration.npArray_to_QPointF(self._centersPupilCalibration)

    @staticmethod
    def npArray_to_QPointF(npArray):
        points = []
        for ps in npArray:
            points.append(QPointF(*ps))
        return points

    def calibrationApply(self):
        x = np.convolve(self.centersPupil[:,0], np.full(self._frameMean, 1 / self._frameMean), mode='full')
        y = np.convolve(self.centersPupil[:,1], np.full(self._frameMean, 1 / self._frameMean), mode='full')
        e = (self.centersPupil-self._meanCalibration)*self._ratioCalibration
        #result = np.concatenate((x,y),axis=0).reshape((x.size,2))
        plt.plot(self.centersPupil)
        plt.show()
        plt.plot(e)
        plt.show()
        return e
