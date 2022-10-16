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
    title: "DECtop"
    onClosing: (closeEvent) => {
        closeEvent.accepted = false
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
                shortcut: StandardKey.Open
                onTriggered: beforeNew()
            }
            Action {
                text: qsTr("&Save")
                shortcut: StandardKey.Save
                onTriggered: window.save()
            }
            Action {
                text: qsTr("Save &As...")
                shortcut: "Ctrl+Shift+s"
                onTriggered: window.openSaveAs()
            }
            MenuSeparator {}
            Action {
                text: qsTr("&Quit")
                shortcut: StandardKey.Quit
                onTriggered: Qt.quit()
            }
        }
    }

    MessageDialog {
        id: quitConfirm
        text: "Are you sure you would like to quit? You have unsaved changes to transcript and or audio file."

        buttons: MessageDialog.Yes | MessageDialog.Cancel
        onAccepted: { Qt.exit(0) } //MUST be exit, or else we get an onClose loop
    }

    MessageDialog {
        id: newConfirm
        text: "Are you sure you would like to edit a new prompt? You have unsaved changes."

        buttons: MessageDialog.Yes | MessageDialog.Cancel
        onAccepted: { mainScreen.newDocument() }
    }

    Dialog {
        width: 200
        id: saveAsDialog
        title: qsTr("Input save name")

        contentItem: TextField {
            id: newNameField
            placeholderText: "Input Name"

            onTextChanged: {
                if (newNameField.text)
                    saveAsDialog.standardButton(Dialog.Ok).enabled = true
                else saveAsDialog.standardButton(Dialog.Ok).enabled = false
            }
        }
        standardButtons: Dialog.Ok | Dialog.Cancel

        onOpened: {
            saveAsDialog.standardButton(Dialog.Ok).enabled = false
            newNameField.text = null
        }

        onAccepted: {
            if (newNameField.text)
                window.saveAs(newNameField.text)
        }
    }

    MainLayout {
        objectName: "mainLayout"
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

    function openSaveAs() {
        saveAsDialog.open()
        newNameField.forceActiveFocus()
    }

    function save() {
        console.log(mainScreen.dirty, mainScreen.getCurrentFileDir(), mainScreen.dirty && mainScreen.getCurrentFileDir())
        if (mainScreen.dirty && mainScreen.getCurrentFileDir()) //if has dir, it already has a save name
            mainScreen.save()
        else openSaveAs()
    }

    function saveAs(name) {
        if (mainScreen.dirty)
            mainScreen.saveAs(Constants.saveDir, name)
    }
}
