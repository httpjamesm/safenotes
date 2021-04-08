import tkinter as Tkinter

def make_menu(w):
    global the_menu
    the_menu = Tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

t = Tkinter.Tk()
make_menu(t)

e1 = Tkinter.Entry(); e1.pack()
e2 = Tkinter.Entry(); e2.pack()
e1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

t.mainloop()
