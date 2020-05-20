import QtQuick 2.12
import QtQuick.Controls 2.12
import "."
GroupBox {
    id: control

    background: Rectangle {

        y:0
        anchors.topMargin:0
        width: parent.width
        color: "transparent"
        border.color: Style.gray
        radius: 2
    }

    label: Text {

        x: control.leftPadding
        y :0
        width: control.availableWidth
        text: control.title
        color: Style.white
        elide: Text.ElideRight
    }


}