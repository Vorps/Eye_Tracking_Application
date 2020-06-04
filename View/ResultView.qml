import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14
import "Style"

            Canvas {
                property real opacity1: 1
                property real opacity2: 0.1
                id: canvasCalibration
                height:parent.height
                width:parent.width
                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset();
                    ctx.fillStyle = Qt.rgba(200, 200, 200, canvasCalibration.opacity1);
                    ctx.fillRect(0, 0, width, height)
                    ctx.fill()
                    ctx.lineWidth = 4
                    ctx.strokeStyle = Qt.rgba(0, 1, 0, canvasCalibration.opacity2);
                    ctx.moveTo(40, 40)
                    ctx.lineTo(width-40, height-40)
                    ctx.moveTo(40, 40)
                    ctx.lineTo(width-40, 40)
                    ctx.moveTo(40, height-40)
                    ctx.lineTo(width-40, 40)
                    ctx.moveTo(40, height-40)
                    ctx.lineTo(width-40, height-40)
                    ctx.stroke()
                    ctx.fillStyle = Qt.rgba(1, 0, 0, canvasCalibration.opacity1);
                    for(var i in calibration.centersPupilCalibration){
                        var point = calibration.centersPupilCalibration[i]
                        ctx.roundedRect((point.x*canvasCalibration.width)+width/2, (point.y*canvasCalibration.height)+canvasCalibration.height/2,4,4,2,2)
                        ctx.fill()
                    }
                }
            }
