import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Item {
    ColumnLayout{
        anchors.centerIn: parent
        spacing:parent.height/10
        width:parent.width/4
        AppButton{
            text:'New Calibration'
            Layout.fillWidth:true
        }
        AppButton{
            text:'Report'
            Layout.fillWidth:true
        }
    }
}