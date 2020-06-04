import QtQuick 2.0
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.14

Button{
    id:appButton
    property int widthNormal: width
    height :40
    background: Rectangle {
        id:rect
        width:400
        height:40
        border.width: 1
        opacity: 0.8
        radius: 10
        color:"#2b3948"
        MouseArea{
            id: rec1M
            anchors.fill: parent
            hoverEnabled: true
            onEntered:{
                rect.color= applicationWindow.color
            }
            onExited: {
                rect.color= "#2b3948"
            }
            onReleased: {
                if(appButton.enabled){
                    load_page(text)
                }
            }
        }
        onEnabledChanged: rect.opacity = appButton.enabled ? 1 : 0.3
        Image {
            height:35
            width:35
            anchors.verticalCenter:parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
            source: "../Resources/Images/"+appButton.text+".svg"
        }
    }
    contentItem: Text {
        anchors.fill:rect
        text: parent.text
        font.family: "Helvetica"
        font.pointSize: 18
        opacity: 0.5
        color:"white"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}