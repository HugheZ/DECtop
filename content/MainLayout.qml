import QtQuick 6.2
import QtQuick.Controls 6.2
import DECtop
import QtMultimedia 6.3
import QtQuick.Controls.Windows 6.0
import QtQuick.Layouts 6.3
import QtCharts 6.3

Rectangle {
    id: mainLayout
    width: 950
    height: Constants.height
    color: Constants.backgroundColor

    property bool dirty: false

    ColumnLayout {
        id: gridLayout
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10

        RowLayout {
            id: rowLayout
            width: 100
            height: 100
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayout
                width: 100
                height: 100

//                StackLayout {
//                    id: multidocOrganizer
//                    width: 100
//                    height: 100
//                    Layout.fillHeight: true
//                    Layout.fillWidth: true


//                    TabBar {
//                        id: tabBar
//                        Layout.minimumHeight: 20
//                        Layout.maximumHeight: 20
//                        Layout.fillHeight: false
//                        Layout.fillWidth: true
//                        TabButton {
//                            width: 80
//                            text: qsTr("Untitled")
//                        }
//                    }

//                    EditPanel {
//                        id: editPanel
//                        Layout.fillHeight: true
//                        Layout.fillWidth: true
//                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                        transformOrigin: Item.Center
//                        onModified: mainLayout.textDirty = true
//                    }
//                }

                EditPanel {
                    id: editPanel
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    transformOrigin: Item.Center
                    onModified: mainLayout.dirty = true
                }

                Button {
                    id: submitButton
                    text: qsTr("Submit Text")
                    palette.buttonText: "black"
                    Layout.preferredHeight: 80
                    Layout.maximumHeight: 50
                    Layout.fillHeight: false
                    Layout.fillWidth: true
                }

            }

            SavedAudioList {
                id: savedAudioList
                Layout.maximumWidth: 200
                Layout.fillHeight: true
                Layout.fillWidth: true

                //TODO hooks
                onPlayAudio: (dir, filename) => playSavedAudio(dir, filename)
                onEditAudio: (dir, filename) => loadAndEditAudio(dir, filename)
                onDeleteAudio: (dir) => deleteAudio(dir)
            }

        }

        AudioControl {
            id: audioControl
            Layout.minimumHeight: 70
            Layout.minimumWidth: 300
            Layout.maximumHeight: 200
            Layout.preferredHeight: -1
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }

    function newDocument() {
        editPanel.reset()
        //reset dirty value, since above modifies values
        dirty = false
    }

    function loadAndEditAudio(dir, filename) {
        //TODO
        console.log('TODO: load and edit ' + dir + '/' + filename)
    }

    function deleteAudio(dir) {
        //TODO
        console.log('TODO: delete ' + dir)
    }

    //just plays the cached audio, nothing else
    function playSavedAudio(dir, filename) {
        audioControl.submitAudio(dir, filename)
    }
}