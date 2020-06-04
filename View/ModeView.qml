import QtQuick 2.0
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

Item {
  ButtonGroup { id: radioGroup1 }
    ButtonGroup { id: radioGroup2 }
 ColumnLayout{

        id:typeView
    GroupBox {
        title: "Camera"
        anchors.left: parent.left
        anchors.right: parent.right
        CustomSpinBox{
            id:indexSpinBox
            x :10
            width:80
            from:0
            to:10
            value:envVariable.index
            onValueModified:{
                envVariable.index=indexSpinBox.value
                capture.start(indexSpinBox.index)
            }
        }
        }
    GroupBox {
        id:modeView
        title: "Mode View"
        anchors.left: parent.left
        anchors.right: parent.right
        ColumnLayout{
            CheckBox {
                text: "All"
                checked : envVariable.modeView == 1
                onClicked: envVariable.modeView = 1
                ButtonGroup.group: radioGroup1
            }
            CheckBox {
                text: "Face"
                checked : envVariable.modeView == 2
                onClicked: envVariable.modeView = 2
                ButtonGroup.group: radioGroup1
            }
            CheckBox {
                text: "Left eye"
                checked : envVariable.modeView == 3
                onClicked: envVariable.modeView = 3
                ButtonGroup.group: radioGroup1
            }
            CheckBox {
                text: "Right eye"
                checked : envVariable.modeView == 4
                onClicked: envVariable.modeView = 4
                ButtonGroup.group: radioGroup1
            }
            CheckBox {
                text: "Eyes"
                checked : envVariable.modeView == 5
                onClicked: envVariable.modeView = 5
                ButtonGroup.group: radioGroup1
            }
            CheckBox {
                text: "Zoom"
                checked : envVariable.modeView == 6
                onClicked: envVariable.modeView = 6
                ButtonGroup.group: radioGroup1
            }
        }
    }
    GroupBox {
        title : "Type View"
        anchors.left: parent.left
        anchors.right: parent.right
        ColumnLayout{
            CheckBox {
                text: "RGB"
                checked : envVariable.typeView == 1
                onClicked: envVariable.typeView = 1
                ButtonGroup.group: radioGroup2
            }
            CheckBox {
                text: "Gray"
                checked : envVariable.typeView == 2
                onClicked: envVariable.typeView = 2
                ButtonGroup.group: radioGroup2
            }
            CheckBox {
                text: "Treshold"
                checked : envVariable.typeView == 3
                onClicked: envVariable.typeView = 3
                ButtonGroup.group: radioGroup2
            }
        }
     }
}
         Button{
            icon.source:"../Resources/Images/Reset.svg"

            anchors.leftMargin: 20
            anchors.topMargin: 5
            anchors.bottomMargin: 5
            anchors.rightMargin: 20
            anchors.right:parent.right
            anchors.left:parent.left
            anchors.bottom:parent.bottom
            anchors.top:typeView.bottom
            height:width
            onClicked: eyeTrackingVariable.reset()

     }
}
