import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

Rectangle {
    id: savedAudio
    width: 170
    height: 60
    border.width: 1
    property alias titleText: title.text
    property url directory
    antialiasing: false

    signal playAudio(url directory, string title)
    signal editAudio(url directory, string title)
    signal deleteAudio(url directory)

    MessageDialog {
        property string titleToDelete: ""
        id: deleteConfirm
        text: "Are you sure you would like to delete " + titleToDelete + "?"
        buttons: MessageDialog.Yes | MessageDialog.Cancel

        //if we accept, send the delete
        onAccepted: {
            savedAudio.deleteAudio(directory)
        }
    }

    Text {
        id: title
        text: qsTr("Saved Item")
        anchors.left: parent.left
        anchors.top: parent.top
        font.pixelSize: 12
        anchors.leftMargin: 8
        anchors.topMargin: 8
    }

    Button {
        id: play
        y: 30
        width: 33
        height: 24
        text: qsTr("")
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        icon.source: "images/play.png"
        display: AbstractButton.IconOnly
        anchors.leftMargin: 8
        anchors.bottomMargin: 6
        onPressed: savedAudio.playAudio(directory, titleText + '.wav')
    }

    Button {
        id: edit
        y: 30
        width: 33
        height: 24
        text: qsTr("")
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        icon.source: "images/edit.png"
        display: AbstractButton.IconOnly
        anchors.leftMargin: 47
        anchors.bottomMargin: 6
        onPressed: savedAudio.editAudio(directory, titleText + '.dect')
    }

    Button {
        id: deleteTrack
        y: 30
        width: 33
        height: 24
        text: qsTr("")
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 8
        icon.source: "images/delete.png"
        display: AbstractButton.IconOnly
        anchors.bottomMargin: 6
        onPressed: {
            deleteConfirm.titleToDelete = titleText
            deleteConfirm.open()
        }
    }
}
