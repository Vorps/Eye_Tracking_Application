import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Item {
    Rectangle{
        id:mouseItem
        anchors.fill: parent
        color: "white"
        opacity: 0.5
        Grid {
            columns: mouseControl.column
            Repeater {
                id:gridRepeater
                model: mouseControl.column*mouseControl.row
                Rectangle {
                    width:mouseItem.width/mouseControl.column
                    height:mouseItem.height/mouseControl.row
                    border.width: 2
                    color: "transparent"
                    property int time:0
                    Text{
                        text:parent.time
                    }
                }
            }
        }
        Rectangle{
            id : mouseControlParameter
            anchors.bottom: parent.bottom
            anchors.horizontalCenter : parent.horizontalCenter
            height:95
            width : 800
            opacity : 0.9
            color:applicationWindow.color
            RowLayout {
                CheckBox{
                    text:"Speed color"
                    checked:true
                }
                GroupBox {
                    title: "Row Number"
                    RowLayout {
                        Slider {
                            id:rowSlider
                            from: 1
                            to: 10
                            value: mouseControl.row
                            onMoved:mouseControl.row = rowSlider.value
                        }
                        SpinBox {
                            id:rowSpinBox
                            from: 1
                            value: mouseControl.row
                            to: 10
                            onValueModified : mouseControl.row = rowSpinBox.value
                        }
                    }
                }
                GroupBox {
                    title: "Column Number"
                    RowLayout {
                        Slider {
                            id:columnSlider
                            from: 1
                            to: 10
                            value: mouseControl.column
                            onMoved:mouseControl.column = columnSlider.value
                        }
                        SpinBox {
                            id:columnSpinBox
                            from: 1
                            value: mouseControl.column
                            to: 10
                            onValueModified : mouseControl.column = columnSpinBox.value
                        }
                    }
                }
            }
        }
        property int zone: 0
        property int lastX: 0

        Timer {
            interval: 25
            running: true
            repeat: true
            onTriggered: {
                gridRepeater.itemAt(mouseItem.zone).time = gridRepeater.itemAt(mouseItem.zone).time+500
                cible.color = Qt.rgba((Math.abs(areaTest.mouseX-mouseItem.lastX))/100,0.5, 0.5, 1)
                mouseItem.lastX = areaTest.mouseX
            }
        }

         MouseArea {
            id : areaTest
            anchors.left:parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: mouseControlParameter.top
            focus:true
            onPressed:{
                var row = Math.floor(mouseY*mouseControl.row/mouseItem.height)
                var column = Math.floor(mouseX*mouseControl.column/mouseItem.width)
                mouseItem.zone = row*mouseControl.column+column
            }
        }
        Text{
            anchors.bottom:parent.bottom
            text:mouseItem.zone
        }
        Rectangle{
            id:cible
            height:50
            width:50
            radius:25
            color:"red"
            x:mouseControl.posMouse.x+parent.width/2
            y:mouseControl.posMouse.y+parent.height/2
            onXChanged:{
            }
            onYChanged:{
            }
        }
    }

}