import QtQuick 2.14
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Item{
    Rectangle
    {
        id: background
        anchors.fill: parent
        color:"#ececec"
    }
    property var pass: 0
    Image {
        id : imageSimonTask
        anchors.centerIn: parent
        source: "../Resources/Images/start.png"
    }
    Text {
        text: "Pass : "+pass
    }
}