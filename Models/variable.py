import os.path as path
from abc import abstractmethod
import numpy as np

from lxml import etree
from PyQt5 import QtCore

class Variable(QtCore.QObject):

    def __init__(self, parent=None):
        super(Variable, self).__init__(parent)
        self.blackList = []

    def setBlackList(self, blacklist):
        self.blackList = blacklist

    @QtCore.pyqtSlot(str)
    def load(self, name):
        if path.exists(name[7:]):
            tree = etree.parse(name[7:])
            root = tree.getroot()
            for child in root:
                if child.attrib['type'] == "int":
                    setattr(self, child.tag, int(child.attrib['data']))
                elif child.attrib['type'] == "ndarray":
                    value = child.attrib['data']
                    setattr(self, child.tag, np.fromstring(value[1:-1], dtype=float, sep=' '))
                else:
                    setattr(self, child.tag, child.attrib['data'])
                if child.tag[1:]+"Change" in dir(self):
                    self.__getattribute__(child.tag[1:]+"Change").emit()
            return True
        else:
            self.reset()
            return False

    @QtCore.pyqtSlot(str)
    def save(self, name):
        envVariable = etree.Element(type(self).__name__)
        for property, value in vars(self).items():
            if property not in self.blackList and property != "blackList":
                Variable.setData(envVariable, property, value)
        Variable.writeData(name, etree.tostring(envVariable))

    @abstractmethod
    def reset(self):
        pass

    def setData(envVariable, propertie, data):
        element = etree.SubElement(envVariable, propertie)
        element.set("data", str(data))
        element.set("type", str(type(data).__name__))

    def writeData(name, data):
        output_file = open(name[7:], 'wb')
        output_file.write(data)
        output_file.close()


class EyeTrackingVariable(Variable):
    instance = None

    scale_factorChange = QtCore.pyqtSignal()
    min_neighborsChange = QtCore.pyqtSignal()
    minSizeChange = QtCore.pyqtSignal()
    maxSizeChange = QtCore.pyqtSignal()
    leftThresholdChange = QtCore.pyqtSignal()
    rightThresholdChange = QtCore.pyqtSignal()
    posZoomXChange = QtCore.pyqtSignal()
    posZoomYChange = QtCore.pyqtSignal()
    zoomXChange = QtCore.pyqtSignal()
    zoomYChange = QtCore.pyqtSignal()
    zoomXMaxChange = QtCore.pyqtSignal()
    zoomYMaxChange = QtCore.pyqtSignal()
    selectEyeChange = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(EyeTrackingVariable, self).__init__(parent)
        self._scale_factor = None
        self._min_neighbors = None
        self._minSize = None
        self._maxSize = None
        self._leftThreshold = None
        self._rightThreshold = None
        self._posZoomX = None
        self._posZoomY = None
        self._zoomXMax = 0
        self._zoomYMax = 0
        self._zoomX = 0
        self._zoomY = 0
        self._selectEye = None
        EyeTrackingVariable.instance = self
        self.load(EnvVariable.instance.getFileEyeTrackingVariable())

    @QtCore.pyqtSlot()
    def reset(self):
        self.setScale_factor(13)
        self.setMin_neighbors(5)
        self.setMinSize(0)
        self.setMaxSize(400)
        self.setLeftThreshold(25)
        self.setRightThreshold(25)
        self._zoomX = self._zoomXMax
        self._zoomY = self._zoomYMax
        self._posZoomX = 0
        self._posZoomY = 0
        self._selectEye = 3
        self.selectEyeChange.emit()
        self.zoomXChange.emit()
        self.zoomYChange.emit()
        self.posZoomXChange.emit()
        self.posZoomYChange.emit()

    @QtCore.pyqtSlot(str)
    def load(self, name):
        if super(EyeTrackingVariable, self).load(name):
            EnvVariable.instance.setFileEyeTrackingVariable(name)

    @QtCore.pyqtSlot(str)
    def save(self, name):
        super(EyeTrackingVariable, self).save(name)
        EnvVariable.instance.setFileEyeTrackingVariable(name)

    def setScale_factor(self, scale_factor):
        if self._scale_factor == scale_factor: return
        self._scale_factor = scale_factor
        self.scale_factorChange.emit()

    @QtCore.pyqtProperty(int, fset=setScale_factor, notify=scale_factorChange)
    def scale_factor(self):
        return self._scale_factor

    def setMin_neighbors(self, min_neighbors):
        if self._min_neighbors == min_neighbors: return
        self._min_neighbors = min_neighbors
        self.min_neighborsChange.emit()

    @QtCore.pyqtProperty(int, fset=setMin_neighbors, notify=min_neighborsChange)
    def min_neighbors(self):
        return self._min_neighbors

    def setMinSize(self, minSize):
        if self._minSize == minSize: return
        self._minSize = minSize
        self.minSizeChange.emit()

    @QtCore.pyqtProperty(int, fset=setMinSize, notify=minSizeChange)
    def minSize(self):
        return self._minSize

    def setMaxSize(self, maxSize):
        if self._maxSize == maxSize: return
        self._maxSize = maxSize
        self.maxSizeChange.emit()

    @QtCore.pyqtProperty(int, fset=setMaxSize, notify=maxSizeChange)
    def maxSize(self):
        return self._maxSize

    def setLeftThreshold(self, leftThreshold):
        if self._leftThreshold == leftThreshold: return
        self._leftThreshold = leftThreshold
        self.leftThresholdChange.emit()

    @QtCore.pyqtProperty(int, fset=setLeftThreshold, notify=leftThresholdChange)
    def leftThreshold(self):
        return self._leftThreshold

    def setRightThreshold(self, rightThreshold):
        if self._rightThreshold == rightThreshold: return
        self._rightThreshold = rightThreshold
        self.rightThresholdChange.emit()

    @QtCore.pyqtProperty(int, fset=setRightThreshold, notify=rightThresholdChange)
    def rightThreshold(self):
        return self._rightThreshold

    def setPosZoomX(self, posZoomX):
        if int(self._zoomXMax / 2) + self._posZoomX - int(self._zoomX / 2) < 0:
            self._posZoomX = -int(self._zoomXMax / 2) + int(self._zoomX / 2)
        elif int(self._zoomXMax / 2) + self._posZoomX + int(self._zoomX / 2) > self._zoomXMax:
            self._posZoomX = int(self._zoomXMax / 2) - int(self._zoomX / 2)
        else:
            self._posZoomX = posZoomX
        self.posZoomXChange.emit()

    @QtCore.pyqtProperty(int, fset=setPosZoomX, notify=posZoomXChange)
    def posZoomX(self):
        return self._posZoomX

    def setPosZoomY(self, posZoomY):
        if int(self._zoomYMax / 2) + self._posZoomY - int(self._zoomY / 2) < 0:
            self._posZoomY = -int(self._zoomYMax / 2) + int(self._zoomY / 2)
        elif int(self._zoomYMax / 2) + self._posZoomY + int(self._zoomY / 2) > self._zoomYMax:
            self._posZoomY = int(self._zoomYMax / 2) - int(self._zoomY / 2)
        else:
            self._posZoomY = posZoomY
        self.posZoomYChange.emit()

    @QtCore.pyqtProperty(int, fset=setPosZoomY, notify=posZoomYChange)
    def posZoomY(self):
        return self._posZoomY

    def setZoomX(self, zoomX):
        if zoomX <= 0: return
        if zoomX > self.zoomXMax:
            self._zoomX = self.zoomXMax
        else:
            self._zoomX = zoomX
        self.zoomXChange.emit()
        if int(self._zoomXMax / 2) + self._posZoomX - int(self._zoomX / 2) < 0:
            self.setPosZoomX(-int(self._zoomXMax / 2) + int(self._zoomX / 2))
        elif int(self._zoomXMax / 2) + self._posZoomX + int(self._zoomX / 2) > self._zoomXMax:
            self.setPosZoomX(int(self._zoomXMax / 2) - int(self._zoomX / 2))

    @QtCore.pyqtProperty(int, fset=setZoomX, notify=zoomXChange)
    def zoomX(self):
        return self._zoomX

    def setZoomY(self, zoomY):
        if zoomY <= 0: return
        if zoomY > self.zoomYMax:
            self._zoomY = self.zoomYMax
        else:
            self._zoomY = zoomY
        self.zoomYChange.emit()

        if int(self._zoomYMax / 2) + self._posZoomY - int(self._zoomY / 2) < 0:
            self.setPosZoomY(-int(self._zoomYMax / 2) + int(self._zoomY / 2))
        elif int(self._zoomYMax / 2) + self._posZoomY + int(self._zoomY / 2) > self._zoomYMax:
            self.setPosZoomY(int(self._zoomYMax / 2) - int(self._zoomY / 2))

    @QtCore.pyqtProperty(int, fset=setZoomY, notify=zoomYChange)
    def zoomY(self):
        return self._zoomY

    def setZoomXMax(self, zoomXMax):
        if zoomXMax != 0:
            self._zoomXMax = zoomXMax
            if self._zoomX == 0 or self._zoomX > self._zoomXMax:
                self.setZoomX(self._zoomXMax)
            self.zoomXMaxChange.emit()

    @QtCore.pyqtProperty(int, fset=setZoomXMax, notify=zoomXMaxChange)
    def zoomXMax(self):
        return self._zoomXMax

    def setZoomYMax(self, zoomYMax):
        if zoomYMax != 0:
            self._zoomYMax = zoomYMax
            if self._zoomY == 0 or self._zoomY > self._zoomYMax:
                self.setZoomY(self._zoomYMax)
            self.zoomYMaxChange.emit()

    @QtCore.pyqtProperty(int, fset=setZoomYMax, notify=zoomYMaxChange)
    def zoomYMax(self):
        return self._zoomYMax

    def setSelectEye(self, selectEye):
        self._selectEye ^= 1 << selectEye
        self.selectEyeChange.emit()

    @QtCore.pyqtProperty(int, fset=setSelectEye, notify=selectEyeChange)
    def selectEye(self):
        return self._selectEye


class EnvVariable(Variable):
    instance = None

    modeViewChange = QtCore.pyqtSignal()
    typeViewChange = QtCore.pyqtSignal()
    modeProcessChange = QtCore.pyqtSignal()
    indexChange = QtCore.pyqtSignal()
    infoChange = QtCore.pyqtSignal()
    calibrationLoadChange = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(EnvVariable, self).__init__(parent)
        self.setBlackList(['_info', '_calibrationLoad'])
        self._modeView = None
        self._modeProcess = None
        self._typeView = None
        self._selectEye = None
        self._fileEyeTrackingVariable = None
        self._fileCalibration = None
        self._info = {'Setup':'', 'Calibration':''}
        self._index = 0
        self._calibrationLoad = False
        self.load("1234567Data/EnvVariable/Default.xml")
        EnvVariable.instance = self

    def getFileEyeTrackingVariable(self):
        return self._fileEyeTrackingVariable

    def setFileEyeTrackingVariable(self, fileEyeTrackingVariable):
        self._fileEyeTrackingVariable = fileEyeTrackingVariable
        self.setInfo("Setup", fileEyeTrackingVariable.split('/')[-1][0:-4])

    def getCalibration(self):
        return self._fileCalibration

    def setFileCalibration(self, fileCalibration):
        self._fileCalibration = fileCalibration
        self.setInfo("Calibration", fileCalibration.split('/')[-1][0:-4])
        self.setCalibrationLoad(True)

    def reset(self):
        self.setModeView(1)
        self._modeProcess = 1
        self.setTypeView(1)
        self.setIndex(0)
        self.setInfo("Setup", "")
        self.setInfo("Calibration", "")
        self.setFileEyeTrackingVariable("1234567Data/EyeTrackingVariable/Default.xml")
        self.setFileCalibration("1234567Data/Calibration/Default.xml")

    def setModeView(self, modeView):
        if self._modeView == modeView: return
        self._modeView = modeView
        self.modeViewChange.emit()

    @QtCore.pyqtProperty(int, fset=setModeView, notify=modeViewChange)
    def modeView(self):
        return self._modeView

    def setIndex(self, index):
        if self._index == index: return
        self._index = index
        self.indexChange.emit()

    @QtCore.pyqtProperty(int, fset=setIndex, notify=indexChange)
    def index(self):
        return self._index

    def setTypeView(self, typeView):
        if self._typeView == typeView: return
        self._typeView = typeView
        self.typeViewChange.emit()

    @QtCore.pyqtProperty(int, fset=setTypeView, notify=typeViewChange)
    def typeView(self):
        return self._typeView

    def setModeProcess(self, modeProcess):
        self._modeProcess ^= 1 << modeProcess
        self.modeProcessChange.emit()

    @QtCore.pyqtProperty(int, fset=setModeProcess, notify=modeProcessChange)
    def modeProcess(self):
        return self._modeProcess

    def setCalibrationLoad(self, calibrationLoad):
        self._calibrationLoad = calibrationLoad
        self.calibrationLoadChange.emit()

    @QtCore.pyqtProperty(bool, notify=calibrationLoadChange)
    def calibrationLoad(self):
        return self._calibrationLoad

    def setInfo(self, key, info):
        self._info[key] = info
        self.infoChange.emit()

    @QtCore.pyqtProperty(str, notify=infoChange)
    def info(self):
        info = ""
        for key in self._info.keys():
            if self._info[key] != "":
                info += key+" : "+self._info[key]+"     "
        return info

    def permission(perm):
        def decorator(function):
            def new_function(*args, **kwargs):
                if EnvVariable.instance.modeProcess >> perm & 1:
                    function(*args, **kwargs)
            return new_function
        return decorator