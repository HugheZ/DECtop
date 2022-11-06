from os import path, makedirs, remove
from shutil import rmtree, move
from zipfile import BadZipFile, ZipFile, is_zipfile
from PySide6.QtCore import Slot, QObject, QUrl, QDir
from PySide6.QtQml import QmlElement
from ..temp.tempmanager import TempFileManager
from .dec import DECEngine
import json
import requests


QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_NAME = 'DECtop'
SIDECAR_URL = 'http://localhost:8080'

MODEL_PART = 'model.json'
AUDIO_PART = 'audio.wav'


@QmlElement
class QmlBackend(QObject):

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.model = None
        self.save_path = None
        self.name = None
        self.__temp = TempFileManager('DECTop') #link to obj so it can be deleted later in __del__

    @Slot(QUrl, result=dict)
    def load_transcript(self, dectfile_qurl) -> None:
        '''
        Loads a transcript file.
        Expects dectfile to be the full path to the .dect file
        '''
        dectfile = self.qt_to_local_file(dectfile_qurl)
        self.__check_file(dectfile)

        #unzip dect to get json and cached audio
        with ZipFile(dectfile) as zip:
            with zip.open(MODEL_PART, 'r') as f:
                self.model = json.loads(f.read().decode('utf-8')) #wack, zipfile can't just be fed to json.load since it it's bytes
            #if no audio, handle gracefully
            if AUDIO_PART in zip.namelist():
                with zip.open(AUDIO_PART, 'r') as audio, open(self.__cached_audio_file(), 'wb') as audio_cache:
                    audio_cache.write(audio.read())

        self.save_path = dectfile
        self.name = path.splitext(path.basename(self.save_path))[0]
    
    @Slot(QUrl, result=QUrl)
    def load_audio_only(self, dectfile_qurl) -> QUrl:
        '''
        In contrast to load_transcript, this loads only the audio file to let the user play files without editing
        '''
        dectfile = self.qt_to_local_file(dectfile_qurl)
        self.__check_file(dectfile)
        #unzip dect to get cached audio

        with ZipFile(dectfile) as zip:
            cache_loc = self.__cached_audio_file()
            #if no audio, handle gracefully
            if AUDIO_PART in zip.namelist():
                with zip.open(AUDIO_PART, 'r') as audio, open(cache_loc, 'wb') as audio_cache:
                    audio_cache.write(audio.read())
                    return QUrl.fromLocalFile(cache_loc)
            return None #not in zip, nothing to do, perhaps TODO return error?

    @Slot(QUrl)
    def delete_audio_library(self, dectfile_qurl) -> None:
        '''
        Deletes a .dect archive.
        The dect_file argument must be a full path to a .dect archive
        '''
        dectfile = self.qt_to_local_file(dectfile_qurl)
        self.__check_file(dectfile)
        remove(dectfile)
        self.model = None
    
    @Slot(result=QUrl)
    def run_TTS(self) -> QUrl:
        text = self.model.get('text')
        if text is None or text == '':
            return None
        #NOTE cannot use TemporaryFile since we want a path, and we can't double-open the file.
        file_path = self.__cached_audio_file()

        #RUN YEEHAW
        self.__call_TTS_sidecar(file_path)

        #correctly ran, convert to QUrl path for UI
        return QUrl.fromLocalFile(file_path)
    
    def __call_TTS_sidecar(self, file_path: str):
        '''
        Calls the sidecar server for TTS translation

        file_path: path to move response data to
        '''
        res = requests.post(SIDECAR_URL + '/run-tts',
            json={
                'text': self.model['text'],
                'meta': self.model.get('metadata')
            }
        )

        #on failure abort
        res.raise_for_status()
        if res.status_code > 299:
            raise requests.exceptions.HTTPError('Non 200 Success: ' + str(res.status_code))
        
        #success, map
        content_type = res.headers['Content-Type']
        if content_type == 'application/json': #why can't mimetypes just have a nice enumeration of constants?
            js = res.json()
            if js.get('path', None) is None:
                raise requests.exceptions.HTTPError('Response did not have path data in JSON')
            move(js['path'], file_path)
            return
        elif content_type == 'audio/wav' or content_type == 'audio/x-wav':
            #assume is raw wav file
            with open(file_path, 'wb') as f:
                f.write(res.content)
            return
        else:
            raise requests.exceptions.HTTPError('Response was successful but was neither JSON nor WAV return type: ' + content_type)
    
    @Slot(result="QVariantMap")
    def get_model(self) -> dict:
        '''
        Returns the underlying model as a QVariantMap. Primarily useful to see if this is a loaded file or in-memory new.
        '''
        return self.model

    @Slot(result=str)
    def get_name(self) -> str:
        return self.name
    
    @Slot(result=str)
    def get_save_path(self) -> str:
        return self.save_path
    
    #handy getter for qurl-formatted URL, since doing that in QML is stupidly weird
    @Slot(result=QUrl)
    def get_cached_audio(self) -> QUrl:
        '''
        Retrieves the model's cached audio file as a path, else None
        '''
        cached_audio = self.__cached_audio_file()
        if path.exists(cached_audio) and path.isfile(cached_audio):
            return QUrl.fromLocalFile(cached_audio)
        return None
    
    # if file_path and name is None, ignore the input and assume it's a 'save' not a 'saveAs'
    # note that file_path should be to the base save dir. The 'name' parameter is treated as both final directory as well as file names
    @Slot(str, str, result=bool)
    def save_model(self, file_path, name) -> bool:
        '''
        Saves the underlying model (if exists) to the specified directory and name.
        
        file_path: path to the save directory, which is the application directory

        name: name to use for the final library, expected to not have any extension, i.e. a human-readable name
        '''
        if file_path is not None and name is not None:
            # filePath is a qurl, so it needs to be normalized
            to_host_path = self.qt_to_local_file(file_path)
            # check to make sure the dirs actually exist
            makedirs(to_host_path, exist_ok=True)
            #set save paths to file
            self.save_path = path.join(to_host_path, name + '.dect')
            self.name = name
        # don't check dirs on 'save', since we know we have a file then. 'saveAs' is the only necessary time
        

        # dirs exist, now open zip, dump the model, and move the audio IF PRESENT
        with ZipFile(self.save_path, 'w') as zip:
            with zip.open(MODEL_PART, 'w') as f:
                f.write(bytes(json.dumps(self.model), 'utf-8'))
            # if no audio, handle gracefully
            audio_to_save = self.__cached_audio_file()
            if path.exists(audio_to_save):
                with zip.open(AUDIO_PART, 'w') as audio, open(audio_to_save, 'rb') as audio_cache:
                    audio.write(audio_cache.read())
        
        #TODO: test this
    
    def __cached_audio_file(self) -> str:
        return path.join(self.__temp.get_app_dir(), AUDIO_PART)
    
    def __check_file(self, file):
        '''
        Checks that a given path exists, is a file, and is a .dect archive, else throw an exception
        '''
        if file is None:
            raise ValueError('File given is None')
        if not path.exists(file):
            raise FileNotFoundError('File "' + file + '" does not exist.')
        if not path.isfile(file) or not file.lower().endswith('.dect'):
            raise ValueError('File "' + file + '" is not a .dect library file.')
        if not is_zipfile(file):
            raise BadZipFile('File "' + file + '" is not a zip-compressed archive.')
    
    #not needed now, but the logic for QT paths is so weird that I want this here for reference
    @Slot(QUrl, result=str)
    def qt_to_local_file(self, filePath) -> str:
        '''
        Translates a QUrl to a local filesystem url
        '''
        q_url = filePath
        if not isinstance(filePath, QUrl):
            q_url = QUrl(filePath)
        return QDir.toNativeSeparators(q_url.toLocalFile())
    
    @Slot(str)
    def set_text(self, text):
        if self.model is None:
            self.model = {}
        self.model['text'] = text

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