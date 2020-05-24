import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

Item {
    ColumnLayout{
        anchors.fill: parent
        id:mouseItem
        Rectangle{
            Canvas {
                id: ciblecanvas
            anchors.fill: parent
                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset()
                    ctx.fillStyle = Qt.rgba(1, 0, 0, 1);
                    ctx.beginPath()
                    for(var i = 0; i < mouseControl.posMouse.length; i+=1){
                        var point = mouseControl.posMouse[i]
                        ctx.roundedRect(point.x+width/2, point.y+height/2,6,6,3,3)
                    }
                    ctx.fill()
                    var point = mouseControl.posMouse[mouseControl.posMouse.length-1]
                    var xMouse = point.x+width/2
                    var yMouse = point.y+height/2
                    if(yMouse > 0 && yMouse < parent.height && xMouse > 0 && xMouse < parent.width){
                        ctx.beginPath()
                        ctx.fillStyle = Qt.rgba(0, 1, 0, 1);
                        ctx.roundedRect(xMouse, yMouse,20,20,10,10)
                        ctx.fill()
                        var row = Math.floor(yMouse*mouseControl.row/mouseItem.height)
                        var column = Math.floor(xMouse*mouseControl.column/mouseItem.width)
                        mouseItem.zone = row*mouseControl.column+column
                    }
                }
            }
            color: "white"
            opacity: 0.5
            anchors.fill: parent
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
                            color:'red'
                        }
                    }
                }
            }
        }

        Rectangle{
            id : mouseControlParameter
            anchors.bottom: parent.bottom
            anchors.horizontalCenter : parent.horizontalCenter
            height:50
            width : 600
            opacity : 0.9
            color:applicationWindow.color
            RowLayout {
            y:10
x:10
                CheckBox{
                    text:"Speed color"
                    checked:true
                }


                        SpinBox {
                            label:"Row Number"
                            id:rowSpinBox
                            from: 1
                            value: mouseControl.row
                            to: 10
                            onValueChanged : mouseControl.row = rowSpinBox.value
                        }



                        SpinBox {
                            label:"Column Number"
                            id:columnSpinBox
                            from: 1
                            value: mouseControl.column
                            to: 10
                            onValueChanged : mouseControl.column = columnSpinBox.value
                        }

            }
        }
        property int zone: 0
        property int lastX: 0
        property int lastY: 0
        Timer {
            interval: 25
            running: true
            repeat: true
            onTriggered: {
                gridRepeater.itemAt(mouseItem.zone).time = gridRepeater.itemAt(mouseItem.zone).time+25
                cible.color = Qt.rgba((Math.abs(cible.x-mouseItem.lastX))/10,0.5, 0.5, 1)
                mouseItem.lastX = cible.x
                mouseItem.lastY = cible.y
                ciblecanvas.requestPaint()
            }
        }

        Rectangle{
            id:cible
            height:50
            width:50
            radius:25
            color:"red"
            onXChanged:{
                if(x > 0 && x < parent.width){
                    var row = Math.floor(y*mouseControl.row/mouseItem.height)
                    var column = Math.floor(x*mouseControl.column/mouseItem.width)
                    mouseItem.zone = row*mouseControl.column+column
                }
            }
            onYChanged:{
                ciblecanvas.requestPaint()
                if(y>0 && y < parent.height){
                    ciblecanvas.requestPaint()
                    var row = Math.floor(y*mouseControl.row/mouseItem.height)
                    var column = Math.floor(x*mouseControl.column/mouseItem.width)
                    mouseItem.zone = row*mouseControl.column+column
                }
            }
        }
    }
}