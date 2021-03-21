import tkinter as tk
import tkinter.messagebox
from functools import partial
import json
from utils.classes.aes_encryption import AesEncryption
from utils.utils_f import utils
import settings
import datetime

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
            data = json.load(json_file)
            temp = data["notes"]
            encname = aes.encrypt(name,self.userpass)
            enccontent = aes.encrypt(content,self.userpass)
            enctime = aes.encrypt(str(datetime.datetime.now()),self.userpass)
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
            self.window.destroy()
            self.noteWindow.destroy()
            self.loggedin(noteslist,contentlist)

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
        if decision == True:
            uipos = list(pos)[0]
            pos = len(allnotes) - list(pos)[0] - 1
            with open("database.json","r+") as dbfile:
                db = json.load(dbfile)
                notes = db["notes"]
                del notes[pos]
                del self.noteslist[pos]
                del self.contentlist[pos]
                dbfile.seek(0)
                dbfile.truncate(0) # Wipe file
                # Replace 
                self.write_json({
                    "notes": notes
                })
                print("Deleted note " + str(pos))
                self.lb.delete(uipos)
                self.contentDisplay.configure(state="normal")
                self.contentDisplay.delete(1.0,"end")
                self.contentDisplay.configure(state="disabled")
        return

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

        createButton = tk.Button(self.editWindow,text="Edit",command=lambda: self.editNote(cursor,self.nameBox.get(1.0,'end'),self.contentBox.get(1.0,'end')))
        createButton.pack(in_=contentFrame,pady=25)

        self.editWindow.title("Edit Secure Note")
        
        self.editWindow.geometry("512x512")
        self.editWindow.mainloop()     
        

    def editNote(self,cursor,newname,newcontent):
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
            
            #del notes[pos]
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
        self.contentDisplay.configure(state="normal")
        self.contentDisplay.delete(1.0,"end")
        self.contentDisplay.insert(1.0,secondlist[num])
        self.contentDisplay.configure(state="disabled")
        self.contentDisplay.pack(anchor='e',side="right",fill="x")

        self.timeLabel.configure(text="Created At: " + self.datelist[num])

    def getPassword(self,event=None):
        self.userpass = self.passBox.get()
        #print(self.passBox.get())
        with open("database.json","r") as db:
            noteslist = []
            db = json.load(db)
            #print(db["notes"])
            try:
                self.userpass = aes.decrypt(settings.configdata["password"].encode(),self.userpass).decode('utf-8')
            except Exception as e:
                tk.messagebox.showerror("Incorrect Password","The password you entered cannot decrypt note data.")
                print(e)
                return
            self.loginWindow.destroy()
            counter = len(db["notes"])
            contentlist = []
            self.datelist = []
            for x in db["notes"]:
                noteslist.append(aes.decrypt(x["name"].encode(),self.userpass).decode('utf-8'))
                contentlist.append(aes.decrypt(x["content"].encode(),self.userpass).decode('utf-8'))
                self.datelist.append(aes.decrypt(x["time"].encode(),self.userpass).decode('utf-8'))
                counter -= 1
            noteslist.reverse()
            contentlist.reverse()
            self.datelist.reverse()
            self.loggedin(noteslist,contentlist)
            #contentlist.reverse()

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
        self.newpassBox.bind('<Control-a>',self.lock_callback)

        self.finishButton = tk.Button(text="Finish Setup",command=lambda: self.finishSetup(self.newpassBox.get()))
        self.finishButton.pack(in_=windowMiddle)
        
        self.frWindow.geometry("512x512")
        self.frWindow.mainloop()

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

        title = tk.Label(text="SafeNotes",font=("Arial", 25),bg='black',fg='white')
        title.pack(side="top",in_=windowMiddle)

        self.passBox = tk.Entry(self.loginWindow,width=15,bg='black',fg='white')
        self.passBox.configure(show="•")
        self.passBox.pack(in_=windowMiddle)
        self.passBox.focus()
        self.passBox.bind('<Control-a>',self.callback)

        self.loginButton = tk.Button(text="Unlock",command=self.getPassword,bg='black',fg='white')
        self.loginButton.pack(in_=windowMiddle,pady=3)
        
        self.loginWindow.bind('<Return>', self.getPassword)

        self.loginWindow.configure(bg='black')
        self.loginWindow.geometry("512x512")
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
        
        self.userpass = None
        
        self.createGUI()
        return 'break'

    def loggedin(self,noteslist,contentlist):
        self.noteslist = noteslist
        self.contentlist = contentlist

        self.window = tk.Tk()
        self.contentDisplay = tk.Text(self.window)
        
        title = tk.Label(text="SafeNotes",font=("Arial", 25))

        #scrollBar = tk.Scrollbar(self.window, width = 100)
        self.lb = tk.Listbox(self.window,background='black', fg="white",width=60)
        self.lb.pack(side='left',fill="both",expand=True)
        for x in self.noteslist:
            self.lb.insert("end",x)
            self.lb.bind("<<ListboxSelect>>", lambda y: self.contentPopout(self.lb.curselection(),self.datelist,self.contentlist))

        self.window.title("SafeNotes - Encrypted Note App")
        #self.window.geometry("")

        self.right = tk.Frame(self.window)
        self.right.pack(side="top")

        #lb.curselection()

        newButton = tk.Button(text="New",command=self.newNote)
        newButton.pack(in_=self.right,fill="x",side='left')
        
        self.editbutton = tk.Button(text="Edit",command=lambda: self.editNoteGUI(self.lb.curselection(),self.lb.get(self.lb.curselection()),self.contentlist[list(self.lb.curselection())[0]]))
        self.editbutton.pack(in_=self.right,fill="x",side='left')
        self.deletebutton = tk.Button(text="Delete",command=lambda: self.deleteNote(self.lb.curselection(),self.noteslist))
        self.deletebutton.pack(in_=self.right,side='left')

        self.bottomNote = tk.Frame(self.window,bg='grey')
        self.bottomNote.pack(side="bottom",fill='y')

        self.timeLabel = tk.Label(self.window,bg='grey',fg='white')
        self.timeLabel.pack(in_=self.bottomNote,side='left')

        self.lockButton = tk.Button(self.window,text="Lock",bg='grey',command=lambda: self.lockApp())
        self.lockButton.pack(in_=self.bottomNote,side='right',anchor='se')

        self.window.bind('<Control-l>', self.lockApp)
        self.window.bind('<Control-n>', self.newNote)
        self.window.bind('<Control-e>', self.editNoteGUI)

        self.window.iconphoto(False,tk.PhotoImage(file='utils/icon.png'))
        self.window.configure(bg='grey')
        self.window.minsize(512,512)
        self.window.mainloop()

