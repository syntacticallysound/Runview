from winreg import *


keypath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"

def AddRunTag (runtag , exepath, keyname = ''):
    """ 
    
    Update Run Commands "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"
    App Paths
        tag.exe
            default = exe path

                        runtag   exepath              keyname (blank for default reg value)
                          ▼         ▼                     ▼
    Example: AddRunTag("Zoom","C:\\Path\\To\\Executable",'')
    
    """

    HKLM = HKEY_LOCAL_MACHINE

    try:
        keypath = OpenKeyEx(HKLM, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths",0,KEY_ALL_ACCESS)
        newKey = CreateKey(keypath,runtag+".exe")
        SetValueEx(newKey, keyname, 0, REG_SZ, str(exepath))
        if newKey:
            CloseKey(newKey)
        return True

    except Exception as e:
        print(e)

    return False

def DelRunTag (runtag):
    """ 
    
    Delete Run Commands "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"
    
    + App Paths
        tag.exe
    
    Example: DelRunTag(Notepad)
    
    """

    HKLM = HKEY_LOCAL_MACHINE

    try:
        keypath = OpenKeyEx(HKLM, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths",0,KEY_ALL_ACCESS)
        newKey = DeleteKey(keypath,runtag+".exe")
        if newKey:
            CloseKey(newKey)
        return True

    except Exception as e:
        print(e)

    return False

def AmendRunTag (oldruntag ,newruntag , exepath, keyname = ''):

    """
    
    Takes Exisiting Run Tag & Deletes from Regitry Path "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"
    App Paths
        tag.exe > Replaces With New Tag & Path
    
    App Paths
        tag.exe


    """
    
    DelRunTag(oldruntag[:-4])
    AddRunTag(newruntag,exepath,keyname="")

def AliasPaths():
    pathlist =[]
    key = OpenKey(HKEY_LOCAL_MACHINE, keypath, 0,KEY_ALL_ACCESS)
    countitems = 0
    for i in range(1000):
        try:
            
            guid = EnumKey(key, i)
            AliasKey = OpenKey(key, str(guid))
            (n, keyname, t) = EnumValue(AliasKey, 0)
            AliasPath = str(keyname)
            pathlist.append(AliasPath)
            
            CloseKey(AliasKey)
            countitems = countitems +1

        except error:
            pass
            
    
    return pathlist
    
def subkeys(key):
    i = 0
    while True:
        try:
            subkey = EnumKey(key, i)
            yield subkey
            i+=1
        except WindowsError as e:
            break

def traverse_registry_tree(hkey, keypath):
    countitems = 0
    reg_dict = {}
    key = OpenKey(hkey, keypath, 0,KEY_ALL_ACCESS)
    for subkeyname in subkeys(key):
        reg_dict[subkeyname] = subkeyname
        countitems = countitems + 1
    # print("number of tags = ",countitems)
    return reg_dict

def combine_key2path():
    combinator = {}
    alspath = []
    keypaths = [] 

    for e in AliasPaths():
        alspath.append(e)

    for e in traverse_registry_tree(HKEY_LOCAL_MACHINE, keypath):
        keypaths.append(e)
    
    combinator =dict(zip(keypaths,alspath))
    return combinator
