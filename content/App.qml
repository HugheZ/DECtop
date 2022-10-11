import QtQuick 6.2
import QtQuick.Controls 2.15
import QtQuick.Window 6.2
import DECtop 1.0
import QtQuick.Dialogs

Window {
    id: window
    width: 600
    height: 600

    palette.buttonText: "black"

    visible: true
    minimumHeight: 300
    minimumWidth: 500
    maximumHeight: 1080
    maximumWidth: 950
    title: "DECtop"
    onClosing: {
        close.accepted = false
        beforeQuit()
    }

    MenuBar {
        id: menu
        height: 28
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        contentHeight: 30
        //file, options, etc
        Menu {
            title: qsTr("&File")
            Action {
                text: qsTr("New")
                onTriggered: beforeNew()
            }
//            Action { text: qsTr("&Import...") }
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator {}
            Action {
                text: qsTr("&Quit")
                onTriggered: beforeQuit()
            }
        }
    }

    MessageDialog {
        id: quitConfirm
        text: "Are you sure you would like to quit? You have unsaved changes to transcript and or audio file."

        buttons: MessageDialog.Yes | MessageDialog.Cancel
        onAccepted: { Qt.quit() }
    }

    MessageDialog {
        id: newConfirm
        text: "Are you sure you would like to edit a new prompt? You have unsaved changes."

        buttons: MessageDialog.Yes | MessageDialog.Cancel
        onAccepted: { mainScreen.newDocument() }
    }

    MainLayout {
        id: mainScreen
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: menu.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 0
    }

    function beforeQuit() {
        if (mainScreen.dirty)
            quitConfirm.open()
        else Qt.quit()
    }

    function beforeNew() {
        if (mainScreen.dirty)
            newConfirm.open()
        else mainScreen.newDocument()
    }
}

