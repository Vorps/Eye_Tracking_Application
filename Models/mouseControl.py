from PyQt5 import QtCore
from PyQt5.QtCore import QPointF
import numpy as np

from EyesTracking.eyeTracking import EyeTrackingClient
from Models.calibration import Calibration

class MouseControl(EyeTrackingClient):
    instance = None
    posMouseChange = QtCore.pyqtSignal()
    rowChange = QtCore.pyqtSignal()
    columnChange = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MouseControl, self).__init__(parent)
        self._posMouse = np.empty((0, 2), int)
        MouseControl.instance = self
        self.filter = True
        self._column = 2
        self._row = 2
        self.setBuffer(3)

    def setposMouse(self, posMouse):
        self._posMouse = posMouse
        self.posMouseChange.emit()

    def update(self, centerPupil):
        super(MouseControl, self).update(centerPupil)
        self.setposMouse(Calibration.instance.calibrationApply())

    def setColumn(self, column):
        if self._column == column: return
        self._column = column
        self.columnChange.emit()

    @QtCore.pyqtProperty(int, fset=setColumn, notify=columnChange)
    def column(self):
        return self._column

    def setRow(self, row):
        if self._row  == row: return
        self._row = row
        self.rowChange.emit()

    @QtCore.pyqtProperty(int, fset=setRow, notify=rowChange)
    def row(self):
        return self._row

    @QtCore.pyqtProperty("QPointF", fset=setposMouse, notify=posMouseChange)
    def posMouse(self):
        return QPointF(*self._posMouse)
