import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Item {
    ColumnLayout{
        anchors.centerIn: parent
        spacing:parent.height/10
        width:parent.width/4
        AppButton{
            text:'Setup'
            Layout.fillWidth:true
        }
        AppButton{
            text:'Calibration'
            Layout.fillWidth:true
        }
        AppButton{
            text:'Simon Task'
            Layout.fillWidth:true
            enabled:envVariable.calibrationLoad
        }
        AppButton{
            text:'Mouse'
            Layout.fillWidth:true
            enabled:envVariable.calibrationLoad
        }
    }
}