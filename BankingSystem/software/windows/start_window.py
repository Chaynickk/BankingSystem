from tkinter import *
from tkinter import ttk
from software.functions.enter import login

def start_window(root: Tk):
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(20): root.rowconfigure(index=r, weight=1)

    login_button = ttk.Button(text="Войти", command=login)
    login_button.grid(column=7, row=16, sticky=NSEW)

    email_entry = ttk.Entry()
    email_entry.grid(column=4, row=5,sticky=NSEW, columnspan=7)

    password_entry = ttk.Entry()
    password_entry.grid(column=4, row=8, sticky=NSEW, columnspan=7)

    email_label = ttk.Label(text="Почта", font=("Arial", 25))
    email_label.grid(column=3, row=5)