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

    //TODO: make this alias of editPanel.dirty
    property bool dirty: false

    //Python backend object
    QmlBackend {id: backend}

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
                    onPressed: mainLayout.runTTS()
                }

            }

            SavedAudioList {
                id: savedAudioList
                Layout.maximumWidth: 200
                Layout.fillHeight: true
                Layout.fillWidth: true

                //TODO hooks
                onPlayAudio: (dir, filename) => mainLayout.playSavedAudio(dir, filename)
                onEditAudio: (dir, filename) => mainLayout.loadAndEditAudio(dir, filename)
                onDeleteAudio: (dir) => mainLayout.deleteAudioDir(dir)
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

    // Resets the document and edit panel
    //
    //
    function newDocument() {
        editPanel.reset()
        //reset dirty value, since above modifies values
        mainLayout.dirty = false
        audioControl.clearAudio()
    }

    // Loads the directory and sets the editPanel / audio player to the source
    //
    //
    function loadAndEditAudio(dir, filename) {
        if (backend && backend.is_live) {
            backend.load_transcript(dir + '/' + filename)

            //now link up to the ui
            var backendModel = backend.get_model()
            editPanel.setDect(backendModel)
            //IF we have cached audio, also submit that
            mainLayout.splitUrlAndQueue(backend.get_qurl_cached_audio())
        } else {
            console.log('TODO: load and edit ' + dir + '/' + filename)
        }
    }

    //just plays the cached audio, nothing else
    //
    //
    function playSavedAudio(dir, filename) {
        audioControl.submitAudio(dir, filename, true)
    }

    //
    //
    //
    function splitUrlAndQueue(qUrl) {
        if (qUrl) {
            qUrl = qUrl.toString()
            const lastDirIndex = qUrl.lastIndexOf('/')
            audioControl.submitAudio(qUrl.slice(0, lastDirIndex),
                                     qUrl.slice(lastDirIndex + 1),
                                     false)
        }
    }

    // Submits the text for TTS conversion and sets the audio player
    //
    //
    function runTTS() {
        if (backend && backend.is_live) {
            backend.set_text(editPanel.text)
            const saveLocation = backend.run_TTS()
            if (saveLocation && saveLocation.toString()) {
                mainLayout.splitUrlAndQueue(saveLocation)
            } else {
                //we only WONT have a URL if someone hits submit without any actual text, so that can be skipped and reset
                audioControl.clearAudio()
            }
        }
    }

    // Deletes the provided directory
    //
    //
    function deleteAudioDir(dir) {
        if (backend && backend.is_live) {
            backend.delete_audio_library(dir)
        } else {
            console.log('TODO: delete ' + dir)
        }
    }

    function getCurrentFileDir() {
        if (backend && backend.is_live) {
            return backend.get_save_path()
        }
        return false
    }

    //construct metadata object. Central point for meta changes in the future
    //
    //
    function constructMeta() {
        return {
            'rate':editPanel.rate
        }
    }

    //functions for saving. Expects caller for determining eligibility (i.e. is dirty and has name for non-save-as)
    //
    //
    function save() {
        if (backend && backend.is_live) {
            if (mainLayout.dirty || !(backend.get_model())) {
                backend.set_text(editPanel.text)
                backend.set_metadata(mainLayout.constructMeta())
                //TODO: submit audio and save that as well
            }
            backend.save_model(null, null)
        }

        mainLayout.dirty = false
        editPanel.clearDirty()
    }

    function saveAs(dir, name) {
        if (backend && backend.is_live) {
            if (mainLayout.dirty || !(backend.get_model())) {
                backend.set_text(editPanel.text)
                backend.set_metadata(mainLayout.constructMeta())
                //TODO: submit audio and save that as well
                //TODO: here we ALSO have to grab the temp location for the move
            }
            backend.save_model(dir, name)
        }

       //TODO: update UI

        mainLayout.dirty = false
        editPanel.clearDirty()
    }
}
