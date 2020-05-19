import QtQuick 2.0
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Item {
    id:ent1
    objectName:"ent1"
    Rectangle{
        anchors.top: parent.top
        anchors.horizontalCenter : parent.horizontalCenter
        height:95
        width : 1340
        opacity : 0.9
        color:applicationWindow.color
        GroupBox {
            anchors.fill:parent
            title: "Optimization"
            RowLayout {
                GroupBox {
                    title: "ZoomX"
                    RowLayout {
                        anchors.fill: parent
                        Slider {
                            id:zoomXSlider
                            from: eyeTrackingVariable.zoomXMax/10
                            value: eyeTrackingVariable.zoomX
                            to: eyeTrackingVariable.zoomXMax
                            onMoved : eyeTrackingVariable.zoomX = zoomXSlider.value
                        }
                        SpinBox {
                            id:zoomXSpinBox
                            from: eyeTrackingVariable.zoomXMax/10
                            value: eyeTrackingVariable.zoomX
                            to: 1280
                            width : eyeTrackingVariable.zoomXMax
                            onValueModified : eyeTrackingVariable.zoomX = zoomXSpinBox.value
                        }
                    }
                }
                GroupBox {
                    title: "ZoomY"
                    RowLayout {
                        anchors.fill: parent
                        Slider {
                            id:zoomYSlider
                            from: eyeTrackingVariable.zoomYMax/10
                            value: eyeTrackingVariable.zoomY
                            to: eyeTrackingVariable.zoomYMax
                            onMoved : eyeTrackingVariable.zoomY = zoomYSlider.value
                        }
                        SpinBox {
                            id:zoomYSpinBox
                            from: eyeTrackingVariable.zoomYMax/10
                            value: eyeTrackingVariable.zoomY
                            to: eyeTrackingVariable.zoomYMax
                            onValueModified : eyeTrackingVariable.zoomY = zoomYSpinBox.value
                        }
                    }
                }
                GroupBox {
                    title: "X"
                    RowLayout {
                        anchors.fill: parent
                        Slider {
                            id:xSlider
                            from: -(eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX)
                            value: eyeTrackingVariable.posZoomX
                            to: eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX
                            onMoved : eyeTrackingVariable.posZoomX = xSlider.value
                        }
                        SpinBox {
                            id:xSpinBox
                            from: -(eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX)
                            value: eyeTrackingVariable.posZoomX
                            to: eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX
                            onValueModified : eyeTrackingVariable.posZoomX = xSpinBox.value
                        }
                    }
                }
                GroupBox {
                    title: "Y"
                    RowLayout {
                        anchors.fill: parent
                        Slider {
                            id:ySlider
                            from: -(eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY)
                            value: eyeTrackingVariable.posZoomY
                            to: eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY
                            onMoved : eyeTrackingVariable.posZoomY = ySlider.value
                        }
                        SpinBox {
                            id:ySpinBox
                            from: -(eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY)
                            value: eyeTrackingVariable.posZoomY
                            to: eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY
                            onValueModified : eyeTrackingVariable.posZoomY = ySpinBox.value
                        }
                    }
                }
                GroupBox {
                    title: "Eye detection"
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    RowLayout {
                        anchors.fill:parent
                        CheckBox {
                            text:"Left eye"
                            checked: eyeTrackingVariable.selectEye & 1
                            onClicked:eyeTrackingVariable.selectEye = 0
                        }
                        CheckBox{
                            text:"Right eye"
                            checked: (eyeTrackingVariable.selectEye >> 1) & 1
                            onClicked:eyeTrackingVariable.selectEye = 1
                        }
                    }
                }
            }
        }
    }

    Rectangle{
        anchors.right: parent.right
        anchors.verticalCenter : parent.verticalCenter
        height:405
        width : 100
        opacity : 0.9
        color:applicationWindow.color
        ModeView{
        anchors.fill:parent
        }
    }

     Rectangle{
        anchors.bottom: param.top
        anchors.horizontalCenter : parent.horizontalCenter
        height:60
        width : 570
        opacity : 0.9
        color:applicationWindow.color
        RowLayout {
        GroupBox {
                title: "Left Threshold"
                RowLayout {
                    Slider {
                        id:leftThresholdRangeSlider
                        from: 0
                        to: 255
                        value: eyeTrackingVariable.leftThreshold
                        onMoved:eyeTrackingVariable.leftThreshold = leftThresholdRangeSlider.value
                    }
                    SpinBox {
                        id:leftThresholdSpinBox
                        from: 0
                        value: eyeTrackingVariable.leftThreshold
                        to: 255
                        onValueModified : eyeTrackingVariable.leftThreshold = leftThresholdSpinBox.value
                    }
                }
            }
            GroupBox {
                title: "Right Threshold"
                RowLayout {
                    Slider {
                        id:rightThresholdRangeSlider
                        from: 0
                        to: 255
                        value: eyeTrackingVariable.rightThreshold
                        onMoved:eyeTrackingVariable.rightThreshold = rightThresholdRangeSlider.value
                    }
                    SpinBox {
                        id:rightThresholdSpinBox
                        from: 0
                        value: eyeTrackingVariable.rightThreshold
                        to: 255
                        onValueModified : eyeTrackingVariable.rightThreshold = rightThresholdSpinBox.value
                    }
                }
            }
            }
    }

    Rectangle{
    anchors.bottom : parent.bottom
    anchors.horizontalCenter : parent.horizontalCenter
    height : 95
    id:param
    opacity : 0.9
    width : 1090
    color : applicationWindow.color
     RowLayout {
        id : test
                anchors.fill:parent
                 Button{
                  Image {
        anchors.fill: parent
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        source: "../Resources/Images/import.svg"
    }
                id:loadButton
                anchors.left:test.left
                anchors.leftMargin: 20
                anchors.topMargin: 20
                anchors.bottomMargin: 20
                anchors.top:parent.top
                anchors.bottom:parent.bottom
                width:height
                onClicked: fileDialogLoad.visible=true
            }
    GroupBox {
        id : propertieGroupBox
        title: "Properties"
        anchors.leftMargin: 20
        anchors.left:loadButton.right
        RowLayout {
            anchors.fill:parent
            GroupBox {
                title: "Size"
                RowLayout {
                   RangeSlider {
                        id:minMaxSizeRangeSlider
                        from: 0
                        to: 500
                        first.value: eyeTrackingVariable.minSize
                        second.value: eyeTrackingVariable.maxSize
                        first.onMoved:eyeTrackingVariable.minSize = minMaxSizeRangeSlider.first.value
                        second.onMoved:eyeTrackingVariable.maxSize = minMaxSizeRangeSlider.second.value
                   }
                   SpinBox {
                       id:minSizeSpinBox
                       from: 0
                       value: eyeTrackingVariable.minSize
                       to: 500
                       onValueModified : eyeTrackingVariable.minSize = thresholdSpinBox.value
                   }
                   SpinBox {
                       id:maxSizeSpinBox
                       from: 0
                       value: eyeTrackingVariable.maxSize
                       to: 500
                       onValueModified : eyeTrackingVariable.maxSize = thresholdSpinBox.value
                   }
                }
            }
            GroupBox {
                title: "Scale Factor"
                RowLayout {
                    anchors.fill: parent
                    Slider {
                        id:scale_factorSlider
                        from: 13
                        value: eyeTrackingVariable.scale_factor
                        to: 30
                        onMoved : eyeTrackingVariable.scale_factor = scale_factorSlider.value
                    }
                    SpinBox {
                        id:scale_factorSpinBox
                        from: 13
                        value: eyeTrackingVariable.scale_factor
                        to: 30
                        onValueModified : eyeTrackingVariable.scale_factor = scale_factorSpinBox.value
                    }
                }
            }
            GroupBox {
                title: "Min Neighbors"
                RowLayout {
                    anchors.fill: parent
                    Slider {
                        id:min_neighborsSlider
                        from: 5
                        value: eyeTrackingVariable.min_neighbors
                        to: 10
                        onMoved : eyeTrackingVariable.min_neighbors = min_neighborsSlider.value
                    }
                    SpinBox {
                        id:min_neighborsSpinBox
                        from: 5
                        value: eyeTrackingVariable.min_neighbors
                        to: 10
                        onValueModified : eyeTrackingVariable.min_neighbors = min_neighborsSpinBox.value
                    }
                }
            }
            }

            }
 Button{
   Image {
        anchors.fill: parent
        anchors.topMargin: 10
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        source: "../Resources/Images/Save.svg"
    }
 anchors.left:propertieGroupBox.right
                anchors.top:parent.top
                anchors.bottom:parent.bottom
                anchors.leftMargin: 20
                anchors.topMargin: 20
                anchors.rightMargin: 20
                anchors.bottomMargin: 20
                width:height
                onClicked: fileDialogSave.visible=true
            }
           }





    }
}