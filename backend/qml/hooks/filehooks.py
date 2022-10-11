from genericpath import isfile
from os import path
from shutil import rmtree
import json

def load_transcript(dectfile) -> dict:
    if not path.exists(dectfile):
        raise FileNotFoundError('File "' + str(dectfile) + '" does not exist.')
    if not path.isfile(dectfile) or not dectfile.lower().endswith('.dect'):
        raise ValueError('File "' + str(dectfile) + '" is not a .dect metadata file.')
    with open(dectfile, 'r') as f:
        return json.load(f)


def delete_audio_library(directory):
    if not path.exists(directory):
        raise FileNotFoundError('Directory "' + str(directory) + '" does not exist.')
    if not path.isdir(directory):
        raise ValueError('Directory "' + str(directory) + '" is not a directory.')
    rmtree(directory)