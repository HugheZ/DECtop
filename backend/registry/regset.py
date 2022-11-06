from winreg import CreateKey, OpenKey, ConnectRegistry, HKEY_LOCAL_MACHINE, REG_SZ, SetValueEx, QueryValueEx
from os import path

__DEC_REG_US = 'SOFTWARE\\DECtalk Software\\DECtalk\\4.61\\US' #for dict location and such
__DEC_REG_LANGS = 'SOFTWARE\\DECtalk Software\\DECtalk\\Langs' #for installed dict (only US currently supported)
__DEC_REG = 'SOFTWARE\\DECtalk Software\\DECtalk\\4.61' #for installation details
__LANGUAGE = 'Language'
__MAIN_DICT = 'MainDict'
__VERSION = 'Version'
__DLL = 'dectalk.dll'
__DIC = 'dtalk_us.dic'
__DEFAULT_LANG = 'DefaultLang'
__US = 'US'
__COMPANY = 'Company'
__INSTALLER = 'Installer'
__LICENSES = 'Licenses'
__LIC_UPD_PWD = 'LicUpdPwd'
__LOCK_MGR = 'Lock_MGR'

__US_PROPS = {
    __LANGUAGE:'ENGLISH, US',
    __MAIN_DICT:'./'+__DIC,
    __VERSION:'DECtalk us version 4.61'
}

__LANGS_PROPS = {
    __DEFAULT_LANG: 'US',
    __US: 'ENGLISH, US'
}

__INSTALL_PROPS = {
    __COMPANY: 'DECTop',
    __INSTALLER: 'DECTop',
    __LICENSES: '',
    __LIC_UPD_PWD: '',
    __LOCK_MGR: '1'
}

# 1. HKEY_LOCAL_MACHINE\SOFTWARE\DECtalk Software\DECtalk\<version>\<langcode>, e.g US
# 2. Language=ENGLISH, US
# 3. MainDict=<location of main directory>
# 4. Version=DECtalk <langcode> version <version>

def __ensure_key(registry, values, reg_path):
    '''
    Sets key value by create to ensure the key exists.
    registry: actual connected registry
    values: dict of registry values
    reg_path: registry key to set
    '''
    key = CreateKey(registry, reg_path)
    for reg_key in values:
        SetValueEx(key, reg_key, 0, REG_SZ, values[reg_key])
    key.Close()

def setup_dec_reg(install_location=path.join(path.dirname(path.dirname(path.realpath(__file__))), 'includes', 'DTALK_US.DIC')):
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    __US_PROPS[__MAIN_DICT]=path.join(install_location, __DIC)
    
    __ensure_key(reg, __US_PROPS, __DEC_REG_US)
    __ensure_key(reg, __LANGS_PROPS, __DEC_REG_LANGS)
    __ensure_key(reg, __INSTALL_PROPS, __DEC_REG)
    
    reg.Close()

    print('Registry values set. Note that a valid encrypted license count and password must be supplied. DECTop does not handle DECtalk licenses, and so you must manually provide a valid license.')

def get_dll_reg():
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, __DEC_REG_US)
    retval = QueryValueEx(key, __MAIN_DICT)
    reg.Close()
    return None if retval is None or retval[1] != 1 else retval[0] #if none or tuple'd type is not 1 for STR return None, else return the STR path
