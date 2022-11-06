from tempfile import TemporaryDirectory
from os import path, mkdir
from uuid import uuid4

class TempFileManager:
    def __init__(self, name: str):
        self.__temp_dir = TemporaryDirectory(prefix=name)
        self.__app_dir = path.join(self.__temp_dir.name, name)
        mkdir(self.__app_dir)
    
    def new_file(self, type: str = None) -> str:
        pth = path.join(self.__temp_dir.name, str(uuid4()) + ('' if type is None else '.'+type))
        open(pth, 'w').close()
        return pth
    
    def get_app_dir(self) -> str:
        return self.__app_dir
        
         