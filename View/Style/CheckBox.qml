import QtQuick 2.12
import QtQuick.Controls 2.12

CheckBox {
    id: control

    indicator: Rectangle {
        implicitWidth: 26
        implicitHeight: 26
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 3
        border.color: Style.blue2
        border.width:3
        color:Style.b1

        Rectangle {
            width: 14
            height: 14
            x: 6
            y: 6
            radius: 2
            color: Style.blue2
            visible: control.checked
        }
    }

    contentItem: Text {
        text: control.text
        font: control.font
        opacity: enabled ? 1.0 : 0.3
        color: Style.white
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + control.spacing
    }
}