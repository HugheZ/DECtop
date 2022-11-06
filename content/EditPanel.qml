import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 6.3
import DECtop 1.0

Rectangle {
    id: editPanel
    width: 600
    height: 400
    color: Constants.backgroundColor

    signal modified()
    property bool dirty: false

    property alias text: textInput.text
    property alias rate: speakingRate.value

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        spacing: 4

        Rectangle {
            id: rectangle
            width: 200
            height: 200
            color: "#ffffff"
            Layout.preferredHeight: 50
            Layout.maximumHeight: 60
            Layout.fillHeight: false
            Layout.minimumHeight: 50
            Layout.fillWidth: true

            GridLayout {
                id: gridLayout
                anchors.fill: parent
                rowSpacing: 1
                rows: 2
                columns: 2



                Text {
                    id: rateText
                    text: qsTr("Speaking Rate")
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    Layout.rightMargin: 5
                    Layout.columnSpan: 1
                    Layout.rowSpan: 1
                    Layout.minimumWidth: 80
                    Layout.maximumWidth: 80
                    Layout.margins: 5
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }

                Text {
                    id: titleText
                    text: qsTr("Title")
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }

                SpinBox {
                    id: speakingRate
                    from: 75
                    value: 200
                    to: 600
                    editable: true
                    Layout.maximumWidth: 80
                    Layout.preferredWidth: 80
                    Layout.minimumWidth: 80
                    Layout.margins: 5
                    Layout.fillHeight: false
                    Layout.fillWidth: false
                    onValueModified: editPanel.setModifiedAndEmit()
                }

                Text {
                    id: titleAndLocation
                    text: qsTr("Untitled")
                    font.pixelSize: 12
                }

            }
        }

        ScrollView {
            id: scrollComponent
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Rectangle {
                id: textAreaColor
                anchors.fill: parent
                TextArea {
                    id: textInput
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    leftPadding: 7
                    transformOrigin: Item.Center
                    placeholderText: qsTr("Input text here. When ready, press \"Submit Text\" to perform TTS.")
                    onTextChanged: editPanel.setModifiedAndEmit()
                }
            }
        }

    }

    //emits the modified signal if not already
    function setModifiedAndEmit() {
        if (!editPanel.dirty) {
            editPanel.dirty = true
            titleAndLocation.text = titleAndLocation.text + '*'
            editPanel.modified()
        }
    }

    //called on save, this removes the * at the end of the file and clears dirty
    function clearDirty() {
        editPanel.dirty = false
        if (titleAndLocation.text.endsWith('*'))
            titleAndLocation.text = titleAndLocation.text.replace(/.$/, '') //remove last * to indicate modified
    }

    function setName(newName) {
        titleAndLocation.text = newName
    }

    //expects dect obj, see example.dect for format
    //unfortunately, changing text still emits the modified event, so that sucks
    function setDect(dect, fileLocation) {
        if (dect) {
            if (dect.text)
                textInput.text = dect.text
            if (dect.metadata) {
                if (dect.metadata.rate)
                    speakingRate.value = dect.metadata.rate
            }

            if (fileLocation)
                titleAndLocation.text = fileLocation
            
            //have to manually clear dirty, love how 'programmatic' set still sets 'onModified'
            editPanel.dirty = false
        } else {
            reset()
        }
    }

    //completely resets the state to NEW
    function reset() {
        editPanel.dirty = false
        speakingRate.value = 0
        textInput.text = ''
        titleAndLocation.text = 'Untitled'
    }
}
