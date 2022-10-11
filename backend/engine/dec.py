import ctypes
from ctypes import wintypes
from ctypes import byref

NO_AUDIO = wintypes.DWORD(0x80000000)
WAV_FORMAT = wintypes.DWORD(0x00000004)
WAVE_MAPPER = ctypes.c_uint(-1)
START = 'TextToSpeechStartup'
PROCESS = ''
NULL_PTR = ctypes.c_void_p(None)

class DECEngine():
    def __init__(self):
        self.dll = ctypes.WinDLL('dectalk.dll')
        self.handle = ctypes.c_void_p()

        errcode = self.dll.TextToSpeechStartup(NULL_PTR, byref(self.handle), WAVE_MAPPER, NO_AUDIO)
        if errcode != 0:
            print('ERROR during DLL load: ' + str(errcode))
        else:
            print('DLL loaded successfully')

        # setup_proto = ctypes.WINFUNCTYPE(wintypes.HWND, ctypes.c_void_p, ctypes.c_uint, wintypes.DWORD)
        # setup_API = setup_proto((START, self.dll), setup_params)
    
    def runTTS(self, outfile, text):
        if not isinstance(outfile, str) or not isinstance(text, str):
            raise TypeError("Arguments outfile and text must be strings")
        
        self.dll.TextToSpeechOpenWaveOutFile(self.handle, bytes(outfile), WAV_FORMAT)
        self.dll.TextToSpeechSpeak(self.handle, ctypes.c_char_p(text), ctypes.c_int(1)) #1 is forced
        self.dll.TextToSpeechSync(self.handle)
        self.dll.TextToSpeechCloseWaveOutFile(self.handle)

    def __del__(self):
        self.dll.TextToSpeechShutdown(self.handle)
        del self.dll

#TODO: remember, when copying dectalk.dll to directory, it will require a few registry keys on windows to run:
#
# 5. also requires python 32 bit or full recompilation, and I ain't doin' that


if __name__ == '__main__':
    dec = DECEngine()
    dec.runTTS('Hello aeiou world', 'test.wav')