import tkinter as tk
import tkinter.messagebox
from utils.classes.aes_encryption import AesEncryption

import json,os
import settings

from utils.utils_f import utils

aes = AesEncryption()

class preferences():
    def createWindow(self):
        self.preferencesWindow = tk.Tk()

        windowTitle = tk.Label(self.preferencesWindow,text="Settings",font=("Arial", 25))
        windowTitle.pack(side='top',anchor='nw')

        buttons = tk.Frame(self.preferencesWindow)
        buttons.pack()

        changePassBttn = tk.Button(self.preferencesWindow,text="Change Password",command=self.passChangeGUI)
        changePassBttn.pack(in_=buttons)

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