import QtQuick 2.12
import QtQuick.Controls 2.12
import "."
import QtQuick.Layouts 1.14

SpinBox {
    property string label: ""
    id: control
    contentItem:
         Rectangle {
            implicitWidth: 180
            implicitHeight: 20
            color:"transparent"
             Text {
                    y:-15
                    text: control.label+" Value : "+control.textFromValue(control.value, control.locale)
                    font: control.font
                    color: Style.white
            }
                Slider {
                    id: control1
                    from:control.from
                    to:control.to
                    value:control.value
                    background: Rectangle {
                        x: control1.leftPadding
                        y: control.availableHeight / 2 - height / 2
                        implicitWidth: 180
                        implicitHeight: 6
                        width: control1.availableWidth
                        height: implicitHeight
                        radius: 3
                        color: Style.gray
                        Rectangle {
                            width: control1.visualPosition * parent.width
                            height: parent.height
                            color: Style.blue
                            radius: 2
                        }
                    }
                    onMoved:control.value=control1.value
                    handle: Rectangle {
                        x: control1.leftPadding + control1.visualPosition * (control1.availableWidth - width)
                        y: control.availableHeight / 2 - height / 2
                        implicitWidth: 20
                        implicitHeight: 20
                        radius: 10
                        color: Style.blue1
                        border.color: Style.gray
                    }
            }
        }


    up.indicator: Rectangle {
        x: control.mirrored ? 0 : parent.width - width
        height: parent.height
        color: "transparent"
        implicitWidth: 20
        implicitHeight: 30

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
        x: control.mirrored ? parent.width - width : 0
        height: parent.height
        color: "transparent"
        implicitWidth: 20
        implicitHeight: 38
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
        implicitWidth: 40
        color: "transparent"
    }
}