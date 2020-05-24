import QtQuick.Controls 2.4
import QtQuick 2.0
import QtQuick.Layouts 1.14
import Models 1.0
import QtQuick.Dialogs 1.2
import QtQuick.Controls.Universal 2.12
import "Style"

ApplicationWindow {
    id : applicationWindow
    objectName: "applicationWindow"
    title: "Eyes Tracking Application"
    visible: true
    width: 1400
    height: 850
    color:"#151d25"
    onClosing: {
        envVariable.save("Data/EnvVariable/Default.xml")
    }

    ButtonGroup { id: radioGroup1 }
    ButtonGroup { id: radioGroup2 }

    menuBar: MenuBar {
        id: menuBarApp
        height:25
        Menu {
        title: "File"
                Action {
                    text: "Load Setup"
                    shortcut: "Ctrl+O"
                    onTriggered: fileDialogLoad.visible=true
                }
                Action {
                    text: "Save Setup"
                    shortcut: "Ctrl+S"
                    onTriggered: fileDialogSave.visible=true
                }
                MenuSeparator { }
                 Action {
                    text: "Load Calibration"
                    shortcut: "Ctrl+C"
                    onTriggered: fileDialogLoadCalibration.visible=true
                }
                Action {
                    text: "Save Calibration"
                    shortcut: "Ctrl+S"
                    onTriggered: fileDialogSaveCalibration.visible=true
                }
                MenuSeparator { }
                Action {
                    text: "Quit"
                    shortcut: "Ctrl+Q"
                    onTriggered: Qt.quit()

                }
            }

        Menu {
            title: "View"
            Action {
                text: "All"
                checkable:true
                checked : envVariable.modeView == 1
                onTriggered: envVariable.modeView = 1
                ButtonGroup.group: radioGroup1
            }

            Action {
                text: "Face"
                checkable:true
                checked : envVariable.modeView == 2
                onTriggered: envVariable.modeView = 2
                ButtonGroup.group: radioGroup1
            }
            Action {
                text: "Left eye"
                checkable:true
                checked : envVariable.modeView == 3
                onTriggered: envVariable.modeView = 3
                ButtonGroup.group: radioGroup1
            }
            Action {
                text: "Right eye"
                checkable:true
                checked : envVariable.modeView == 4
                onTriggered: envVariable.modeView = 4
                ButtonGroup.group: radioGroup1
            }
            Action {
                text: "Eyes"
                checkable:true
                checked : envVariable.modeView == 5
                onTriggered: envVariable.modeView = 5
                ButtonGroup.group: radioGroup1
            }
            MenuSeparator { }
             Action {
                text: "RGB"
                checkable:true
                checked : envVariable.typeView == 1
                onTriggered: envVariable.typeView = 1
                ButtonGroup.group: radioGroup2
            }
            Action {
                text: "Gray"
                checkable:true
                checked : envVariable.typeView == 2
                onTriggered: envVariable.typeView = 2
                ButtonGroup.group: radioGroup2
            }
            Action {
                text: "Treshold"
                checkable:true
                checked : envVariable.typeView == 3
                onTriggered: envVariable.typeView = 3
                ButtonGroup.group: radioGroup2
            }
            MenuSeparator { }
            Action {
                checkable:true
                text: "FullScreen"
                shortcut: "F11"
                onTriggered: applicationWindow.visibility = checked  ? "FullScreen" : "Windowed"
            }

        }
        Menu {
            id:helpMenu
            title: "Help"
            Action {
                text: "About"
                shortcut: "F9"
                onTriggered: {
                    dialog.visible = true
                    helpMenu.visible = false
                }
            }
        }
    }

    FileDialog {
        id: fileDialogLoad
        title: "Load Setup"
        folder: "../Data/EyeTrackingVariable"
        defaultSuffix :'xml'
        onAccepted: {
            eyeTrackingVariable.load(fileUrl);
            fileDialogLoad.visible = false
        }
        onRejected: {
            fileDialogLoad.visible = false
        }
    }

      FileDialog {
        id: fileDialogLoadCalibration
        title: "Load Calibration"
        folder: "../Data/Calibration"
        defaultSuffix :'xml'
        onAccepted: {
            calibration.load(fileUrl);
            fileDialogLoadCalibration.visible = false
        }
        onRejected: {
            fileDialogLoadCalibration.visible = false
        }
    }

     FileDialog {
            id: fileDialogSaveCalibration
            title: "Save Calibration"
            folder: "../Data/Calibration"
            selectExisting: false
            onAccepted: {
                calibration.save(fileUrl)
                fileDialogSaveCalibration.visible = false
            }
            onRejected: {
                fileDialogSaveCalibration.visible = false
            }
        }

    FileDialog {
        id: fileDialogSave
        title: "Save Setup"
        folder: "../Data/EyeTrackingVariable"
        selectExisting: false
        onAccepted: {
            eyeTrackingVariable.save(fileUrl)
            fileDialogSave.visible = false
        }
        onRejected: {
            fileDialogSave.visible = false
        }
    }

    MessageDialog {
        id:dialog
        visible:false
        title: "About"
        text: "Developers: Valentin BOUSSOT & Anh Vu NGUYEN\n"
        informativeText:"Supervisor: Assoc. Prof. Oscar ACOSTA"
        detailedText:"Preferences:\n"+
                 "Paul Viola and Michael J. Jones : Robust real-time face detection. International Journal of Computer Vision, 57(2):137–154, 2004.\n\n"+
                 "Shameem Hameed : haarcascade_eye.xml\n\n"+
                 "Rainer Lienhart : haarcascade_frontalface_default.xml\n\n"+
                 "Simon, J.R. and Wolf, J.D. : Choice reaction times as a function of angular stimulus-response correspondence and age. Ergonomics, 6, 99-105, 1963\n\n"+
                 "Psytoolkit.org : Simon Task\n\n"+
                 "OpenCV.org : opencv2 library\n\n"+
                 "Riverbank Computing : PyQT5 library"
        standardButtons: StandardButton.Ok
    }
    property int x1
    property int y1
    CVImage  {
        id: imageWriter
        opacity:0.3
        anchors.fill: parent
        image: capture.image
        MouseArea {
            id : areaZoom
            anchors.fill: parent
            focus:true
            onPressed:{
                x1 = mouseX
                y1 = mouseY
            }
            onPositionChanged: {
                if(pressed && stack.currentItem.objectName == "ent1"){
                    eyeTrackingVariable.posZoomX = eyeTrackingVariable.posZoomX+(mouseX-x1)
                    eyeTrackingVariable.posZoomY = eyeTrackingVariable.posZoomY+(mouseY-y1)
                    x1 = mouseX
                    y1 = mouseY
                }
            }
            onWheel:{
                if(stack.currentItem.objectName == "ent1"){
                    eyeTrackingVariable.zoomX = eyeTrackingVariable.zoomX+(wheel.angleDelta.y < 0 ? 100 : -100)
                    eyeTrackingVariable.zoomY = eyeTrackingVariable.zoomY+(wheel.angleDelta.y < 0 ? 50 : -50)
                }
            }
            onFocusChanged : if(!focus) { areaZoom.focus = true }
        }
    }



    header: ToolBar {
        id: toolBarApp
        RowLayout {
            id:toolBarAppRowLayout
            spacing:20
            anchors.fill: parent
            Button {
                height:40
                width:40
                id:homeButton
                enabled:false
                icon.source: "../Resources/Images/Back.svg"
                onClicked: {
                    back()
                }
            }
            CheckBox {
                checked: envVariable.modeProcess & 1
                text: qsTr("Eye-Tracking")
                onClicked:envVariable.modeProcess = 0
            }
            CheckBox {
                checked: envVariable.modeProcess >> 1 & 1
                text: qsTr("Pupil Segmentation")
                onClicked:envVariable.modeProcess = 1
            }
            CheckBox {
                checked: envVariable.modeProcess >> 2 & 1
                text: qsTr("Gaze Estimator")
                onClicked:envVariable.modeProcess = 2
            }
            CheckBox {
                checked: envVariable.modeProcess >> 3 & 1
                text: qsTr("FPS")
                onClicked:envVariable.modeProcess = 3
            }
            Label {
                id:warningText
                font.family: "Helvetica"
                font.pointSize: 15
                color: "red"
                text:""
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignRight
            }
            property bool stateWarning: false
            Timer {
                id:timerWarning
                interval: 500; running: calibration.record|mouseControl.record; repeat: true
                onTriggered: {
                    if(!toolBarAppRowLayout.stateWarning){
                        warningText.text = "Record ..."
                    } else {
                        warningText.text = ""
                    }
                    toolBarAppRowLayout.stateWarning = !toolBarAppRowLayout.stateWarning
                }
                onRunningChanged: warningText.text = ""

            }
            Label {
                text:envVariable.info
                Layout.fillWidth: true
                color:'white'
                horizontalAlignment: Text.AlignRight
            }
        }
    }

    StackView {
        id: stack
        anchors.fill: parent
        initialItem : mainView
        onCurrentItemChanged: {
            homeButton.focus = false
        }
    }

    Component{
        id : mainView
        MainView {}
    }

    Component{
        id : eyeTrackingVariableView
        EyeTrackingVariableView {}
    }


     Component{
        id : reportView
        ReportView {}
    }

    Component{
        id : mainCalibrationView
        MainCalibrationView {}
    }

    Component{
        id : calibrationView
        CalibrationView {}
    }


    Component{
        id : simonTaskView
        SimonTaskView {}
    }

    Component{
        id : mouseView
        MouseView {}
    }


    EnvVariable{
        id: envVariable
    }

    EyeTrackingVariable{
        id: eyeTrackingVariable
    }

    Calibration{
        id: calibration
    }

    MouseControl{
        id: mouseControl
    }

    CVCapture{
        id: capture
        Component.onCompleted: capture.start(envVariable.index)
    }

    function load_page(page){
        homeButton.enabled = true
        switch(page){
        case 'Setup':
            imageWriter.opacity= 1
            stack.push(eyeTrackingVariableView);
            break;
        case 'Report':
             stack.push(reportView);
             break;
        case 'Calibration':
            stack.push(mainCalibrationView);
             break;
        case 'New Calibration':
            calibration.reset()
            stack.push(calibrationView);
            warningText.text="Click for start"
            break;
        case 'Simon Task':
            stack.push(simonTaskView);
            break;
        case 'Simon Task':
            stack.push(simonTaskView);
            break;
        case 'Mouse':
            stack.push(mouseView);
            mouseControl.record = true
            break;
        }
    }

    function back(){
         imageWriter.opacity= 0.5
         envVariable.modeView = 1
         envVariable.typeView = 1
         calibration.record = false
         mouseControl.record = false
         stack.pop()
    }

}
