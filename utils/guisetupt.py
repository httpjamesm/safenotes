"""import tkinter as tk
import tkinter.messagebox
from functools import partial
import json
from utils.classes.aes_encryption import AesEncryption
import settings
aes = AesEncryption()

class guisetup():
    def contentPopout(self,name,content):
        print(content)
        tkinter.messagebox.showinfo(name,content)

    def createGUI(self):
        try:
            dbfile = open("database.json","r")
        except:
            return
        
        #userpass = getpass("Enter your decryption password: ")
        userpass = "umqEr66^^"

        with open("database.json","r") as db:
            noteslist = []
            db = json.load(db)
            #print(db["notes"])
            try:
                userpass = aes.decrypt(settings.configdata["password"].encode(),userpass).decode('utf-8')
            except Exception as e:
                print(e)
                print("incorrect password.")
                return
            counter = len(db["notes"])
            contentlist = []
            for x in db["notes"]:
                noteslist.append(aes.decrypt(x["name"].encode(),userpass).decode('utf-8'))
                contentlist.append(aes.decrypt(x["content"].encode(),userpass).decode('utf-8'))
                counter -= 1
            noteslist.reverse()
            contentlist.reverse()

            userpass = None
        window = tk.Tk()
        
        title = tk.Label(text="SafeNotes",font=("Arial", 25))
        #title.pack(side="top",anchor="nw")
        
        #contentPopout = partial(self.contentPopout, noteslist[0],contentlist[0])
        #button1 = tk.Button(text=noteslist[0],command=contentPopout)
        #button1.pack()

        n = 5
        i = 3
        counter = -1
        print(noteslist)
        print(contentlist)
        e = [0 for x in range(len(noteslist))]
        #buttons = []
        for j in range(len(noteslist)):
            #print(counter)
            #b =
            e[j]  
            e[j] = tk.Button(window,text=noteslist[j],command=lambda: self.contentPopout(noteslist[j],contentlist[j]))
            e[j].grid(column=1)
            #e[j]()
            #counter += 1

        window.title("SafeNotes - Encrypted Note App")
        window.geometry("1024x1024")
        window.mainloop()"""