import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

Item {
    Rectangle{
        id:scenarioCalibration
        property int speed: 1000
        anchors.fill:parent
        color:'transparent'
        ColumnLayout{
anchors.fill:parent
        ResultView{
            id:canvasCalibration
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
                Row {
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
                    AppButton{
                        text:'Report'
                        x: 100
                        y :parent.height/2-height/2
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
                calibration.setPositionCalibration(Qt.point(cible.x-scenarioCalibration.width/2, cible.y-scenarioCalibration.height/2))
            }
            onYChanged:{
                calibration.setPositionCalibration(Qt.point(cible.x-scenarioCalibration.width/2, cible.y-scenarioCalibration.height/2))
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
            calibration.setSize(canvasCalibration.width, canvasCalibration.height)
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
            canvasCalibration.opacity1 = 0.8
            canvasCalibration.opacity2 = 1
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
                     opacity: 1

                     x: scenarioCalibration.cible.x-10
                     y: scenarioCalibration.cible.y
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
