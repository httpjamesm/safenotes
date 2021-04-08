import tkinter as tk
import tkinter.messagebox
from utils.classes.aes_encryption import AesEncryption

import json,os
import settings

from utils.utils_f import utils

aes = AesEncryption()

class preferences():
    def __init__(self, userpass):
        self.userpass = userpass

    def killWindows(self):
        try:
            self.preferencesWindow.destroy()
        except:
            print("preferencesWindow already destroyed")
        
        try:
            self.passWindow.destroy()
        except:
            print("passWIndow already destroyed")

    def confirmDeletion(self):
        confirmation = tk.messagebox.askyesno("Are you sure?", "Wiping your data is irreversible, and will permanently delete all notes. Do you wish to proceed?")
        if confirmation != True:
            return
        
        with open("database.json","r+") as dbfile:
            #db = json.load(dbfile)
            dbfile.seek(0)
            dbfile.truncate(0)
            utils().write_json({
                "notes": []
            })


    def createWindow(self):
        self.preferencesWindow = tk.Tk()

        windowTitle = tk.Label(self.preferencesWindow,text="Settings",font=("Arial", 25))
        windowTitle.pack(side='top',anchor='nw')

        buttons = tk.Frame(self.preferencesWindow)
        buttons.pack()

        encryptionSection = tk.Label(self.preferencesWindow, text="Encryption", font=("Arial",16))
        encryptionSection.pack(in_=buttons,pady=5)

        changePassBttn = tk.Button(self.preferencesWindow,text="Change Password",command=self.passChangeGUI)
        changePassBttn.pack(in_=buttons)

        reencryptBttn = tk.Button(self.preferencesWindow, text="Re-Encrypt", command=self.reencryptGUI)
        reencryptBttn.pack(in_=buttons)

        dataSection = tk.Label(self.preferencesWindow, text="Data", font=("Arial",16))
        dataSection.pack(in_=buttons,pady=5)

        clearDataBttn = tk.Button(self.preferencesWindow, text="Wipe", command=self.confirmDeletion)
        clearDataBttn.pack(in_=buttons)

        self.preferencesWindow.title("SafeNotes - Preferences")
        self.preferencesWindow.minsize(512,512)
        self.preferencesWindow.mainloop()
    
    def passChangeGUI(self):
        self.passWindow = tk.Tk()

        title = tk.Label(self.passWindow, text="Change Password",font=("Arial", 25))
        title.pack()

        currentPassTxt = tk.Label(self.passWindow,text="Current Password")
        currentPassTxt.pack()
        currentPass = tk.Entry(self.passWindow, width=15)
        currentPass.configure(show="•")
        currentPass.pack()
        currentPass.focus()

        newPassTxt = tk.Label(self.passWindow,text="New Password")
        newPassTxt.pack()
        newPassOne = tk.Entry(self.passWindow, width=15)
        newPassOne.configure(show="•")
        newPassOne.pack()

        confirmPassTxt = tk.Label(self.passWindow,text="Confirm Password")
        confirmPassTxt.pack()
        confirmPass = tk.Entry(self.passWindow, width=15)
        confirmPass.configure(show="•")
        confirmPass.pack()

        changeButton = tk.Button(self.passWindow,text="Change",command=lambda: self.passCheck(currentPass.get(),newPassOne.get(),confirmPass.get()))
        changeButton.pack(pady=15)

        self.passWindow.title("Change Password")
        self.passWindow.mainloop()

    def passCheck(self, old, new, confirmation):
        key = aes.decrypt(settings.configdata["password"].encode(), old)        
        if new != confirmation:
            tk.messagebox.showerror("Password Mismatch","The new passwords do not match.")
            return
        
        try:
            utils().reencrypt(old,new)
        except Exception as e:
            tk.messagebox.showerror("Error", "An error occured while re-encrypting your note data.\n\n" + str(e))
            return
        
        tk.messagebox.showinfo("Password Changed", "Your encryption password was successfully changed.")
        
        self.passWindow.destroy()
        
        exit()

    def reencryptGUI(self):
        self.reencryptWindow = tk.Tk()

        infoText = tk.Label(self.reencryptWindow, text="Re-encryption will keep your data intact while changing the contents of the encrypted database file.")
        infoText.pack()

        self.passBox = tk.Entry(self.reencryptWindow,width=15)
        self.passBox.configure(show="•")
        self.passBox.pack(expand=True)
        self.passBox.focus()

        initiateBttn = tk.Button(self.reencryptWindow, text="Start Re-Encryption",command=lambda: self.reencrypt(self.passBox.get()))
        initiateBttn.pack()

        self.reencryptWindow.mainloop()
    
    def reencrypt(self,password):
        try:
            utils().reencrypt(password,password)
        except:
            tk.messagebox.showerror("Error","An unexpected error occured while re-encrypting your data.")
            return
        
        tk.messagebox.showinfo("Data Re-Encrypted", "Your data was successfully re-encrypted.")
        self.reencryptWindow.destroy()