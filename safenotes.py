#!/usr/bin/python
import json, datetime,sys,string,os

from utils.classes.aes_encryption import AesEncryption
from utils.guisetup import guisetup
import settings

from utils.utils_f import utils

aes = AesEncryption()

class main():
    allargs = sys.argv[1:]
    if "--new" in allargs:
        allargs.remove("--new")
        name = allargs[0]
        content = ' '.join(allargs[1:])
        utils().createDbFile()
        utils().createSettingsFile()
        utils().addToDb(name,content)
        exit()
    if "--view" in allargs:
        utils().viewNotes()
        exit()

    if "--change" in allargs:
        utils().changePass()
        exit()
    
    
    guisetup().createGUI()