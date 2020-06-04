import QtQuick 2.14
import QtQuick.Controls 2.14
import "."

    Button {
        id: button
        contentItem: Item{}
        background: Rectangle {
            implicitWidth: 40
            implicitHeight: 40
            color: button.down ?  Style.b1 : Style.b2
            border.color: Style.blue2
            border.width: 1
            radius: 4
              Image {
                anchors.fill:parent
                anchors.leftMargin: 10
anchors.topMargin: 10
anchors.bottomMargin: 10
anchors.rightMargin: 10
                source: button.icon.source
            }
        }
    }
