import QtQuick 2.12
import QtQuick.Controls 2.12
import "."
Menu {
    id: menu

    delegate: MenuItem {
        id: menuItem
        implicitWidth: 200
        implicitHeight: 30

        indicator: Item {
            implicitWidth: 40
            implicitHeight: 30
            Rectangle {
                width: 26
                height: 26
                anchors.centerIn: parent
                visible: menuItem.checkable
                        border.color: Style.blue2
        border.width:3
        color:Style.b1
                radius: 3
                Rectangle {
                    width: 14
                    height: 14
                    anchors.centerIn: parent
                    visible: menuItem.checked
                    color: Style.blue2
                    radius: 2
                }
            }
        }

        contentItem: Text {
            leftPadding: menuItem.indicator.width
            rightPadding: menuItem.arrow.width
            text: menuItem.text
            font: menuItem.font
            opacity: enabled ? 1.0 : 0.3
            color: Style.white
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: 150
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: menuItem.highlighted ? Style.blue1 : "transparent"
        }
    }

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 30
        color: Style.b1
        border.color: Style.gray
        radius: 2
    }
}