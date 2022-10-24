from winreg import CreateKey, OpenKey, ConnectRegistry, HKEY_LOCAL_MACHINE, REG_SZ, SetValueEx, QueryValueEx
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

def __ensure_key(registry, key_name, key_value):
    '''
    Sets key value by create to ensure the key exists.
    registry: actual connected registry
    key_name: name of the key
    key_value: value of the key
    '''
    key = CreateKey(registry, __DEC_REG)
    SetValueEx(key, key_name, 0, REG_SZ, key_value)
    key.Close()

def setup_dec_reg(install_location=path.join(path.dirname(path.dirname(path.realpath(__file__))), 'includes')):
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    __PROPS[__MAIN_DICT]=path.join(install_location, __DLL)
    
    for reg_key in __PROPS:
        __ensure_key(reg, reg_key, __PROPS[reg_key])
    
    reg.Close()

def get_dll_reg():
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, __DEC_REG)
    retval = QueryValueEx(key, __MAIN_DICT)
    reg.Close()
    return None if retval is None or retval[1] != 1 else retval[0] #if none or tuple'd type is not 1 for STR return None, else return the STR path
