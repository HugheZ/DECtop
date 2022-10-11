from winreg import CreateKey, SetValue, ConnectRegistry, HKEY_LOCAL_MACHINE, REG_SZ
from os import path

__DEC_REG = 'SOFTWARE\\DECtalk Software\\DECtalk\\4.61\\US'
__LANGUAGE = 'Language'
__MAIN_DICT = 'MainDict'
__VERSION = 'Version'
__DLL = 'dectalk.dll'

__PROPS = {
    __LANGUAGE:'ENGLISH, US',
    __MAIN_DICT:'./'+__DLL,
    __VERSION:'DECtalk us version 4.61'
}

# 1. HKEY_LOCAL_MACHINE\SOFTWARE\DECtalk Software\DECtalk\<version>\<langcode>, e.g US
# 2. Language=ENGLISH, US
# 3. MainDict=<location of main directory>
# 4. Version=DECtalk <langcode> version <version>

def __ensure_key(key_value, registry_key):
    key = CreateKey(HKEY_LOCAL_MACHINE, __DEC_REG)
    SetValue(key, registry_key, REG_SZ, key_value)
    key.Close()

def setup_dec_reg(install_location=path.join(path.dirname(path.dirname(path.realpath(__file__))), 'includes')):
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    __PROPS[__MAIN_DICT]=path.join(install_location, __DLL)
    
    for reg_key in __PROPS:
        __ensure_key(reg_key, HKEY_LOCAL_MACHINE)
    
    reg.Close()
