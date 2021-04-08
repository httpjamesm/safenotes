import tkinter as tk
import tkinter.messagebox
from functools import partial
import json
import os
from utils.classes.aes_encryption import AesEncryption
from utils.utils_f import utils
from utils.settingspane import preferences
import settings
import datetime

from tkinter.filedialog import askopenfilename

aes = AesEncryption()


class guisetup():

    def write_json(self,data, filename="database.json"):
        # Helper function to write json data to the db file
        with open(filename,'w') as f:
            json.dump(data, f, indent=4)

    def addToDb(self,name,content):
        if "\n" in name:
            name = list(name)
            del name[-1]
            name = ''.join(name)
        # Add a note to the db file
        with open("database.json") as json_file:
            now = datetime.datetime.now()
            data = json.load(json_file)
            temp = data["notes"]
            encname = aes.encrypt(name,self.userpass)
            enccontent = aes.encrypt(content,self.userpass)
            enctime = aes.encrypt(str(now),self.userpass)
            temp.append({
                "name":encname.decode('utf-8'),
                "time":enctime.decode('utf-8'),
                "content":enccontent.decode('utf-8')
            })

            self.write_json(data)
            noteslist = []
            db = data
            counter = len(db["notes"])
            contentlist = []
            for x in db["notes"]:
                noteslist.append(aes.decrypt(x["name"].encode(),self.userpass).decode('utf-8'))
                contentlist.append(aes.decrypt(x["content"].encode(),self.userpass).decode('utf-8'))
                counter -= 1
            noteslist.reverse()
            contentlist.reverse()
            
            self.lb.insert(0,name)
            self.noteslist.insert(0,name)
            self.contentlist.insert(0,content)
            self.datelist.insert(0,str(now))

            try:
                self.noteWindow.destroy()
            except:
                return

    def newNote(self,event=None):
        self.noteWindow = tk.Tk()

        nameFrame = tk.Frame(self.noteWindow)
        nameFrame.pack(side="top",pady=15)
        nameText = tk.Label(self.noteWindow,text="Note Name")
        nameText.pack(in_=nameFrame)
        self.nameBox = tk.Text(self.noteWindow,height=1,width=50)
        self.nameBox.pack(in_=nameFrame)

        contentFrame = tk.Frame(self.noteWindow)
        contentFrame.pack(side="top",pady=30)
        contentText = tk.Label(self.noteWindow,text="Content")
        contentText.pack(in_=contentFrame)
        self.contentBox = tk.Text(self.noteWindow,height=15,width=50)
        self.contentBox.pack(in_=contentFrame)

        createButton = tk.Button(self.noteWindow,text="Create",command=lambda: self.addToDb(self.nameBox.get(1.0,'end'),self.contentBox.get(1.0,'end')))
        createButton.pack(in_=contentFrame,pady=25)

        self.noteWindow.title("New Secure Note")
        self.noteWindow.configure(bg='grey')
        self.noteWindow.geometry("512x512")
        self.noteWindow.mainloop()
        
    def deleteNote(self,pos,allnotes):
        decision = tk.messagebox.askyesno(title="Are you sure?", message="Note deletion is permanent, do you wish to proceed?")
        if decision is True:
            uipos = list(pos)[0]
            pos = len(allnotes) - list(pos)[0] - 1
            with open("database.json","r+") as dbfile:
                #db = json.load(dbfile)
                notes = db["notes"]
                del notes[pos]
                del self.noteslist[uipos]
                del self.contentlist[uipos]
                dbfile.seek(0)
                dbfile.truncate(0) # Wipe file
                # Replace 
                self.write_json({
                    "notes": notes
                })
                print("Deleted note " + str(pos) + "\nDeleted UI " + str(uipos))
                self.lb.delete(uipos)
                self.contentDisplay.configure(state="normal")
                self.contentDisplay.delete(1.0,"end")
                self.contentDisplay.configure(state="disabled")

    def decryptAttachment(self,fileName):
        aes.decrypt_file(fileName,self.userpass)
        print("file decrypted successfully, dropped.")
        tk.messagebox.showinfo("File Decrypted","The requested attachment was successfully decrypted into SafeNotes' working directory.")

    def viewAttachments(self,cursor):
        print(cursor)
        pos = len(self.noteslist) - cursor[0] - 1

        self.attachmentViewer = tk.Tk()
        self.attachmentViewer.title("Attachments for note " + str(cursor[0] + 1))

        with open("database.json","r+") as dbfile:
            db = json.load(dbfile)
            notes = db["notes"]
            try:
                attachmentslist = notes[pos]["attachments"]
            except:
                print("No attachments list was found--warning user")
                tk.messagebox.showerror("No Attachments","This note has no attachments to view.")
                self.attachmentViewer.destroy()
                return

        self.attachmentlb = tk.Listbox(self.attachmentViewer,background='black', fg="white",width=60)
        self.attachmentlb.pack(side='left',fill="both",expand=True)
        
        decryptFile = tk.Button(self.attachmentViewer,text="Decrypt File",command=lambda: self.decryptAttachment(self.attachmentlb.get(self.attachmentlb.curselection())))
        decryptFile.pack(side='bottom',fill="both",expand=True)
        for x in attachmentslist:
            self.attachmentlb.insert("end",x)
            #self.lb.bind("<<ListboxSelect>>", lambda y: self.contentPopout(self.lb.curselection(),self.datelist,self.contentlist))
        self.attachmentViewer.mainloop()

    def addAttachment(self,cursor):
        selectFile = tk.Tk()
        selectFile.withdraw()
        filepath = askopenfilename()
        selectFile.destroy()
        aes.encrypt_file(filepath, os.getcwd() + "/" + os.path.basename(filepath), self.userpass)
        print("Encrypted and dropped into " + os.getcwd() + "/" + os.path.basename(filepath) + ".enc")
        print("Locating and importing JSON into mem")
        with open("database.json","r+") as dbfile:
            db = json.load(dbfile)
            notes = db["notes"]
            pos = len(self.noteslist) - list(cursor)[0] - 1
            print("Database position defined as " + str(pos))
            try:
                attachmentslist = notes[pos]["attachments"]
            except:
                print("No attachments list was found--creating one")
                attachmentslist = []
            attachmentslist.append(os.getcwd() + "/" + os.path.basename(filepath) + ".enc")
            notes[pos]["attachments"] = attachmentslist
            print("Encrypted attachment path saved in mem database\nWriting to database")
            dbfile.seek(0)
            dbfile.truncate(0) # Wipe file
            self.write_json(db)
            print("We're done.")
            self.attachments.configure(text="Attachments: " + str('\n'.join(attachmentslist)))
            return os.getcwd() + "/" + os.path.basename(filepath) + ".enc"


    def editNoteGUI(self,cursor,currentName,currentContent,event=None):
        self.editWindow = tk.Tk()

        nameFrame = tk.Frame(self.editWindow)
        nameFrame.pack(side="top",pady=15)
        nameText = tk.Label(self.editWindow,text="Note Name")
        nameText.pack(in_=nameFrame)
        self.nameBox = tk.Text(self.editWindow,height=1,width=50)
        self.nameBox.pack(in_=nameFrame)
        self.nameBox.insert('end',currentName)

        contentFrame = tk.Frame(self.editWindow)
        contentFrame.pack(side="top",pady=30)
        contentText = tk.Label(self.editWindow,text="Content")
        contentText.pack(in_=contentFrame)
        self.contentBox = tk.Text(self.editWindow,height=15,width=50)
        self.contentBox.pack(in_=contentFrame)
        self.contentBox.insert('end',currentContent)

        with open("database.json","r+") as dbfile:
            db = json.load(dbfile)
            notes = db["notes"]
            pos = len(self.noteslist) - list(cursor)[0] - 1
            try:
                attachmentslist = notes[pos]["attachments"]
            except:
                attachmentslist = []

        self.attachments = tk.Label(self.editWindow, text="Attachments: " + str('\n'.join(attachmentslist)))
        self.attachments.pack(in_=contentFrame)

        createButton = tk.Button(self.editWindow,text="Edit",command=lambda: self.editNote(cursor,self.nameBox.get(1.0,'end'),self.contentBox.get(1.0,'end')))
        createButton.pack(in_=contentFrame)

        addAttachmentButton = tk.Button(self.editWindow,text="Add Attachment",command=lambda: self.addAttachment(cursor))
        addAttachmentButton.pack(in_=contentFrame)

        self.editWindow.title("Edit Secure Note")
        self.editWindow.configure(bg='grey')
        self.editWindow.geometry("512x512")
        self.editWindow.mainloop()     
        

    def editNote(self,cursor,newname,newcontent):
        if "\n" in newname:
            newname = list(newname)
            del newname[-1]
            newname = ''.join(newname)

        pos = cursor
        allnotes = self.noteslist
        uipos = list(pos)[0]
        pos = len(allnotes) - list(pos)[0] - 1
        print(pos)
        with open("database.json","r+") as dbfile:
            db = json.load(dbfile)
            notes = db["notes"]
            notes[pos]["name"] = aes.encrypt(newname,self.userpass).decode('utf-8')
            notes[pos]["content"] = aes.encrypt(newcontent,self.userpass).decode('utf-8')

            del self.noteslist[uipos]
            self.noteslist.insert(uipos,newname)

            del self.contentlist[uipos]
            self.contentlist.insert(uipos,newcontent)

            self.lb.delete(uipos)
            self.lb.insert(uipos,newname)
            
            dbfile.seek(0)
            dbfile.truncate(0) # Wipe file
            # Replace 
            self.write_json({
                "notes": notes
            })
            print("Edited note " + str(pos))
        
        self.editWindow.destroy()

    def contentPopout(self,num,thelist, secondlist):
        num = list(num)[0]
        self.noteTitle.configure(text=self.noteslist[num])
        self.contentDisplay.configure(state="normal")
        self.contentDisplay.delete(1.0,"end")
        self.contentDisplay.insert(1.0,secondlist[num])
        self.contentDisplay.configure(state="disabled")
        self.contentDisplay.pack(anchor='e',side="right",fill="x")

        self.timeLabel.configure(text="Created At: " + self.datelist[num])

    def getPassword(self,event=None):
        self.userpass = self.passBox.get()
        with open("database.json","r") as db:
            noteslist = []
            db = json.load(db)
            try:
                self.userpass = aes.decrypt(settings.configdata["password"].encode(),self.userpass).decode('utf-8')
            except Exception as e:
                self.passBox.delete(0,'end')
                tk.messagebox.showerror("Incorrect Password","The password you entered cannot decrypt note data.")
                print(e)
                return
            #print(self.userpass)
            self.loginWindow.destroy()
            counter = len(db["notes"])
            contentlist = []
            self.datelist = []
            for x in db["notes"]:
                #try:
                noteslist.append(aes.decrypt(x["name"].encode(),self.userpass).decode('utf-8'))
                contentlist.append(aes.decrypt(x["content"].encode(),self.userpass).decode('utf-8'))
                self.datelist.append(aes.decrypt(x["time"].encode(),self.userpass).decode('utf-8'))
                #except:
                #    noteslist.append("🔐 Encrypted")
                #    contentlist.append("[SYSTEM] This note could not be decrypted due to an unexpected error.\n\nIs the database.json file corrupted?")
                #    self.datelist.append("Decryption Error.XXXXXX")
                counter -= 1
            noteslist.reverse()
            contentlist.reverse()
            self.datelist.reverse()
            self.loggedin(noteslist,contentlist)

            self.userpass = None
    def callback(self,event):
        # Ctrl + A function

        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')
        return 'break'

    def finishSetup(self,password):
        import string
        alphabet = string.ascii_letters + string.punctuation + string.digits
        userpass = password
        try:
            file2 = open("settings.json", "xt")
        except:
            return
    
        emptysettingsdict = {
            "password": aes.encrypt(utils().make_random_password(64,alphabet),userpass).decode('utf-8')
        }

        utils().write_json(emptysettingsdict,"settings.json")

        tkinter.messagebox.showinfo(title="Setup Finished", message="SafeNotes is setup, but you need to restart the app to use it. Please do so.")
        exit()

    def firstRun(self):

        utils().createDbFile()
        self.frWindow = tk.Tk()
        windowMiddle = tk.Frame(self.frWindow)
        windowMiddle.pack(expand="yes",anchor="center")

        title = tk.Label(self.frWindow,text="SafeNotes Setup",font=("Arial", 25))
        title.pack(side="top",in_=windowMiddle)
        
        newPassTitle = tk.Label(self.frWindow,text="Set your encryption password.")
        newPassTitle.pack(in_=windowMiddle)

        self.newpassBox = tk.Entry(self.frWindow, width=15)
        self.newpassBox.configure(show="•")
        self.newpassBox.pack(in_=windowMiddle)

        self.finishButton = tk.Button(text="Finish Setup",command=lambda: self.finishSetup(self.newpassBox.get()))
        self.finishButton.pack(in_=windowMiddle)
        
        self.frWindow.geometry("512x512")
        self.frWindow.mainloop()

    def showAbout(self):
        self.infoText.configure(fg='white',text="SafeNotes is an encrypted note-taking app which protects all user data with industry leading AES-256 bit encryption.\nEnter your password above to view your notes. If you've forgotten your password, you must delete your database and settings file to re-initiate setup.")

    def createGUI(self):
        try:
            dbfile = open("database.json","r")
            settingsfile = open("settings.json","r")
        except:
            self.firstRun()
            return
        
        self.loginWindow = tk.Tk()
        
        windowMiddle = tk.Frame(self.loginWindow,bg='black')
        windowMiddle.pack(expand="yes",anchor="center")
        bottomRight = tk.Frame(self.loginWindow,bg='black')
        bottomRight.pack(expand='no',anchor='se')

        title = tk.Label(text="SafeNotes",font=("Arial", 25),bg='black',fg='white')
        title.pack(side="top",in_=windowMiddle)

        self.passBox = tk.Entry(self.loginWindow,width=15,bg='black',fg='white')
        self.passBox.configure(show="•")
        self.passBox.pack(in_=windowMiddle,expand=True)
        self.passBox.focus()
        self.passBox.bind('<Control-a>',self.callback)

        self.loginButton = tk.Button(text="Unlock",command=self.getPassword,bg='black',fg='white')
        self.loginButton.pack(in_=windowMiddle,pady=3)
        info = tk.Button(self.loginWindow,text='?',bg='black',fg='white',command=self.showAbout)
        info.pack(in_=bottomRight)
        self.infoText = tk.Label(bg='black')
        self.infoText.pack(in_=windowMiddle)

        self.loginWindow.bind('<Return>', self.getPassword)

        self.loginWindow.configure(bg='black')
        self.loginWindow.minsize(512,512)
        self.loginWindow.title("SafeNotes - Locked")
        self.loginWindow.mainloop()        
    
    def lockApp(self,event=None):
        self.window.destroy()
        try:
            self.noteWindow.destroy()
        except:
            print("noteWindow already destroyed")
        try:
            self.editNoteGUI.destroy()
        except:
            print("editNoteGUI already destroyed")
        
        preferences().killWindows()

        self.userpass = None
        
        self.createGUI()
        return 'break'

    def dupe(self,pos):
        self.addToDb(self.lb.get(self.lb.curselection()),self.contentlist[list(pos)[0]])
        print("Duplicated note " + str(pos))
        
    def loggedin(self,noteslist,contentlist):
        self.noteslist = noteslist
        self.contentlist = contentlist

        self.window = tk.Tk()
        self.contentDisplay = tk.Text(self.window)
        
        title = tk.Label(text="SafeNotes",font=("Arial", 25))

        self.lb = tk.Listbox(self.window,background='black', fg="white",width=60)
        self.lb.pack(side='left',fill="both",expand=True)
        for x in self.noteslist:
            self.lb.insert("end",x)
            self.lb.bind("<<ListboxSelect>>", lambda y: self.contentPopout(self.lb.curselection(),self.datelist,self.contentlist))

        self.window.title("SafeNotes - Encrypted Note App")

        self.right = tk.Frame(self.window)
        self.right.pack(side="top")

        newButton = tk.Button(text="New",command=self.newNote)
        newButton.pack(in_=self.right,fill="x",side='left')
        
        topright = tk.Frame(self.window)
        topright.pack(anchor='ne',side='top')
        settingsButton = tk.Button(text='⚙',command=lambda: preferences(self.userpass).createWindow())
        settingsButton.pack(in_=topright)

        self.editbutton = tk.Button(text="Edit",command=lambda: self.editNoteGUI(self.lb.curselection(),self.lb.get(self.lb.curselection()),self.contentlist[list(self.lb.curselection())[0]]))
        self.editbutton.pack(in_=self.right,fill="x",side='left')
        self.dupeButton = tk.Button(text="Duplicate",command=lambda: self.dupe(self.lb.curselection()))
        self.dupeButton.pack(in_=self.right,fill='x',side='left')
        self.deletebutton = tk.Button(text="Delete",command=lambda: self.deleteNote(self.lb.curselection(),self.noteslist))
        self.deletebutton.pack(in_=self.right,side='left')

        self.noteTitle = tk.Label(self.window)
        self.noteTitle.pack(side="top",pady=10)

        self.bottomNote = tk.Frame(self.window,bg='grey')
        self.bottomNote.pack(side="bottom",fill='y')

        self.timeLabel = tk.Label(self.window,bg='grey',fg='white')
        self.timeLabel.pack(in_=self.bottomNote,side='left')

        self.lockButton = tk.Button(self.window,text="Lock",command=self.lockApp)
        self.lockButton.pack(in_=self.bottomNote,side='right',anchor='se')

        viewAttachments = tk.Button(self.window,text="Attachments",command=lambda: self.viewAttachments(self.lb.curselection()))
        viewAttachments.pack(in_=self.bottomNote,side='right',anchor='se')
        self.window.bind('<Control-l>', self.lockApp)
        self.window.bind('<Control-n>', self.newNote)
        self.window.bind('<Control-e>',lambda p: self.editNoteGUI(self.lb.curselection(),self.lb.get(self.lb.curselection()),self.contentlist[list(self.lb.curselection())[0]]))
        self.window.bind('<Control-comma>', lambda d: preferences(self.userpass).createWindow())

        self.window.iconphoto(False,tk.PhotoImage(file='utils/icon.png'))
        self.window.configure(bg='grey')
        self.window.minsize(512,512)
        self.window.mainloop()