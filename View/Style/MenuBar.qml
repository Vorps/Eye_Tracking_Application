import QtQuick 2.12
import QtQuick.Controls 2.12
import "."
MenuBar {
    id: menuBar

    delegate: MenuBarItem {
        id: menuBarItem

        contentItem: Text {
            text: menuBarItem.text
            font: menuBarItem.font
            opacity: enabled ? 1.0 : 0.3
            color: "white"
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: 40
            implicitHeight: 25
            opacity: enabled ? 1 : 0.3
            color: menuBarItem.highlighted ? Style.b1 : "transparent"
        }
    }

    background: Rectangle {
        implicitWidth: 40
        implicitHeight: 30
        color: Style.blue1

        Rectangle {
            color: Style.b1
            width: parent.width
            height: 1
            anchors.bottom: parent.bottom
        }
    }
}