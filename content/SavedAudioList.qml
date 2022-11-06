import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 6.3
import QtQuick3D 6.3
import Qt.labs.folderlistmodel 2.15
import DECtop


Rectangle {
    id: savedList
    width: 200
    height: 600

    //signals to parrot everything up to a central point for easy hooking
    signal playAudio(url dir, string filename) //emit to load into the audio source
    signal editAudio(url dir, string filename) //emit to load transcript into edit field
    signal deleteAudio(url dir) //emit to delete saved audio dir

    Item {
        id: __materialLibrary__
    }

    ScrollView {
        id: scrollView
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.topMargin: 5
        clip: true
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        Layout.fillHeight: true
        Layout.fillWidth: true
        ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ListView {
            id: listView
            visible: true
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 8
            spacing: 2
            snapMode: ListView.SnapToItem
            clip: false
            model: FolderListModel {
                id: savedAudioFilesModel
                folder: Constants.saveDir
                showFiles: true
                showDirs: false
                nameFilters: ["*.dect"]
            }

            delegate: SavedAudio {
                id: savedAudioDelegate
                width: listView.width - 5
                height: 60
                filePath: fileUrl // /place/in/dir/savedir/filename
                titleText: fileBaseName // /place/in/dir/savedir/filename/<filename.dect or filename.wav>
                //I've been workin' on the chain gang, all the live-long day
                onPlayAudio: (filePath, title) => savedList.playAudio(filePath, title)
                onEditAudio: (filePath, title) => savedList.editAudio(filePath, title)
                onDeleteAudio: filePath => savedList.deleteAudio(filePath)
            }
            headerPositioning: ListView.OverlayHeader
            header: Rectangle {
                Text {
                    id: savedItemsTitle
                    text: qsTr("Saved Audio")
                    font.pixelSize: 12
                    Layout.rightMargin: 5
                    Layout.leftMargin: 5
                    Layout.bottomMargin: 5
                    Layout.topMargin: 5
                    Layout.maximumHeight: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }
                width: parent.width
                height: 20
                z:2
            }
        }
    }
}
