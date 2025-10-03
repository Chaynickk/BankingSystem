import tkinter as tk
from tkinter import ttk

from software.api_requests.accouts import request_get_accounts
from software.functions.enter import login, registration


def login_frame(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(20): root.rowconfigure(index=r, weight=1)


    email_entry = ttk.Entry(root, font=("Arial", 23))
    email_entry.grid(column=4, row=5,sticky=tk.NSEW, columnspan=7)

    email_label = ttk.Label(root, text="Почта", font=("Arial", 25))
    email_label.grid(column=3, row=5)

    password_entry = ttk.Entry(root, font=("Arial", 24))
    password_entry.grid(column=4, row=8, sticky=tk.NSEW, columnspan=7)

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
    login_button.grid(column=7, row=16, sticky=tk.NSEW)

    registration_button = ttk.Button(root, text="Зарегестрироватся", command=lambda: registrations_frame(window, root))
    registration_button.grid(column=0, row=0, sticky=tk.NSEW)

def registrations_frame(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    for c in range(15): root.columnconfigure(index=c, weight=1)
    for r in range(100): root.rowconfigure(index=r, weight=1)

    first_name_entry = ttk.Entry(root, font=("Arial", 23))
    first_name_entry.grid(column=4, row=10, sticky=tk.NSEW, columnspan=7)

    first_name_label = ttk.Label(root, text="Имя", font=("Arial", 23))
    first_name_label.grid(column=3, row=10)

    last_name_entry = ttk.Entry(root, font=("Arial", 23))
    last_name_entry.grid(column=4, row=15, sticky=tk.NSEW, columnspan=7)

    last_name_label = ttk.Label(root, text="Фамилия", font=("Arial", 23))
    last_name_label.grid(column=3, row=15)

    patronymic_entry = ttk.Entry(root, font=("Arial", 23))
    patronymic_entry.grid(column=4, row=20, sticky=tk.NSEW, columnspan=7)

    patronymic_label = ttk.Label(root, text="Отчество", justify=tk.CENTER, font=("Arial", 23))
    patronymic_label.grid(column=3, row=20)

    email_entry = ttk.Entry(root, font=("Arial", 23))
    email_entry.grid(column=4, row=25, sticky=tk.NSEW, columnspan=7)

    email_label = ttk.Label(root, text="Email", font=("Arial", 23))
    email_label.grid(column=3, row=25)

    phone_number_entry = ttk.Entry(root, font=("Arial", 23))
    phone_number_entry.grid(column=4, row=30, sticky=tk.NSEW, columnspan=7)

    phone_number_label = ttk.Label(root, text="Телефон", font=("Arial", 23))
    phone_number_label.grid(column=3, row=30)

    password_entry = ttk.Entry(root, font=("Arial", 23))
    password_entry.grid(column=4, row=35, sticky=tk.NSEW, columnspan=7)

    password_label = ttk.Label(root, text="Пароль", font=("Arial", 23))
    password_label.grid(column=3, row=35)

    login_button = ttk.Button(root, text="Войти", command=lambda: login_frame(window, root))
    login_button.grid(column=0, row=0, sticky=tk.NSEW, rowspan=6, columnspan=2)

    error_label = ttk.Label(root, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=7, row=60)

    registration_button = ttk.Button(root,
                              text="Зарегистрироваться",
                              command=lambda: registration(email=email_entry.get(),
                                                           first_name=first_name_entry.get(),
                                                           last_name=last_name_entry.get(),
                                                           patronymic=patronymic_entry.get(),
                                                           phone_number=phone_number_entry.get(),
                                                           password=password_entry.get(),
                                                           label=error_label,
                                                           func=lambda: client_frame(window, root)))
    registration_button.grid(column=7, row=80, sticky=tk.NSEW, rowspan=6)

def client_frame(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    accounts = request_get_accounts()

    root = tk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    for c in range(10): root.columnconfigure(index=c, weight=1)
    for r in range(10): root.rowconfigure(index=r, weight=1)

    accounts_frame = tk.Frame(root)
    accounts_frame.grid(column=2, row=0, columnspan=9, rowspan=10, sticky=tk.NSEW)
    for c in range(7):
        if c % 2 == 0:
            accounts_frame.columnconfigure(index=c, weight=1)
        else:
            accounts_frame.columnconfigure(index=c, weight=6)
    for r in range(9):
        if r % 2 == 0:
            accounts_frame.rowconfigure(index=r, weight=1)
        else:
            accounts_frame.rowconfigure(index=r, weight=4)

    len = 4

    r = 1
    c = 1
    while len > 0:


        new_frame = tk.Frame(accounts_frame, bg="#d5d5d5")
        new_frame.grid(row=r, column=c, sticky=tk.NSEW)

        len -= 1

        if c + 2 >= 7:
            c = 1
            r+=2
        else:
            c+=2





    menu_frame = tk.Frame(root, bg="gray")
    menu_frame.grid(column=0, row=0, columnspan=2, rowspan=10, sticky=tk.NSEW)

    menu_frame.rowconfigure(index=0, weight=4)
    for r in range(1, 10): menu_frame.rowconfigure(index=r, weight=10)
    menu_frame.rowconfigure(index=10, weight=4)
    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=5)
    menu_frame.columnconfigure(index=2, weight=1)

    exit_button = ttk.Button(menu_frame, command=lambda: login_frame(window, root))
    exit_button.grid(row=9, column=1, sticky=tk.NSEW)

    create_account_button = ttk.Button(menu_frame, command=lambda: login_frame(window, root))
    create_account_button.grid(row=1, column=1, sticky=tk.NSEW)




