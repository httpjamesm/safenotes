#!/usr/bin/python

import json,getpass,string,os
from utils.classes.aes_encryption import AesEncryption
#from utils.utils_f import utils

aes = AesEncryption()
alphabet = string.ascii_letters + string.punctuation + string.digits

def make_random_password(length, symbols):
    password = []
    for i in map(lambda x: int(len(symbols)*x/255.0), os.urandom(length)):
        password.append(symbols[i])
    return ''.join(password)


def setting():
    try:
        with open('settings.json','r') as json_file:
            configdata = json.load(json_file)
    except:
        try:
            file2 = open("settings.json", "xt")
        except:
            return
        
        userpass = getpass.getpass("Set your encryption password: ")

        emptysettingsdict = {
            "password": aes.encrypt(make_random_password(64,alphabet),userpass).decode('utf-8')
        }

        utils().write_json(emptysettingsdict,"settings.json")
        exit()
global configdata
def main():
    try:
        with open('settings.json','r') as json_file:
            configdata = json.load(json_file)
            print('congidata loaded')
    except Exception as e:
        print(e)
        return
try:
    with open('settings.json','r') as json_file:
        configdata = json.load(json_file)
        print('congidata loaded')
except Exception as e:
    print(e)


