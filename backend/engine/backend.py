from os import path, makedirs
from shutil import rmtree, move
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
        self.name = None

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
        self.name = path.basename(path.normpath(self.save_dir))

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

    @Slot(result=str)
    def get_save_path(self) -> str:
        return self.save_dir
    
    #handy getter for qurl-formatted URL, since doing that in QML is stupidly weird
    @Slot(result=QUrl)
    def get_qurl_cached_audio(self) -> QUrl:
        if self.model is not None and self.model.get('audio') is not None:
            return QUrl.fromLocalFile(self.model['audio'])
        return None
    
    # if file_path and name is None, ignore the input and assume it's a 'save' not a 'saveAs'
    # note that file_path should be to the base save dir. The 'name' parameter is treated as both final directory as well as file names
    @Slot(str, str, result=bool)
    def save_model(self, file_path, name) -> bool:
        if file_path is not None and name is not None:
            # filePath is a qurl, so it needs to be normalized
            to_host_path = self.qt_to_local_file(file_path)
            self.save_dir = path.join(to_host_path, name)
            self.name = name
        
        # check to make sure the dirs actually exist
        makedirs(self.save_dir, exist_ok=True)

        with open(path.join(self.save_dir, self.name + '.dect'), 'w+') as f:
            json.dump(self.model, f)
        
        # if the audio dir is NOT the same as the .dect dir, it must be in the temp dir, or someone manually messed with files. Move it back.
        if self.model.get('audio') is not None and not path.samefile(path.normpath(self.model['audio']), path.normpath(self.save_dir)):
            move(self.model['audio'], path.join(self.save_dir, name + '.wav'))
        
        #TODO: test this
    
    #not needed now, but the logic for QT paths is so weird that I want this here for reference
    @Slot(QUrl, result=str)
    def qt_to_local_file(self, filePath) -> str:
        q_url = filePath
        if not isinstance(filePath, QUrl):
            q_url = QUrl(filePath)
        return QDir.toNativeSeparators(q_url.toLocalFile())
    
    @Slot(str)
    def set_text(self, text):
        if self.model is None:
            self.model = {}
        self.model['text'] = text
    
    @Slot(str)
    def set_audio(self, audio_path):
        if self.model is None:
            self.model = {}
        self.model['audio'] = audio_path

    @Slot("QVariantMap")
    def set_metadata(self, metadata):
        if self.model is None:
            self.model = {}
        self.model['metadata'] = metadata
    
    #dummy function for when we have the QML def but not Python backend
    @Slot(result=bool)
    def is_live(self) -> bool:
        print(self.test)
        return True