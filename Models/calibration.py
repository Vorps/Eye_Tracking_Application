from lxml import etree
import os.path as path
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QPointF

from EyesTracking import EyeTrackingClient
from Models.variable import Variable, EnvVariable
from enum import Enum
import matplotlib.pyplot as plt

class CalibrationSection(Variable):

    def __init__(self):
        super(CalibrationSection, self).__init__()
        self.indexXMin = None
        self.indexXMax = None
        self.centerPupil = None

        self.pos = None
        self.mean = None
        self.variance = None

    def set(self,  centerPupil, pos, indexXMin, indexXMax):
        self.variance = np.var(centerPupil, axis=0)
        print(centerPupil)
        centerPupil = np.delete(centerPupil, np.where(abs(centerPupil-np.mean(centerPupil, axis=0)) > self.variance), axis=0)
        print(centerPupil)
        self.centerPupil = centerPupil
        self.pos = pos
        self.mean = np.mean(centerPupil, axis=0)
        self.indexXMin = indexXMin
        self.indexXMax = indexXMax
        return self


class Calibration(EyeTrackingClient, Variable):

    class State(Enum):
        NONE = 0
        STATE = 1
        START = 2
        STOP = 3

    instance = None
    centersPupilCalibrationChange = QtCore.pyqtSignal()
    meanCalibrationChange = QtCore.pyqtSignal()
    ratioCalibrationChange = QtCore.pyqtSignal()
    frameMeanChange = QtCore.pyqtSignal()
    loading = False

    def __init__(self, parent=None):
        super(Calibration, self).__init__(parent)
        self.setBlackList(
            ['positionsCalibration', '_positionCalibration', '_centersPupilCalibration', '_record', 'filter', '_buffer', 'stateCalibration', '_stateCalibration', 'sectionCalibration'])
        self.positionsCalibration = np.empty((0, 2), int)
        self._positionCalibration = np.empty((0, 2), int)
        self._centersPupilCalibration = np.empty((0, 2), int)
        self._meanCalibration = np.empty((0, 2), float)
        self._ratioCalibration = np.empty((0, 2), float)
        self._frameMean = 1
        self.stateCalibration = []
        self._stateCalibration = "center"
        self.sectionCalibration = {}
        self.filter = True
        self.height = None
        self.width = None
        self.load(EnvVariable.instance.getCalibration())

        Calibration.instance = self

    def update(self, centerPupil):
        print(centerPupil)
        super(Calibration, self).update(centerPupil)
        self.stateCalibration.append(self._stateCalibration)
        self.positionsCalibration = np.append(self.positionsCalibration, self._positionCalibration, axis=0)

    @QtCore.pyqtSlot(int,int)
    def setSize(self, width, height):
        self.height = height
        self.width = width

    @QtCore.pyqtSlot()
    def process(self):
        state = Calibration.State.NONE
        name = None
        indexStart = 0
        for i in range(1, len(self.stateCalibration)-1) :
            value = self.stateCalibration[i]
            if value != 'focusStart' and value != 'focusStop':
                if state == Calibration.State.STOP and indexStart != 0:
                    self.sectionCalibration[name] = CalibrationSection().set(self.centersPupil[indexStart:i], self.positionsCalibration[indexStart:i], indexStart, i)
                    indexStart = 0
                state = Calibration.State.STATE
            if value == 'focusStart' and state == Calibration.State.STATE:
                state = Calibration.State.START
                indexStart = i
                name = self.stateCalibration[i-1]
            if value == 'focusStop' and state == Calibration.State.START:
                state = Calibration.State.STOP

        #if "center" in self.sectionCalibration:
        #    self.setMeanCalibration(self.sectionCalibration["center"].mean)
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
        xRangeMean = np.array([np.mean(xMin), np.mean(xMax)])
        yRangeMean = np.array([np.mean(yMin), np.mean(yMax)])
        self.setMeanCalibration(np.array([np.mean(xRangeMean), np.mean(yRangeMean)]))

        rangeXReal, rangeYReal = Calibration.rangePos(self.positionsCalibration)
        ratio = np.append(np.diff(rangeXReal) / np.diff(xRangeMean), np.diff(rangeYReal) / np.diff(yRangeMean))
        self.setRatioCalibration(ratio)
        self.setCentersPupilCalibration(self.calibrationApply())


    @QtCore.pyqtSlot(str)
    def load(self, name):
        if path.exists(name[7:]):
            tree = etree.parse(name[7:])
            root = tree.getroot()
            super(Calibration, self).loadApply(root)
            for calibrationSection in root.findall('CalibrationSections/CalibrationSection'):
                self.sectionCalibration[calibrationSection.attrib['name']] = CalibrationSection().loadApply(calibrationSection)
            EnvVariable.instance.setFileCalibration(name)
            self.setCentersPupilCalibration(self.calibrationApply())


    @QtCore.pyqtSlot(str)
    def save(self, name):
        envVariable = super(Calibration, self).save(None)
        sections = etree.SubElement(envVariable, "CalibrationSections")
        for sectionCalibration in self.sectionCalibration:
            section = etree.SubElement(sections, "CalibrationSection")
            section.set("name", sectionCalibration)
            self.sectionCalibration[sectionCalibration].saveApply(section)
        Variable.writeData(name, envVariable)
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
        print(data)
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
        x = np.convolve(self.centersPupil[:,0], np.full(self._frameMean, 1 / self._frameMean), mode='valid')
        y = np.convolve(self.centersPupil[:,1], np.full(self._frameMean, 1 / self._frameMean), mode='valid')
        u = np.empty((len(x),2), float)
        u[:,0] = x
        u[:,1] = y
        e = (u-self._meanCalibration)*(self._ratioCalibration/np.array([self.width, self.height]))
        return e

    def calibrationApplyClient(self, centersPupil):
        u = np.array([np.mean(centersPupil, axis=0)])
        print((u - self._meanCalibration))
        e = (u - self._meanCalibration) * self._ratioCalibration
        return e

    @QtCore.pyqtSlot()
    def plot(self):
        calibrationValue = self.calibrationApply()*np.array([self.width, self.height])

        fig, (ax1, ax2) = plt.subplots(2,1)
        ax1.plot(self.centersPupil[:, 0],'b', label='X')
        ax3 = ax1.twinx()
        ax3.plot(self.centersPupil[:, 1], 'r', label='Y')
        ax1.set_title('Pupils Center')

        ax2.plot(calibrationValue[:,0],'b', label='X')
        ax2.plot(calibrationValue[:,1],'r', label='Y')
        ax2.plot(self.positionsCalibration[:, 0], 'g', label='X Screen')
        ax2.plot(self.positionsCalibration[:, 1], 'm', label='Y Screen')
        ax2.set_title('Gaze estimation')

        for calibrationSection in self.sectionCalibration:
            xMin = self.sectionCalibration[calibrationSection].indexXMin
            xMax = self.sectionCalibration[calibrationSection].indexXMax
            mean = self.sectionCalibration[calibrationSection].mean
            variance = self.sectionCalibration[calibrationSection].variance
            ax1.text((xMin+xMax)/2, max(self.centersPupil[:, 0]), calibrationSection, horizontalalignment='center', fontsize=8)
            ax1.axvline(x=xMin)
            ax2.text((xMin + xMax) / 2, max(calibrationValue[:, 0]), calibrationSection, horizontalalignment='center',fontsize=8)
            ax2.axvline(x=xMin)
            ax1.axvline(x=xMax)
            ax1.plot((xMin+xMax)/2, mean[0], 'go')
            ax3.plot((xMin+xMax)/2, mean[1], 'go')
            ax1.errorbar((xMin+xMax)/2, mean[0], variance[0])
            ax3.errorbar((xMin + xMax) / 2, mean[1], variance[1])

        ax3.legend('mean')
        for ax in ax1, ax2, ax3:
            ax.set(xlabel='Frame', ylabel='Amplitude (Pixel)')
            ax.legend()

        plt.show()
