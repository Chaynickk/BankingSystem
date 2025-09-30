from tkinter import *
from tkinter import ttk
from software.functions.enter import login


def login_frame(window: Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=BOTH)
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(20): root.rowconfigure(index=r, weight=1)


    email_entry = ttk.Entry(root, font=("Arial", 23))
    email_entry.grid(column=4, row=5,sticky=NSEW, columnspan=7)

    email_label = ttk.Label(root, text="Почта", font=("Arial", 25))
    email_label.grid(column=3, row=5)

    password_entry = ttk.Entry(root, font=("Arial", 24))
    password_entry.grid(column=4, row=8, sticky=NSEW, columnspan=7)

    email_label = ttk.Label(root, text="Пароль", font=("Arial", 25))
    email_label.grid(column=3, row=8)

    error_label = ttk.Label(root, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=7, row=12)


    login_button = ttk.Button(root,
                              text="Войти",
                              command=lambda: login(email=email_entry.get(),
                                                    password=password_entry.get(),
                                                    label=error_label,
                                                    func=lambda: client_frame(window, root)))
    login_button.grid(column=7, row=16, sticky=NSEW)

    registration_button = ttk.Button(root, text="Зарегестрироватся", command=lambda: registrations_frame(window, root))
    registration_button.grid(column=0, row=0, sticky=NSEW)

def registrations_frame(window: Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=BOTH)
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(100): root.rowconfigure(index=r, weight=1)

    first_name_entry = ttk.Entry(root, font=("Arial", 23))
    first_name_entry.grid(column=4, row=10, sticky=NSEW, columnspan=7)

    first_name_label = ttk.Label(root, text="Имя", font=("Arial", 23))
    first_name_label.grid(column=3, row=10)

    last_name_entry = ttk.Entry(root, font=("Arial", 23))
    last_name_entry.grid(column=4, row=15, sticky=NSEW, columnspan=7)

    last_name_label = ttk.Label(root, text="Фамилия", font=("Arial", 23))
    last_name_label.grid(column=3, row=15)

    patronymic_entry = ttk.Entry(root, font=("Arial", 23))
    patronymic_entry.grid(column=4, row=20, sticky=NSEW, columnspan=7)

    patronymic_label = ttk.Label(root, text="Отчество", justify=CENTER, font=("Arial", 23))
    patronymic_label.grid(column=3, row=20)

    email_entry = ttk.Entry(root, font=("Arial", 23))
    email_entry.grid(column=4, row=25, sticky=NSEW, columnspan=7)

    email_label = ttk.Label(root, text="Почта", font=("Arial", 23))
    email_label.grid(column=3, row=25)

    phone_number_entry = ttk.Entry(root, font=("Arial", 23))
    phone_number_entry.grid(column=4, row=30, sticky=NSEW, columnspan=7)

    phone_number_label = ttk.Label(root, text="Email", font=("Arial", 23))
    phone_number_label.grid(column=3, row=30)

    password_entry = ttk.Entry(root, font=("Arial", 23))
    password_entry.grid(column=4, row=35, sticky=NSEW, columnspan=7)

    password_label = ttk.Label(root, text="Пароль", font=("Arial", 23))
    password_label.grid(column=3, row=35)

    login_button = ttk.Button(root, text="Войти", command=lambda: login_frame(window, root))
    login_button.grid(column=0, row=0, sticky=NSEW, rowspan=6, columnspan=2)

    error_label = ttk.Label(root, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=7, row=12)

    login_button = ttk.Button(root,
                              text="Войти",
                              command=lambda: login(email=email_entry.get(),
                                                    password=password_entry.get(),
                                                    label=error_label,
                                                    func=lambda: client_frame(window, root)))
    login_button.grid(column=7, row=80, sticky=NSEW, rowspan=6)



def client_frame(window: Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=BOTH)
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(20): root.rowconfigure(index=r, weight=1)

    error_label = ttk.Label(root, text="dfgsdfg", foreground="red", font=("Arial", 20))
    error_label.grid(column=7, row=12)

