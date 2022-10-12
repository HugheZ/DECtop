from genericpath import isfile
from os import path
from shutil import rmtree
import json
from PySide6.QtCore import Slot, QObject, QUrl, QDir
from PySide6.QtQml import QmlElement


QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_NAME = 'DECtop'


@QmlElement
class QmlBackend(QObject):

    def __init__(self, parent=None, dec_engine=None):
        QObject.__init__(self, parent)
        self.engine = dec_engine
        self.model = None
        self.save_dir = None

    @Slot(str, result=dict)
    def load_transcript(self, dectfile) -> None:
        if not path.exists(dectfile):
            raise FileNotFoundError('File "' + dectfile + '" does not exist.')
        if not path.isfile(dectfile) or not dectfile.lower().endswith('.dect'):
            raise ValueError('File "' + dectfile + '" is not a .dect metadata file.')
        j = None
        with open(dectfile, 'r') as f:
            j = json.load(f)
        
        #do some cleanup  here. If the file specified by the cache field doesn't exist, remove it from the json and save
        if j['audio'] is not None and not path.exists(j['audio']):
            j['audio'] = None
            with open(dectfile, 'w') as f:
                json.dump(j, f)

        self.model = j
        self.save_dir = path.dirname(dectfile)

    @Slot(str)
    def delete_audio_library(self, directory) -> None:
        if not path.exists(directory):
            raise FileNotFoundError('Directory "' + directory + '" does not exist.')
        if not path.isdir(directory):
            raise ValueError('Directory "' + directory + '" is not a directory.')
        rmtree(directory)
        self.model = None
    
    @Slot(result="QVariantMap")
    def get_model(self) -> dict:
        return self.model
    
    #handy getter for qurl-formatted URL, since doing that in QML is stupidly weird
    @Slot(result=QUrl)
    def get_qurl_cached_audio(self) -> QUrl:
        if self.model is not None and self.model['audio'] is not None:
            return QUrl.fromLocalFile(self.model['audio'])
        return None
    
    #not needed now, but the logic for QT paths is so weird that I want this here for reference
    @Slot(QUrl, result=str)
    def qt_to_local_file(self, filePath) -> str:
        return QDir.toNativeSeparators(filePath.toLocalFile())
    
    #dummy function for when we have the QML def but not Python backend
    @Slot(result=bool)
    def is_live(self) -> bool:
        print(self.test)
        return True