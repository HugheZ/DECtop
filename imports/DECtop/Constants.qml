pragma Singleton
import QtQuick 6.2
//import QtQuick.Studio.Application
import QtCore 6.2

QtObject {
    readonly property int width: 1920
    readonly property int height: 1080

    property string relativeFontDirectory: "fonts"

    /* Edit this comment to add your custom font */
    readonly property font font: Qt.font({
                                             family: Qt.application.font.family,
                                             pixelSize: Qt.application.font.pixelSize
                                         })
    readonly property font largeFont: Qt.font({
                                                  family: Qt.application.font.family,
                                                  pixelSize: Qt.application.font.pixelSize * 1.6
                                              })

    readonly property color backgroundColor: "#c2c2c2"


//    property StudioApplication application: StudioApplication {
//        fontPath: Qt.resolvedUrl("../../content/" + relativeFontDirectory)
//    }

    readonly property string saveDir: StandardPaths.writableLocation(StandardPaths.DocumentsLocation) + '/DECtop'

    readonly property string tempDir: StandardPaths.writableLocation(StandardPaths.TempLocation) + '/DECtop'
}
