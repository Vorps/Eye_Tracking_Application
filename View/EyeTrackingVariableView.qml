import QtQuick 2.0
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

Item {
    id:ent1
    objectName:"ent1"
    Rectangle{
        anchors.top: parent.top
        anchors.horizontalCenter : parent.horizontalCenter
        height:130
        width : 1220
        opacity : 0.9
        color:applicationWindow.color
        GroupBox {
            title: "Optimization"
            RowLayout {
 GroupBox {
 title: "Zoom"
  RowLayout {
                        SpinBox {
                            label:"ZoomX"
                            id:zoomXSpinBox
                            from: eyeTrackingVariable.zoomXMax/10
                            value: eyeTrackingVariable.zoomX
                            to: eyeTrackingVariable.zoomXMax
                            width : eyeTrackingVariable.zoomXMax
                            onValueChanged : eyeTrackingVariable.zoomX = zoomXSpinBox.value
                        }
                        SpinBox {
                            label: "ZoomY"
                            id:zoomYSpinBox
                            from: eyeTrackingVariable.zoomYMax/10
                            value: eyeTrackingVariable.zoomY
                            to: eyeTrackingVariable.zoomYMax
                            onValueChanged : eyeTrackingVariable.zoomY = zoomYSpinBox.value
                        }
                        SpinBox {
                            label:"X"
                            id:xSpinBox
                            from: -(eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX)
                            value: eyeTrackingVariable.posZoomX
                            to: eyeTrackingVariable.zoomXMax-eyeTrackingVariable.zoomX
                            onValueChanged : eyeTrackingVariable.posZoomX = xSpinBox.value
                        }
                        SpinBox {
                            label:"Y"
                            id:ySpinBox
                            from: -(eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY)
                            value: eyeTrackingVariable.posZoomY
                            to: eyeTrackingVariable.zoomYMax-eyeTrackingVariable.zoomY
                            onValueChanged : eyeTrackingVariable.posZoomY = ySpinBox.value
                        }
}
}
                GroupBox {
                    title: "Eye detection"
                    RowLayout {
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
        height:630
        width : 120
        opacity : 0.9
        color:applicationWindow.color
        ModeView{
        anchors.fill:parent
        }
    }

     Rectangle{
        anchors.bottom: param.top
        anchors.horizontalCenter : parent.horizontalCenter
        height:50
        width : 490
        opacity : 0.9
        color:applicationWindow.color
        RowLayout {
            y:10
x:10
                    SpinBox {
                         label:"Left Threshold"
                        id:leftThresholdSpinBox
                        from: 0
                        value: eyeTrackingVariable.leftThreshold
                        to: 255
                        onValueChanged : eyeTrackingVariable.leftThreshold = leftThresholdSpinBox.value

                    }

                    SpinBox {
                        label:"Right Threshold"
                        id:rightThresholdSpinBox
                        from: 0
                        value: eyeTrackingVariable.rightThreshold
                        to: 255
                        onValueChanged : eyeTrackingVariable.rightThreshold = rightThresholdSpinBox.value
                    }


        }
    }

    Rectangle{
    anchors.bottom : parent.bottom
    anchors.horizontalCenter : parent.horizontalCenter
    height : 82
    id:param
    opacity : 0.9
    width : 1130
    color : applicationWindow.color
     RowLayout {
            id : test
                anchors.fill:parent
                anchors.leftMargin:20
                 Button{
                    icon.source: "../Resources/Images/import.svg"
                    id:loadButton
                    width:height
                    onClicked: fileDialogLoad.visible=true
            }
    GroupBox {
        id : propertieGroupBox
        title: "Properties"
        anchors.left:loadButton.right
        anchors.leftMargin:20
        RowLayout {
            anchors.fill:parent
            SpinBox {
                        label:"Min Size"
                        id:minSizeSpinBox
                        from: 0
                        value: eyeTrackingVariable.minSize
                        to: eyeTrackingVariable.maxSize
                        onValueChanged : eyeTrackingVariable.minSize = minSizeSpinBox.value
                    }
            SpinBox {
                        label:"Max Size"
                        id:maxSizeSpinBox
                        from: eyeTrackingVariable.minSize
                        value: eyeTrackingVariable.maxSize
                        to: 500
                        onValueChanged : eyeTrackingVariable.maxSize = maxSizeSpinBox.value
                    }

                    SpinBox {
                        label:"Scale Factor"
                        id:scale_factorSpinBox
                        from: 13
                        value: eyeTrackingVariable.scale_factor
                        to: 30
                        onValueChanged : eyeTrackingVariable.scale_factor = scale_factorSpinBox.value
                    }

                    SpinBox {
                        label: "Min Neighbors"
                        id:min_neighborsSpinBox
                        from: 5
                        value: eyeTrackingVariable.min_neighbors
                        to: 10
                        onValueChanged : eyeTrackingVariable.min_neighbors = min_neighborsSpinBox.value
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