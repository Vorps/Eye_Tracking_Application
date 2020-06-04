import QtQuick 2.12
import QtQuick.Controls 2.12
import "."
SpinBox {
    id: control
    value:10
    contentItem: TextInput {
        x:parent.width/2
        text: control.textFromValue(control.value, control.locale)
        font: control.font
        color: Style.white
    }

    up.indicator: Rectangle {
        x: parent.width-width-5
        height: parent.height
        implicitWidth: 20
        implicitHeight: 20
             color: "transparent"

        Text {
            text: ">"
            font.pixelSize: control.font.pixelSize * 2
            color: Style.white
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    down.indicator: Rectangle {
        x: 0
        height: parent.height
        implicitWidth: 20
        implicitHeight: 20
        color: "transparent"

        Text {
            text: "<"
            font.pixelSize: control.font.pixelSize * 2
            color: Style.white
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    background: Rectangle {
        implicitWidth: 50
        color: Style.b1
    }
}