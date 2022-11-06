import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 6.3
import QtMultimedia 6.3


Rectangle {
    id: audioControl
    width: 300
    height: 80

    RowLayout {
        id: rowLayout
        anchors.fill: parent
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.topMargin: 5

        property string audioToPlay : ""

        RowLayout {
            id: buttons
            width: 100
            height: 100
            Layout.fillHeight: true


            Dial {
                id: volumeDial
                visible: true
                Layout.minimumWidth: 70
                Layout.maximumWidth: 70
                Layout.maximumHeight: 70
                Layout.minimumHeight: 70
                Layout.rowSpan: 2
                from: 0.0
                value: 0.5
                to: 1.0
                clip: false
            }

            RoundButton {
                id: playToggle
                text: ""
                Layout.minimumWidth: 40
                Layout.minimumHeight: 40
                icon.source: "images/play.png"
                display: AbstractButton.IconOnly
                icon.color: "#00ffffff"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                flat: false
                Layout.fillHeight: false
                Layout.fillWidth: false
                onPressed: audioControl.toggle()
            }

        }
        ColumnLayout {
            id: trackMetadata
            width: 100
            height: 100
            Layout.fillHeight: true
            Layout.fillWidth: true


            Text {
                id: audioTrack
                text: qsTr("<NONE>")
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.fillWidth: true
            }
            Slider {
                id: audioProgress
                Layout.fillHeight: true
                Layout.fillWidth: true
                clip: false
                transformOrigin: Item.Center
                wheelEnabled: false
                hoverEnabled: false
                enabled: true
                value: 0.5

                onMoved: (value) => seekTo(audioProgress.value)
            }
        }
        MediaPlayer {
            id: player
            source: 'audio/aeiou.wav'

            onPositionChanged: audioControl.positionChanged(player.position)

            audioOutput: AudioOutput {
                id: output
                volume: volumeDial.value
            }
        }
    }

    function submitAudio(file, name, playOnStart) {
        var url = Qt.url(file)
        player.source = url;
        audioTrack.text = name ? name : 'Untitled'
        if (playOnStart)
            play()
    }

    //called only by NEW
    function clearAudio() {
        player.pause()
        player.source = 'audio/aeiou.wav'
        audioTrack.text = '<NONE>'
    }

    //called when setting back to beginning
    function pause() {
        player.pause()
        playToggle.icon.source = 'images/play.png'
    }

    //called when setting back to beginning
    function play() {
        player.play()
        playToggle.icon.source = 'images/pause.png'
    }

    function toggle() {
        //if there's audio to play, play it, else skip
        if (player.mediaStatus == MediaPlayer.NoMedia)
            return;
        if (player.playbackState == MediaPlayer.StoppedState || player.playbackState == MediaPlayer.PausedState) {
            //reset position if can
            if (player.mediaStatus == MediaPlayer.EndOfMedia)
                player.setPosition(0.0)
            play()
        } else {
            pause()
        }
    }

    function positionChanged(position) {
        var percent = position / player.duration;
        audioProgress.value = percent

        //set back to 'play' if over. Unfortunately, EndOfMedia is triggered AFTER last position update, so gotta do delta compare
        if (percent > (1 - .003)) {
            pause()
            player.setPosition(0)
        }
    }

    function seekTo(position) {
        player.position = position * player.duration
    }
}
