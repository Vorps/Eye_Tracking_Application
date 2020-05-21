import QtQuick 2.0
import QtQuick.Controls 2.4
import "Style"
import QtQuick.Layouts 1.14
Item{
    ColumnLayout{
        anchors.fill:parent
        ResultView{
            id:canvasCalibration
            height:parent.height-95
        }
        Rectangle{
            id: resultCalibration
            anchors.bottom: parent.bottom
            anchors.horizontalCenter : parent.horizontalCenter
            height: 95
            width : 800
            opacity : 0.8
            color:applicationWindow.color
            RowLayout {
                spacing:20
                anchors.fill: parent
                Text{
                    id:textCalibration
                    anchors.leftMargin: 20
                    anchors.left:loadButtonCalibrationRetry.right
                    font.family: "Helvetica"
                    font.pointSize: 15
                    color: "white"
                    text:"Center : x = " +Math.round(calibration.meanCalibration.x)+" y = "+Math.round(calibration.meanCalibration.y)+" Ratio : x = " +Math.round(calibration.ratioCalibration.x)+" y = "+Math.round(calibration.ratioCalibration.y)
                }

                        SpinBox {
                            label:"Frame mean"
                            id:frameMeanSpinBox
                            from: 1
                            value: calibration.frameMean
                            to: 10
                            onValueChanged : {
                                calibration.frameMean = frameMeanSpinBox.value
                                canvasCalibration.requestPaint()
                            }
                        }
                Button{
                    icon.source: "../Resources/Images/Plot.svg"
                    id:loadButtonCalibration
                    anchors.right:parent.right
                    anchors.rightMargin: 20
                    anchors.topMargin: 20
                    anchors.bottomMargin: 20
                    anchors.top:parent.top
                    anchors.bottom:parent.bottom
                    width:height
                    onClicked: calibration.plot()
                }
            }
        }
    }
}