import ctypes
from ctypes import wintypes
from ctypes import byref
# from math import max

NO_AUDIO = wintypes.DWORD(0x80000000)
WAV_FORMAT = wintypes.DWORD(0x00000004)
WAVE_MAPPER = ctypes.c_uint(-1)
START = 'TextToSpeechStartup'
PROCESS = ''
NULL_PTR = ctypes.c_void_p(None)
SPEAK_RATE_MIN = 75
SPEAK_RATE_MAX = 600
SPEAK_RATE_DEFAULT = 200

class DECEngine():
    def __init__(self, dll_path: str = 'dectalk.dll'):
        #dll_path = get_dll_reg()
        print(dll_path)
        self.dll = ctypes.WinDLL(dll_path)
        self.handle = ctypes.c_void_p()
        self.speak_rate = SPEAK_RATE_DEFAULT

        errcode = self.dll.TextToSpeechStartup(NULL_PTR, byref(self.handle), WAVE_MAPPER, NO_AUDIO)
        if errcode != 0:
            print('ERROR during DLL load: ' + str(errcode)) #TODO: currently getting 4 = ERROR_READING_DICTIONARY
        else:
            print('DLL loaded successfully')
    
    def set_speak_rate(self, val):
        if isinstance(val, int):
            self.speak_rate = self.__clamp(val)
        raise TypeError("Speaking rate must be int for words per minute")

        # setup_proto = ctypes.WINFUNCTYPE(wintypes.HWND, ctypes.c_void_p, ctypes.c_uint, wintypes.DWORD)
        # setup_API = setup_proto((START, self.dll), setup_params)
    
    def runTTS(self, outfile, text):
        if not isinstance(outfile, str) or not isinstance(text, str):
            raise TypeError("Arguments outfile and text must be strings")
        
        self.dll.TextToSpeechSetRate(self.handle, wintypes.DWORD(self.speak_rate))
        self.dll.TextToSpeechOpenWaveOutFile(self.handle, bytes(outfile, encoding='utf-8'), WAV_FORMAT)
        self.dll.TextToSpeechSpeak(self.handle, ctypes.c_char_p(bytes(text, encoding='utf-8')), ctypes.c_int(1)) #1 is forced
        self.dll.TextToSpeechSync(self.handle)
        self.dll.TextToSpeechCloseWaveOutFile(self.handle)

    def __clamp(self, val):
        self.speak_rate = max(SPEAK_RATE_MIN, min(SPEAK_RATE_MAX, val))

    def __del__(self):
        self.dll.TextToSpeechShutdown(self.handle)
        del self.dll


if __name__ == '__main__':
    dec = DECEngine()
    dec.runTTS('Hello aeiou world', 'test.wav')