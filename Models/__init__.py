from PyQt5 import QtQml
from .cvCapture import CVCapture,CVImage
from .variable import EyeTrackingVariable, EnvVariable
from .calibration import Calibration
from .mouseControl import MouseControl

def registerTypes(uri = "Models"):
    QtQml.qmlRegisterType(CVCapture, uri, 1, 0, "CVCapture")
    QtQml.qmlRegisterType(CVImage, uri, 1, 0, "CVImage")
    QtQml.qmlRegisterType(EyeTrackingVariable, uri, 1, 0, "EyeTrackingVariable")
    QtQml.qmlRegisterType(EnvVariable, uri, 1, 0, "EnvVariable")
    QtQml.qmlRegisterType(MouseControl, uri, 1, 0, "MouseControl")
    QtQml.qmlRegisterType(Calibration, uri, 1, 0, "Calibration")