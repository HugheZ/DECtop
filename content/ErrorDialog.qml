import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

Item {
    function openError(message, detail) {
        errorDialog.informativeText = message ?
                    message :
                    'An error occured during the previous operation, preventing it from completing.'
        errorDialog.detailedText = detail ?
                    detail :
                    null
        errorDialog.open()
    }

    MessageDialog {
        id: errorDialog
        text: 'An error has occurred'
        buttons: MessageDialog.Ok
    }
}
