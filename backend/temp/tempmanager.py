from tempfile import TemporaryDirectory
from os import path
from uuid import uuid4

class TempFileManager:
    def __init__(self, name: str):
        self.__temp_dir = TemporaryDirectory(prefix=name)
    
    def new_file(self, type: str = None) -> str:
        pth = path.join(self.__temp_dir.name, str(uuid4()) + ('' if type is None else '.'+type))
        open(pth, 'w').close()
        return pth
         