import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

Item {
    Rectangle{
        id:scenarioCalibration
        property int speed: 1000
        property real opacity1: 1
        property real opacity2: 0.1
        anchors.fill:parent
        color:'transparent'
        ColumnLayout{
            anchors.fill:parent
            Canvas {
                id: canvasCalibration
                height:parent.height
                width:parent.width
                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset();
                    ctx.fillStyle = Qt.rgba(200, 200, 200, scenarioCalibration.opacity1);
                    ctx.fillRect(0, 0, width, height)
                    ctx.fill()
                    ctx.lineWidth = 4
                    ctx.strokeStyle = Qt.rgba(0, 1, 0, scenarioCalibration.opacity2);
                    ctx.moveTo(40, 40)
                    ctx.lineTo(width-40, height-40)
                    ctx.moveTo(40, 40)
                    ctx.lineTo(width-40, 40)
                    ctx.moveTo(40, height-40)
                    ctx.lineTo(width-40, 40)
                    ctx.moveTo(40, height-40)
                    ctx.lineTo(width-40, height-40)
                    ctx.stroke()
                    ctx.fillStyle = Qt.rgba(1, 0, 0, scenarioCalibration.opacity1);
                    var meanLeft = calibration.meanCalibration
                    var ratioLeft = calibration.ratioCalibration
                    for(var i in calibration.centersPupilCalibration){
                        var point = calibration.centersPupilCalibration[i]
                        ctx.roundedRect(point.x+width/2, point.y+height/2,4,4,2,2)
                        ctx.fill()
                    }
                }
            }
            Rectangle{
                id: resultCalibration
                visible:false
                anchors.bottom: parent.bottom
                anchors.horizontalCenter : parent.horizontalCenter
                height: 95
                width : 600
                opacity : 0.8
                color:applicationWindow.color
                RowLayout {
                    spacing:20
                    anchors.fill: parent
                    Button{
                        icon.source: "../Resources/Images/Retry.svg"
                        id:loadButtonCalibrationRetry
                        anchors.left:parent.left
                        anchors.leftMargin: 20
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.top:parent.top
                        anchors.bottom:parent.bottom
                        width:height
                        onClicked: scenarioCalibration.reset()
                    }
                    Text{
                        id:textCalibration
                        anchors.leftMargin: 20
                        anchors.left:loadButtonCalibrationRetry.right
                        font.family: "Helvetica"
                        font.pointSize: 15
                        color: "white"
                        text:"Center : x = " +Math.round(calibration.meanCalibration.x)+" y = "+Math.round(calibration.meanCalibration.y)+" Ratio : x = " +Math.round(calibration.ratioCalibration.x)+" y = "+Math.round(calibration.ratioCalibration.y)
                    }
                    GroupBox {
                        title: "Frame mean"
                        RowLayout {
                            Slider {
                                id:frameMeanSlider
                                from: 1
                                to: 10
                                value: calibration.frameMean
                                onMoved:{
                                    calibration.frameMean = frameMeanSlider.value
                                    canvasCalibration.requestPaint()
                                }
                            }
                            SpinBox {
                                id:frameMeanSpinBox
                                from: 1
                                value: calibration.frameMean
                                to: 10
                                onValueModified : {
                                    calibration.frameMean = frameMeanSpinBox.value
                                    canvasCalibration.requestPaint()
                                }
                            }
                        }
                    }
                    Button{
                        icon.source: "../Resources/Images/Save.svg"
                        id:loadButtonCalibration
                        anchors.right:parent.right
                        anchors.rightMargin: 20
                        anchors.topMargin: 20
                        anchors.bottomMargin: 20
                        anchors.top:parent.top
                        anchors.bottom:parent.bottom
                        width:height
                        onClicked: fileDialogSaveCalibration.visible=true
                    }
                }
            }
        }
        Rectangle{
            id:cible
            color:"transparent"
            height:20
            width:20
            radius:10
            opacity:0.5
            visible : false
            x: scenarioCalibration.width/2-10
            y: scenarioCalibration.height/2-10
            Image {
                anchors.fill:parent
                source: "../Resources/Images/Target.svg"
            }
            onXChanged:{
                calibration.setPositionCalibration(Qt.point(cible.x, cible.y))
            }
            onYChanged:{
                calibration.setPositionCalibration(Qt.point(cible.x, cible.y))
            }
        }

        MouseArea {
            id : areaCalibration
            anchors.fill: parent
          acceptedButtons: Qt.LeftButton | Qt.RightButton
            onReleased: {
                if(mouse.button == 1 && !calibration.record){
                   scenarioCalibration.start()
                }
                if(mouse.button == 2){
                    scenarioCalibration.quit()
                }
            }

        }
        transitions: [
            Transition {
                NumberAnimation {
                    target: cible
                    properties: "height,width,x,y, opacity";
                    duration: scenarioCalibration.speed
                }
                onRunningChanged : {
                    if(!running && calibration.record){
                        scenarioCalibration.switchState()
                        calibration.setStateCalibration(scenarioCalibration.state)
                    }
                }
            }
        ]

        function reset() {
            calibration.reset()
            areaCalibration.enabled  = true;
            scenarioCalibration.state = "";
            scenarioCalibration.opacity1 = 1
            scenarioCalibration.opacity2 =0.2;
            resultCalibration.visible = false;
            canvasCalibration.height = scenarioCalibration.height;
            canvasCalibration.requestPaint();
            warningText.text="Click for start"
        }

        function start() {
            scenarioCalibration.state = "center"
            calibration.setStateCalibration("center")
            calibration.record = true;
            toolBarApp.visible = false
            menuBarApp.visible = false
            canvasCalibration.height = scenarioCalibration.height;
            canvasCalibration.requestPaint();
        }
        function quit() {
            calibration.record = false;
            toolBarApp.visible = true
            menuBarApp.visible = true
            back()
        }

        function stop() {
            scenarioCalibration.state = "center"
            toolBarApp.visible = true
            menuBarApp.visible = true
            scenarioCalibration.opacity1 = 0.8
            scenarioCalibration.opacity2 = 1
            calibration.record = false;
            calibration.process()
            resultCalibration.visible = true
            canvasCalibration.height = scenarioCalibration.height-95
            cible.visible = false
            canvasCalibration.requestPaint()
            areaCalibration.enabled  = false;
        }

        property string nextState: ""

        function switchState() {
            if (scenarioCalibration.state == "center"){
                scenarioCalibration.nextState = "nw"
                scenarioCalibration.state = "focusStart"
                cible.visible =true
                return
            }
            if (scenarioCalibration.state == "focusStart"){

                scenarioCalibration.state = "focusStop"
                return
            }
            if (scenarioCalibration.state == "focusStop"){
                scenarioCalibration.state = scenarioCalibration.nextState
                return
            }
            if (scenarioCalibration.state == "nw"){
                scenarioCalibration.nextState = "ne"
                scenarioCalibration.state = "focusStart"
                return
            }
            if (scenarioCalibration.state == "ne"){
                scenarioCalibration.nextState = "sw"
                scenarioCalibration.state = "focusStart"
                return
            }
            if (scenarioCalibration.state == "sw"){
                scenarioCalibration.nextState = "se"
                scenarioCalibration.state = "focusStart"
                return
            }
            if (scenarioCalibration.state == "se"){
                scenarioCalibration.nextState = "stop"
                scenarioCalibration.state = "focusStart"
                return
            }
            if (scenarioCalibration.state == "stop"){
                scenarioCalibration.stop()
                return
            }
        }

        states: [
             State {
                name: "center"

                PropertyChanges {
                    target: cible
                    x: scenarioCalibration.width/2-10
                    y: scenarioCalibration.height/2-10
                }
            },
            State {
                name: "focusStart"

                PropertyChanges {
                    target: cible
                     x: scenarioCalibration.cible.x
                     y: scenarioCalibration.cible.y
                     opacity: 1
                     height:40
                     width:40
                }
            },
            State {
                name: "focusStop"

                PropertyChanges {
                    target: cible
                     height:20
                     width:20
                     x: scenarioCalibration.cible.x-10
                     y: scenarioCalibration.cible.y
                     opacity: 0.5
                }
            },
            State {
                name: "nw"

                PropertyChanges {
                    target: cible
                    x: 30
                    y: 30
                }
            },
            State {
                name: "ne"

                PropertyChanges {
                    target: cible
                    x: scenarioCalibration.width-50
                    y: 30
                }
            },
            State {
                name: "se"

                PropertyChanges {
                    target: cible
                    x: scenarioCalibration.width-50
                    y: scenarioCalibration.height-50
                }
            },
            State {
                name: "sw"

                PropertyChanges {
                    target: cible
                    x: 30
                    y: scenarioCalibration.height-50
                }
            },
             State {
                name: "stop"

                PropertyChanges {
                    target: cible
                    x: scenarioCalibration.width/2-10
                    y: scenarioCalibration.height/2-10
                }
            }
        ]
    }
}