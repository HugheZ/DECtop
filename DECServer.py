import argparse

from flask import Flask, request, Response, send_file
from backend.engine.dec import DECEngine
from backend.temp.tempmanager import TempFileManager
from backend.registry.regset import setup_dec_reg, get_dll_reg
from os import path

#local vars
__app = Flask(__name__)
__return_path = False
__engine = None
__temp = None

@__app.route('/run-tts', methods=['POST'])
def hello():
    payload = request.json
    if payload is None or not 'text' in payload:
        return Response('Required JSON body with at minimum \'text\' provided', 422)
    audio_path = __run_tts(payload['text'], payload.get('meta', None))

    if __return_path:
        return audio_path
    
    return send_file(audio_path)


def __run_tts(text: str, meta: dict) -> str:
    out_file = __temp.new_file('wav')
    __engine.runTTS(out_file, text)
    return out_file

def __setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launches and optionally configures the DECTop companion server and DECTalk library")
    parser.add_argument('-s', '--setup', dest='setup', action='store_true', default=False, required=False, help='If provided, sets up the DECtalk library by setting required registry values.')
    parser.add_argument('-d', '--directory', dest='directory', action='store', default=None, type=str, required=False, help='If --setup is specified, this flag specifies an optional dectalk main dictionary install location. Default <DECtop install location>/includes.')
    parser.add_argument('-r', '--returnpath', dest='return_path', action='store_true', default=False, required=False, help='If provided, sets the app to return file paths instead of data.')
    parser.add_argument('-p', '--port', dest='port', action='store', default=8080, required=False, help='If provided, the Flask port.')
    parser.add_argument('--host', dest='host', action='store', default='localhost', required=False, help='If provided, sets the Flask host.')

    return parser

#if run as script get args and setup, else just run
if __name__ == '__main__':
    parser = __setup_parser()
    args = parser.parse_args()

    if args.setup:
        if args.directory is not None:
            setup_dec_reg(args.directory)
        else:
            setup_dec_reg()
    __return_path = args.return_path

    dll_loc = path.join(path.dirname(get_dll_reg()), 'dectalk.dll')
    __engine = DECEngine(dll_loc)
    #have it's own temp dir just to better segment
    __temp = TempFileManager('DECServer') #link to obj so it can be deleted later
    __app.run(host=args.host, port=args.port, debug=False)
else:
    dll_loc = path.join(path.dirname(get_dll_reg()), 'dectalk.dll')
    __engine = DECEngine(dll_loc)
    #have it's own temp dir just to better segment
    __temp = TempFileManager('DECServer') #link to obj so it can be deleted later