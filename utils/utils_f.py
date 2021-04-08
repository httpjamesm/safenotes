#!/usr/bin/python

import json,string,os
import settings
import datetime
from getpass import getpass
from utils.classes.aes_encryption import AesEncryption

import settings

aes = AesEncryption()

alphabet = string.ascii_letters + string.punctuation + string.digits

class utils():
    def make_random_password(self,length, symbols):
        password = []
        for i in map(lambda x: int(len(symbols)*x/255.0), os.urandom(length)):
            password.append(symbols[i])
        return ''.join(password)

    def write_json(self,data, filename="database.json"):
        # Helper function to write json data to the db file
        with open(filename,'w') as f:
            json.dump(data, f, indent=4)

    def addToDb(self,name,content):
        # Add a note to the db file
        userpass = getpass("Enter your encryption password: ")

        with open("database.json") as json_file:
            data = json.load(json_file)
            temp = data["notes"]
            encpass = aes.decrypt(settings.configdata["password"],userpass).decode('utf-8')
            encname = aes.encrypt(name,encpass)
            enccontent = aes.encrypt(content,encpass)
            enctime = aes.encrypt(str(datetime.datetime.now()),encpass)
            temp.append({
                "name":encname.decode('utf-8'),
                "time":enctime.decode('utf-8'),
                "content":enccontent.decode('utf-8')
            })
            encpass = None
        
        self.write_json(data)

    def createDbFile(self):
        # Create a db file if there is none
        try:
            file = open("database.json", "xt")
        except:
            return
        
        emptydict = {
            "notes":[]
        }
        self.write_json(emptydict)
    
    def createSettingsFile(self):
        try:
            file2 = open("settings.json", "xt")
        except:
            return
        
        userpass = getpass("Set your encryption password: ")

        emptysettingsdict = {
            "password": aes.encrypt(self.make_random_password(64,alphabet),userpass).decode('utf-8')
        }

        self.write_json(emptysettingsdict,"settings.json")
        exit()
    
    def viewNotes(self):
        try:
            dbfile = open("database.json","r")
        except:
            return
        
        userpass = getpass("Enter your decryption password: ")

        with open("database.json","r") as db:
            noteslist = []
            db = json.load(db)
            #print(db["notes"])
            #print(userpass)
            #print(settings.configdata["password"].encode())
            try:
                userpass = aes.decrypt(settings.configdata["password"].encode(),userpass).decode('utf-8')
            except:
                print("incorrect password.")
                return
            counter = len(db["notes"])
            for x in db["notes"]:
                noteslist.append(str(counter) + ". " + aes.decrypt(x["name"].encode(),userpass).decode('utf-8') + "\n\n" + aes.decrypt(x["content"].encode(),userpass).decode('utf-8'))
                counter -= 1
            noteslist.reverse()

            userpass = None
        print('\n\n'.join(noteslist))
        dbfile.close()

    def reencrypt(self, oldpass, newpass):
        # Re encrypts all content with a new password
        print('oldpass just got decrypted')
        oldpass = aes.decrypt(settings.configdata["password"].encode(),oldpass).decode('utf-8') # Decode the decryption password with the user's password
        plainpass = newpass # Store the new password in mem
        newpass = self.make_random_password(64,alphabet) # Generate the new encryption key
        with open("database.json","r+") as json_file:
            print('opened file')
            # Open the db file in read and write mode
            db = json.load(json_file) 
            allnotes = db["notes"] # load all encrypted content in mem
            newnotes = [{}] 
            for x in allnotes:
                # Decrypt
                decname = aes.decrypt(x["name"].encode(),oldpass).decode('utf-8')
                dectime = aes.decrypt(x["time"].encode(),oldpass).decode('utf-8')
                deccontent = aes.decrypt(x["content"].encode(),oldpass).decode('utf-8')
                # Re encrypt
                newname = aes.encrypt(decname,newpass).decode('utf-8')
                newtime = aes.encrypt(dectime,newpass).decode('utf-8')
                newcontent = aes.encrypt(deccontent,newpass).decode('utf-8')
                # Change content
                x["name"] = newname
                x["time"] = newtime
                x["content"] = newcontent
            json_file.seek(0)
            json_file.truncate(0) # Wipe file
            # Replace 
            self.write_json({
                "notes": allnotes
            })
        
        with open("settings.json","r+") as settings_file:
            # Change encrypted key in settings
            settings_file.seek(0)
            settings_file.truncate(0)
            self.write_json({
                "password":aes.encrypt(newpass,plainpass).decode('utf-8')
            },"settings.json")
        
        oldpass = None
        plainpass = None
        newpass = None
    
    def changePass(self):
        oldpass = getpass("Enter your old password: ")
        newpass = getpass("Enter your new password: ")
        self.reencrypt(oldpass, newpass)

        oldpass = None
        newpass = None
                



