import tkinter as tk
from tkinter import ttk

from software.api_requests.accouts import request_get_accounts
from software.api_requests.admin import request_get_admins, request_reject_admin, request_activate_admin, \
    request_find_clients, request_get_accounts_admin
from software.functions.accaunts import add_account, del_account, transaction
from software.functions.admin import find_clients, activate_admin, reject_admin, frieze_account, unfreeze_account
from software.functions.enter import login, registration, login_admin


def login_frame(window: tk.Tk, old_frame=None, is_client=True):
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
    error_label.grid(column=5, row=12, columnspan=5)

    if is_client:
        login_button = ttk.Button(root,
                                  text="Войти",
                                  command=lambda: login(email=email_entry.get(),
                                                        password=password_entry.get(),
                                                        label=error_label,
                                                        func=lambda: client_frame(window, root)),
                                  style="Login.TButton")
        login_button.grid(column=7, row=16, sticky=tk.NSEW)
    else:
        login_button = ttk.Button(root,
                                  text="Войти",
                                  command=lambda: login_admin(email=email_entry.get(),
                                                        password=password_entry.get(),
                                                        label=error_label,
                                                        func=lambda: admin_frame_found_users(window, root)),
                                  style="Login.TButton")
        login_button.grid(column=7, row=16, sticky=tk.NSEW)

    registration_button = ttk.Button(root, text="Зарегестрироватся",
                                     command=lambda: registrations_frame(window, root, is_client),
                                     style="Reg.TButton")
    registration_button.grid(column=0, row=0, sticky=tk.NSEW)

    if is_client:
        admin_button = ttk.Button(root,
                                  text="Войти как админ",
                                  command=lambda: login_frame(window=window, old_frame=root, is_client=False),
                                  style="Login.TButton")
        admin_button.grid(column=0, row=19, sticky=tk.NSEW)
    else:
        client_button = ttk.Button(root,
                                  text="Войти как клиент",
                                  command=lambda: login_frame(window=window, old_frame=root, is_client=True),
                                  style="Login.TButton")
        client_button.grid(column=0, row=19, sticky=tk.NSEW)

def registrations_frame(window: tk.Tk, old_frame=None, is_client=True):
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

    password_entry = ttk.Entry(root, font=("Arial", 23))
    password_entry.grid(column=4, row=30, sticky=tk.NSEW, columnspan=7)
    password_label = ttk.Label(root, text="Пароль", font=("Arial", 23))
    password_label.grid(column=3, row=30)

    email_entry = ttk.Entry(root, font=("Arial", 23))
    email_entry.grid(column=4, row=25, sticky=tk.NSEW, columnspan=7)
    email_label = ttk.Label(root, text="Email", font=("Arial", 23))
    email_label.grid(column=3, row=25)


    if is_client:
        phone_number_entry = ttk.Entry(root, font=("Arial", 23))
        phone_number_entry.grid(column=4, row=35, sticky=tk.NSEW, columnspan=7)
        phone_number_label = ttk.Label(root, text="Телефон", font=("Arial", 23))
        phone_number_label.grid(column=3, row=35)

    login_button = ttk.Button(root, text="Войти", command=lambda: login_frame(window, root, is_client), style="Login.TButton")
    login_button.grid(column=0, row=0, sticky=tk.NSEW, rowspan=6, columnspan=2)

    error_label = ttk.Label(root, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=5, row=60, columnspan=5)

    registration_button = ttk.Button(root,
                                     text="Зарегистрироваться",
                                     style="Reg.TButton",
                                     command=lambda: registration(email=email_entry.get(),
                                                           first_name=first_name_entry.get(),
                                                           last_name=last_name_entry.get(),
                                                           patronymic=patronymic_entry.get(),
                                                           phone_number=phone_number_entry.get(),
                                                           password=password_entry.get(),
                                                           label=error_label,
                                                           func=lambda: client_frame(window, root)))
    registration_button.grid(column=7, row=80, sticky=tk.NSEW, rowspan=6)

    if is_client:
        admin_button = ttk.Button(root,
                                  text="Зарегистрироваться\nкак админ",
                                  command=lambda: registrations_frame(window=window, old_frame=root, is_client=False),
                                  style="Reg.TButton")
        admin_button.grid(column=0, row=96, rowspan=4, sticky=tk.NSEW)
    else:
        client_button = ttk.Button(root,
                                  text="Зарегистрироваться\nкак клиент",
                                  command=lambda: registrations_frame(window=window, old_frame=root, is_client=True),
                                  style="Reg.TButton")
        client_button.grid(column=0, row=96, rowspan=4, sticky=tk.NSEW)

def admin_frame_found_users(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)

    root.rowconfigure(index=0, weight=1)

    menu_frame = tk.Frame(root, bg="gray")
    menu_frame.grid(column=0, row=0, rowspan=1, sticky=tk.NSEW)

    menu_frame.rowconfigure(index=0, weight=1)
    menu_frame.rowconfigure(index=1, weight=4)
    menu_frame.rowconfigure(index=2, weight=1)
    menu_frame.rowconfigure(index=3, weight=4)
    menu_frame.rowconfigure(index=4, weight=20)
    menu_frame.rowconfigure(index=5, weight=4)
    menu_frame.rowconfigure(index=6, weight=1)

    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=8)
    menu_frame.columnconfigure(index=2, weight=1)

    find_client_button = ttk.Button(menu_frame,text="Найти клиента", style="Choice.TButton", command=lambda: admin_frame_found_users(window, root))
    find_client_button.grid(column=1, row=1, sticky=tk.NSEW)
    find_admin_button = ttk.Button(menu_frame, text="Заявки на админа", style="Choice.TButton", command=lambda: admin_frame_requests(window, root))
    find_admin_button.grid(column=1, row=3, sticky=tk.NSEW)
    exit_button = ttk.Button(menu_frame, text="Выйти", style="Exit.TButton", command=lambda: login_frame(window, root, False))
    exit_button.grid(column=1, row=5, sticky=tk.NSEW)

    find_frame = tk.Frame(root)
    find_frame.grid(column=1, row=0, rowspan=1, sticky=tk.NSEW)
    for c in range(15): find_frame.columnconfigure(index=c, weight=1)
    for r in range(100): find_frame.rowconfigure(index=r, weight=1)

    first_name_entry = ttk.Entry(find_frame, font=("Arial", 23))
    first_name_entry.grid(column=4, row=10, sticky=tk.NSEW, columnspan=7)
    first_name_label = ttk.Label(find_frame, text="Имя", font=("Arial", 23))
    first_name_label.grid(column=3, row=10)

    last_name_entry = ttk.Entry(find_frame, font=("Arial", 23))
    last_name_entry.grid(column=4, row=15, sticky=tk.NSEW, columnspan=7)
    last_name_label = ttk.Label(find_frame, text="Фамилия", font=("Arial", 23))
    last_name_label.grid(column=3, row=15)

    patronymic_entry = ttk.Entry(find_frame, font=("Arial", 23))
    patronymic_entry.grid(column=4, row=20, sticky=tk.NSEW, columnspan=7)
    patronymic_label = ttk.Label(find_frame, text="Отчество", justify=tk.CENTER, font=("Arial", 23))
    patronymic_label.grid(column=3, row=20)

    email_entry = ttk.Entry(find_frame, font=("Arial", 23))
    email_entry.grid(column=4, row=25, sticky=tk.NSEW, columnspan=7)
    email_label = ttk.Label(find_frame, text="Email", font=("Arial", 23))
    email_label.grid(column=3, row=25)

    phone_number_entry = ttk.Entry(find_frame, font=("Arial", 23))
    phone_number_entry.grid(column=4, row=30, sticky=tk.NSEW, columnspan=7)
    phone_number_label = ttk.Label(find_frame, text="Телефон", font=("Arial", 23))
    phone_number_label.grid(column=3, row=30)

    id_client_entry = ttk.Entry(find_frame, font=("Arial", 23))
    id_client_entry.grid(column=4, row=35, sticky=tk.NSEW, columnspan=7)
    id_client_label = ttk.Label(find_frame, text="ID", font=("Arial", 23))
    id_client_label.grid(column=3, row=35)

    error_label = ttk.Label(find_frame, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=5, row=60, columnspan=5)

    registration_button = ttk.Button(find_frame,
                                     text="Найти",
                                     style="Reg.TButton",
                                     command=lambda: find_clients(func=lambda:
                                     admin_frame_clients(window=window,
                                                         old_frame=root,
                                                         clients=request_find_clients(email=email_entry.get(),
                                                                  id_client=id_client_entry.get(),
                                                                  first_name=first_name_entry.get(),
                                                                  last_name=last_name_entry.get(),
                                                                  patronymic=patronymic_entry.get(),
                                                                  phone_number=phone_number_entry.get(),
                                                                  ))))
    registration_button.grid(column=7, row=80, sticky=tk.NSEW, rowspan=6)

def admin_frame_requests(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)

    root.rowconfigure(index=0, weight=1)

    menu_frame = tk.Frame(root, bg="gray")
    menu_frame.grid(column=0, row=0, rowspan=1, sticky=tk.NSEW)

    menu_frame.rowconfigure(index=0, weight=1)
    menu_frame.rowconfigure(index=1, weight=4)
    menu_frame.rowconfigure(index=2, weight=1)
    menu_frame.rowconfigure(index=3, weight=4)
    menu_frame.rowconfigure(index=4, weight=20)
    menu_frame.rowconfigure(index=5, weight=4)
    menu_frame.rowconfigure(index=6, weight=1)

    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=8)
    menu_frame.columnconfigure(index=2, weight=1)

    find_client_button = ttk.Button(menu_frame,text="Найти клиента", style="Choice.TButton", command=lambda: admin_frame_found_users(window, root))
    find_client_button.grid(column=1, row=1, sticky=tk.NSEW)
    find_admin_button = ttk.Button(menu_frame, text="Заявки на админа", style="Choice.TButton", command=lambda: admin_frame_requests(window, root))
    find_admin_button.grid(column=1, row=3, sticky=tk.NSEW)
    exit_button = ttk.Button(menu_frame, text="Выйти", style="Exit.TButton", command=lambda: login_frame(window, root, False))
    exit_button.grid(column=1, row=5, sticky=tk.NSEW)

    requests_canvas = tk.Canvas(root, highlightthickness=0)
    requests_canvas.grid(column=1, row=0, columnspan=10, rowspan=10, sticky=tk.NSEW)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=requests_canvas.yview)
    scrollbar.grid(column=12, row=0, rowspan=10, sticky=tk.NS)

    requests_canvas.configure(yscrollcommand=scrollbar.set)

    requests_canvas.columnconfigure(index=0, weight=20)
    requests_canvas.columnconfigure(index=1, weight=1)
    requests_canvas.rowconfigure(index=0, weight=1)
    requests_canvas.rowconfigure(index=1, weight=1)

    requests_frame = tk.Frame(requests_canvas)
    win_id = requests_canvas.create_window((0, 0), window=requests_frame, anchor="nw")

    requests_frame.bind("<Configure>", lambda e: requests_canvas.configure(scrollregion=requests_canvas.bbox("all")))
    requests_canvas.bind("<Configure>", lambda e: requests_canvas.itemconfigure(win_id, width=e.width))


    requests_frame.columnconfigure(index=0, weight=1, minsize=4)
    requests_frame.columnconfigure(index=1, weight=6)
    requests_frame.columnconfigure(index=2, weight=1, minsize=4)
    requests_frame.columnconfigure(index=3, weight=6)
    requests_frame.columnconfigure(index=4, weight=1, minsize=4)

    error_label = ttk.Label(requests_frame, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=0, row=0, columnspan=2)

    try:
        admins = request_get_admins().json()
    except KeyError:
        error_label.config(text="Произошла ошибка, попробуйте перезати")
        admins = []

    len_admins = len(admins)

    for r in range(len_admins*2 + 1):
        if r == 0:
            requests_frame.rowconfigure(index=r, weight=2)
        elif r % 2 == 0:
            requests_frame.rowconfigure(index=r, weight=1, minsize=4)
        else:
            requests_frame.rowconfigure(index=r, weight=4)

    r = 1
    c = 1
    i = -1
    list_frame = []
    while len_admins > 0:


        admin_frame = tk.Frame(requests_frame, bg="#d5d5d5")
        admin_frame.grid(row=r, column=c, sticky=tk.NSEW)

        list_frame.append(admin_frame)

        admin_frame.columnconfigure(index=0, weight=1)
        admin_frame.columnconfigure(index=1, weight=2)
        admin_frame.columnconfigure(index=2, weight=5)
        admin_frame.columnconfigure(index=3, weight=4)
        admin_frame.columnconfigure(index=4, weight=2)

        admin_frame.rowconfigure(index=0, weight=5)
        admin_frame.rowconfigure(index=1, weight=5)
        admin_frame.rowconfigure(index=2, weight=10)

        admin_frame.columnconfigure(index=5, weight=1)
        admin_frame.rowconfigure(index=3, weight=2)

        admin_name_label = tk.Label(admin_frame, text=f"ФИО: {admins[i]["first_name"]} {admins[i]["last_name"]} {admins[i]["patronymic"] or ''}", bg="#d5d5d5", font=("Arial", 18), justify=tk.CENTER)
        admin_name_label.grid(column=0, row=0, columnspan=4, sticky=tk.EW)

        admin_email_label = tk.Label(admin_frame, text=f"Email: {admins[i]["email"]}", bg="#d5d5d5", font=("Arial", 18), width=350, wraplength=500, justify="left")
        admin_email_label.grid(column=0, columnspan=4, row=1, sticky=tk.W)

        button_reject = ttk.Button(admin_frame,
                                  text="Отклонить",
                                  style="Enter.TButton",
                                  command=lambda admin_id=admins[i]["admin_id"]:
                                  reject_admin(admin_id,
                                               lambda: admin_frame_requests(window,root)))
        button_reject.grid(column=2, columnspan=2, row=2, sticky=tk.E)

        button_activate = ttk.Button(admin_frame,
                                  text="Принять",
                                  style="Enter.TButton",
                                  command=lambda admin_id=admins[i]["admin_id"]:
                                  activate_admin(admin_id,
                                               lambda: admin_frame_requests(window,root)))
        button_activate.grid(column=0, columnspan=2, row=2, sticky=tk.EW)


        len_admins -= 1
        i-=1

        if c + 2 >= 4:
            c = 1
            r+=2
        else:
            c+=2

def admin_frame_clients(window: tk.Tk, clients, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)

    root.rowconfigure(index=0, weight=1)

    menu_frame = tk.Frame(root, bg="gray")
    menu_frame.grid(column=0, row=0, rowspan=1, sticky=tk.NSEW)

    menu_frame.rowconfigure(index=0, weight=1)
    menu_frame.rowconfigure(index=1, weight=4)
    menu_frame.rowconfigure(index=2, weight=1)
    menu_frame.rowconfigure(index=3, weight=4)
    menu_frame.rowconfigure(index=4, weight=20)
    menu_frame.rowconfigure(index=5, weight=4)
    menu_frame.rowconfigure(index=6, weight=1)

    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=8)
    menu_frame.columnconfigure(index=2, weight=1)

    find_client_button = ttk.Button(menu_frame,text="Найти клиента", style="Choice.TButton", command=lambda: admin_frame_found_users(window, root))
    find_client_button.grid(column=1, row=1, sticky=tk.NSEW)
    find_admin_button = ttk.Button(menu_frame, text="Заявки на админа", style="Choice.TButton", command=lambda: admin_frame_requests(window, root))
    find_admin_button.grid(column=1, row=3, sticky=tk.NSEW)
    exit_button = ttk.Button(menu_frame, text="Выйти", style="Exit.TButton", command=lambda: login_frame(window, root, False))
    exit_button.grid(column=1, row=5, sticky=tk.NSEW)

    requests_canvas = tk.Canvas(root, highlightthickness=0)
    requests_canvas.grid(column=1, row=0, columnspan=10, rowspan=10, sticky=tk.NSEW)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=requests_canvas.yview)
    scrollbar.grid(column=12, row=0, rowspan=10, sticky=tk.NS)

    requests_canvas.configure(yscrollcommand=scrollbar.set)

    requests_canvas.columnconfigure(index=0, weight=20)
    requests_canvas.columnconfigure(index=1, weight=1)
    requests_canvas.rowconfigure(index=0, weight=1)
    requests_canvas.rowconfigure(index=1, weight=1)

    requests_frame = tk.Frame(requests_canvas)
    win_id = requests_canvas.create_window((0, 0), window=requests_frame, anchor="nw")

    requests_frame.bind("<Configure>", lambda e: requests_canvas.configure(scrollregion=requests_canvas.bbox("all")))
    requests_canvas.bind("<Configure>", lambda e: requests_canvas.itemconfigure(win_id, width=e.width))


    requests_frame.columnconfigure(index=0, weight=1, minsize=4)
    requests_frame.columnconfigure(index=1, weight=6)
    requests_frame.columnconfigure(index=2, weight=1, minsize=4)
    requests_frame.columnconfigure(index=3, weight=6)
    requests_frame.columnconfigure(index=4, weight=1, minsize=4)

    error_label = ttk.Label(requests_frame, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=0, row=0, columnspan=2)

    len_clients = len(clients)

    for r in range(len_clients*2 + 1):
        if r == 0:
            requests_frame.rowconfigure(index=r, weight=2)
        elif r % 2 == 0:
            requests_frame.rowconfigure(index=r, weight=1, minsize=4)
        else:
            requests_frame.rowconfigure(index=r, weight=4)

    r = 1
    c = 1
    i = -1
    list_frame = []
    while len_clients > 0:
        print(len_clients)

        admin_frame = tk.Frame(requests_frame, bg="#d5d5d5")
        admin_frame.grid(row=r, column=c, sticky=tk.NSEW)

        list_frame.append(admin_frame)

        admin_frame.columnconfigure(index=0, weight=1)
        admin_frame.columnconfigure(index=1, weight=2)
        admin_frame.columnconfigure(index=2, weight=5)
        admin_frame.columnconfigure(index=3, weight=4)
        admin_frame.columnconfigure(index=4, weight=2)

        admin_frame.rowconfigure(index=0, weight=5)
        admin_frame.rowconfigure(index=1, weight=5)
        admin_frame.rowconfigure(index=2, weight=5)
        admin_frame.rowconfigure(index=2, weight=5)
        admin_frame.rowconfigure(index=3, weight=10)

        admin_frame.columnconfigure(index=5, weight=1)
        admin_frame.rowconfigure(index=3, weight=2)

        admin_name_label = tk.Label(admin_frame, text=f"ФИО: {clients[i]["first_name"]} {clients[i]["last_name"]} {clients[i]["patronymic"] or ''}", bg="#d5d5d5", font=("Arial", 18), justify=tk.CENTER)
        admin_name_label.grid(column=0, row=0, columnspan=4, sticky=tk.EW)

        admin_email_label = tk.Label(admin_frame, text=f"Email: {clients[i]["email"]}", bg="#d5d5d5", font=("Arial", 18), width=350, wraplength=500, justify="left")
        admin_email_label.grid(column=0, columnspan=4, row=2, sticky=tk.W)

        admin_phone_label = tk.Label(admin_frame, text=f"Телефон: {clients[i]["phone_number"][4:]}", bg="#d5d5d5",
                                     font=("Arial", 18), width=350, wraplength=500, justify="left")
        admin_phone_label.grid(column=0, columnspan=4, row=3, sticky=tk.W)

        button_open_accounts = ttk.Button(admin_frame,
                                          text="Счета",
                                          style="Enter.TButton",
                                          command=lambda client_id=clients[i]["client_id"]: admin_frame_accounts(window=window,
                                                                               old_frame=root,
                                                                               client_id=client_id))
        button_open_accounts.grid(column=0, columnspan=2, row=4, sticky=tk.EW)


        len_clients -= 1
        i-=1

        if c + 2 >= 4:
            c = 1
            r+=2
        else:
            c+=2

def admin_frame_accounts(window: tk.Tk, client_id, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = ttk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=5)

    root.rowconfigure(index=0, weight=1)

    menu_frame = tk.Frame(root, bg="gray")
    menu_frame.grid(column=0, row=0, rowspan=1, sticky=tk.NSEW)

    menu_frame.rowconfigure(index=0, weight=1)
    menu_frame.rowconfigure(index=1, weight=4)
    menu_frame.rowconfigure(index=2, weight=1)
    menu_frame.rowconfigure(index=3, weight=4)
    menu_frame.rowconfigure(index=4, weight=20)
    menu_frame.rowconfigure(index=5, weight=4)
    menu_frame.rowconfigure(index=6, weight=1)

    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=8)
    menu_frame.columnconfigure(index=2, weight=1)

    find_client_button = ttk.Button(menu_frame,text="Найти клиента", style="Choice.TButton", command=lambda: admin_frame_found_users(window, root))
    find_client_button.grid(column=1, row=1, sticky=tk.NSEW)
    find_admin_button = ttk.Button(menu_frame, text="Заявки на админа", style="Choice.TButton", command=lambda: admin_frame_requests(window, root))
    find_admin_button.grid(column=1, row=3, sticky=tk.NSEW)
    exit_button = ttk.Button(menu_frame, text="Выйти", style="Exit.TButton", command=lambda: login_frame(window, root, False))
    exit_button.grid(column=1, row=5, sticky=tk.NSEW)

    requests_canvas = tk.Canvas(root, highlightthickness=0)
    requests_canvas.grid(column=1, row=0, columnspan=10, rowspan=10, sticky=tk.NSEW)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=requests_canvas.yview)
    scrollbar.grid(column=12, row=0, rowspan=10, sticky=tk.NS)

    requests_canvas.configure(yscrollcommand=scrollbar.set)

    requests_canvas.columnconfigure(index=0, weight=20)
    requests_canvas.columnconfigure(index=1, weight=1)
    requests_canvas.rowconfigure(index=0, weight=1)
    requests_canvas.rowconfigure(index=1, weight=1)

    requests_frame = tk.Frame(requests_canvas)
    win_id = requests_canvas.create_window((0, 0), window=requests_frame, anchor="nw")

    requests_frame.bind("<Configure>", lambda e: requests_canvas.configure(scrollregion=requests_canvas.bbox("all")))
    requests_canvas.bind("<Configure>", lambda e: requests_canvas.itemconfigure(win_id, width=e.width))


    requests_frame.columnconfigure(index=0, weight=1, minsize=4)
    requests_frame.columnconfigure(index=1, weight=6)
    requests_frame.columnconfigure(index=2, weight=1, minsize=4)
    requests_frame.columnconfigure(index=3, weight=6)
    requests_frame.columnconfigure(index=4, weight=1, minsize=4)

    error_label = ttk.Label(requests_frame, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=0, row=0, columnspan=2)

    try:
        accounts=request_get_accounts_admin(int(client_id))
    except:
        accounts=[]

    len_accounts = len(accounts)

    for r in range(len_accounts*2 + 1):
        if r == 0:
            requests_frame.rowconfigure(index=r, weight=2)
        elif r % 2 == 0:
            requests_frame.rowconfigure(index=r, weight=1, minsize=4)
        else:
            requests_frame.rowconfigure(index=r, weight=4)

    r = 1
    c = 1
    i = -1
    list_frame = []
    while len_accounts > 0:
        print(len_accounts)

        admin_frame = tk.Frame(requests_frame, bg="#d5d5d5")
        admin_frame.grid(row=r, column=c, sticky=tk.NSEW)

        list_frame.append(admin_frame)

        admin_frame.columnconfigure(index=0, weight=1)
        admin_frame.columnconfigure(index=1, weight=2)
        admin_frame.columnconfigure(index=2, weight=5)
        admin_frame.columnconfigure(index=3, weight=4)
        admin_frame.columnconfigure(index=4, weight=2)

        admin_frame.rowconfigure(index=0, weight=5)
        admin_frame.rowconfigure(index=1, weight=5)
        admin_frame.rowconfigure(index=2, weight=5)
        admin_frame.rowconfigure(index=3, weight=5)
        admin_frame.rowconfigure(index=4, weight=10)

        admin_frame.columnconfigure(index=5, weight=1)
        admin_frame.rowconfigure(index=3, weight=2)

        label_account = tk.Label(admin_frame, text=f"№ {accounts[i]["account_id"]}", bg="#d5d5d5", font=("Arial", 23),
                                 justify=tk.CENTER)
        label_account.grid(column=0, row=0, columnspan=4)

        label_balance = tk.Label(admin_frame,
                                 text=f"Баланс:\n{int(accounts[i]["amount_decimal"]) / 100:,.2f}".replace(",", " "),
                                 bg="#d5d5d5", font=("Arial", 18), justify=tk.LEFT)
        label_balance.grid(column=0, row=1, sticky=tk.EW)

        label_status = tk.Label(admin_frame,
                                 text=f"Состояние:\n{"Заморожен" if accounts[i]["is_frozen"] else "Активен"}",
                                 bg="#d5d5d5", font=("Arial", 18), justify="right")
        label_status.grid(column=4, row=1, sticky=tk.EW)

        button_activate = ttk.Button(admin_frame,
                                     text="Заморозить",
                                     style="Enter.TButton",
                                     command=lambda account_id=accounts[i]["account_id"]:
                                     frieze_account(account_id=account_id,
                                                    func=lambda:admin_frame_accounts(window=window, client_id=client_id, old_frame=root))
                                  )
        button_activate.grid(column=0, columnspan=2, row=4, sticky=tk.EW)

        button_activate = ttk.Button(admin_frame,
                                     text="Разморозить",
                                     style="Enter.TButton",
                                     command=lambda account_id=accounts[i]["account_id"]:
                                     unfreeze_account(account_id=account_id,
                                                    func=lambda:admin_frame_accounts(window=window, client_id=client_id, old_frame=root))
                                  )
        button_activate.grid(column=4, columnspan=2, row=4, sticky=tk.EW)


        len_accounts -= 1
        i-=1

        if c + 2 >= 4:
            c = 1
            r+=2
        else:
            c+=2

def client_frame(window: tk.Tk, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = tk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)


    for c in range(12): root.columnconfigure(index=c, weight=1)
    for r in range(10): root.rowconfigure(index=r, weight=1)



    account_canvas = tk.Canvas(root, highlightthickness=0)
    account_canvas.grid(column=2, row=0, columnspan=10, rowspan=10, sticky=tk.NSEW)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=account_canvas.yview)
    scrollbar.grid(column=12, row=0, rowspan=10, sticky=tk.NS)

    account_canvas.configure(yscrollcommand=scrollbar.set)

    account_canvas.columnconfigure(index=0, weight=20)
    account_canvas.columnconfigure(index=1, weight=1)
    account_canvas.rowconfigure(index=0, weight=1)
    account_canvas.rowconfigure(index=1, weight=1)

    accounts_frame = tk.Frame(account_canvas)
    win_id = account_canvas.create_window((0, 0), window=accounts_frame, anchor="nw")

    accounts_frame.bind("<Configure>", lambda e: account_canvas.configure(scrollregion=account_canvas.bbox("all")))
    account_canvas.bind("<Configure>", lambda e: account_canvas.itemconfigure(win_id, width=e.width))

    for c in range(7):
        if c % 2 == 0:
            accounts_frame.columnconfigure(index=c, weight=1, minsize=4)
        else:
            accounts_frame.columnconfigure(index=c, weight=6)


    accounts_frame.columnconfigure(index=7, weight=1)

    error_label = ttk.Label(accounts_frame, text="", foreground="red", font=("Arial", 20))
    error_label.grid(column=0, row=0, columnspan=2)

    try:
        accounts = request_get_accounts().json()["Accounts"]
    except KeyError:
        error_label.config(text="Произошла ошибка, попробуйте перезати")
        accounts = []

    len_accounts = len(accounts)

    for r in range(len_accounts*2 + 1):
        if r == 0:
            accounts_frame.rowconfigure(index=r, weight=2)
        elif r % 2 == 0:
            accounts_frame.rowconfigure(index=r, weight=1, minsize=4)
        else:
            accounts_frame.rowconfigure(index=r, weight=4)

    r = 1
    c = 1
    i = -1
    list_frame = []
    while len_accounts > 0:


        account_frame = tk.Frame(accounts_frame, bg="#d5d5d5")
        account_frame.grid(row=r, column=c, sticky=tk.NSEW)

        list_frame.append(account_frame)

        account_frame.columnconfigure(index=0, weight=1)
        account_frame.columnconfigure(index=1, weight=5)
        account_frame.columnconfigure(index=2, weight=1)
        account_frame.columnconfigure(index=3, weight=2)

        account_frame.rowconfigure(index=0, weight=1)
        account_frame.rowconfigure(index=1, weight=1)
        account_frame.rowconfigure(index=2, weight=2)

        account_frame.columnconfigure(index=4, weight=1)
        account_frame.rowconfigure(index=3, weight=2)

        label_account = tk.Label(account_frame, text=f"№ {accounts[i]["account_id"]}", bg="#d5d5d5", font=("Arial", 23), justify=tk.CENTER)
        label_account.grid(column=0, row=0, columnspan=4)

        label_balance = tk.Label(account_frame, text=f"Баланс:\n{int(accounts[i]["amount_decimal"]) / 100:,.2f}".replace(",", " "), bg="#d5d5d5", font=("Arial", 18), justify=tk.LEFT)
        label_balance.grid(column=0, row=1, sticky=tk.EW)



        button_enter = ttk.Button(account_frame,
                                  text="Войти",
                                  style="Enter.TButton",
                                  command=lambda money=accounts[i]["amount_decimal"], number=accounts[i]["account_id"]:
                                  frame_account(window, money, number, old_frame=root))
        button_enter.grid(column=3, row=2, sticky=tk.NSEW)


        len_accounts -= 1
        i-=1

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

    exit_button = ttk.Button(menu_frame, text="Выход", command=lambda: login_frame(window, root), style="Exit.TButton")
    exit_button.grid(row=9, column=1, sticky=tk.NSEW)

    create_account_button = ttk.Button(menu_frame,
                                       text="Создать новый счет",
                                       command=lambda: add_account(lambda: client_frame(window, root), error_label),
                                       style="CreateAccount.TButton")
    create_account_button.grid(row=1, column=1, sticky=tk.NSEW)

def frame_account(window: tk.Tk, money, number, old_frame=None, transaction_done=None):
    if old_frame is not None:
        old_frame.destroy()


    root = tk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)

    root.rowconfigure(index=0, weight=1)
    root.columnconfigure(index=0, weight=1)

    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=4)
    root.rowconfigure(index=3, weight=3)
    root.rowconfigure(index=4, weight=3)
    root.rowconfigure(index=5, weight=2)
    root.rowconfigure(index=6, weight=4)
    root.rowconfigure(index=7, weight=1)
    root.rowconfigure(index=8, weight=1)
    root.rowconfigure(index=9, weight=2)
    root.rowconfigure(index=10, weight=1)
    root.rowconfigure(index=11, weight=1)

    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=4)
    root.columnconfigure(index=3, weight=12)
    root.columnconfigure(index=4, weight=1)
    root.columnconfigure(index=5, weight=6)
    root.columnconfigure(index=6, weight=6)
    root.columnconfigure(index=7, weight=6)

    exit_button = ttk.Button(root, text="Выход", command=lambda: client_frame(window, root), style="Exit.TButton")
    exit_button.grid(row=1, column=1, sticky=tk.NSEW)

    heading_label = ttk.Label(root, text="Перевод", style="Heading.TLabel")
    heading_label.grid(column=4, row=2)

    number_account_label = ttk.Label(root, text="Номер аккаунта", style="LargeText.TLabel")
    number_account_label.grid(column=2, row=3)

    number_account_entry = ttk.Entry(root, font=("Arial", 25))
    number_account_entry.grid(column=3, row=3, columnspan=4, sticky=tk.EW)

    money_label = ttk.Label(root, text="Сумма перевода", style="LargeText.TLabel")
    money_label.grid(column=2, row=4)

    money_entry = ttk.Entry(root, font=("Arial", 25))
    money_entry.grid(column=3, row=4, columnspan=4, sticky=tk.EW)

    balance_label = ttk.Label(root, text=f"Баланс: {money / 100:,.2f}". replace(",", " "), style="LargeText.TLabel")
    balance_label.grid(column=1, columnspan=2, row=9, sticky=tk.W)

    number_account_client_label = ttk.Label(root, text=f"Ваш номер счета: {number}", style="LargeText.TLabel")
    number_account_client_label.grid(column=1, columnspan=2, row=10, sticky=tk.W)

    if transaction_done is True:
        status_label = ttk.Label(root, text="Перевод успешно выполнен", foreground="green", font=("Arial", 18))
        status_label.grid(row=8, column=2, columnspan=6)
    else:
        status_label = ttk.Label(root, text="", foreground="red", font=("Arial", 18))
        status_label.grid(row=8, column=2, columnspan=6)

    transaction_button = ttk.Button(root,
                                    text="Перевести",
                                    style="Transaction.TButton",
                                    command=lambda: transaction(error_label=status_label,
                                                                balance=money, money=money_entry.get().replace(",", "."),
                                                                from_account_id=number,
                                                                to_account_id=number_account_entry.get(),
                                                                func=lambda: frame_account(window,
                                                                                           money=money-float(money_entry.get().replace(",", "."))*100,
                                                                                           number=number,
                                                                                           transaction_done=True,
                                                                                           old_frame=root)))

    transaction_button.grid(column=4, row=5, sticky=tk.NSEW)

    delete_button = ttk.Button(root, text="Удалить счет", style="Transaction.TButton",
                               command=lambda: are_you_sure_frame(window, money, number, old_frame=root))
    delete_button.grid(column=7, row=10, sticky=tk.NS)

def are_you_sure_frame(window: tk.Tk, money, number, old_frame=None):
    if old_frame is not None:
        old_frame.destroy()

    root = tk.Frame(window)
    root.pack(expand=True, fill=tk.BOTH)

    root.columnconfigure(index=0, weight=12)
    root.columnconfigure(index=1, weight=4)
    root.columnconfigure(index=2, weight=2)
    root.columnconfigure(index=3, weight=4)
    root.columnconfigure(index=4, weight=12)

    root.rowconfigure(index=0, weight=5)
    root.rowconfigure(index=1, weight=8)
    root.rowconfigure(index=2, weight=2)
    root.rowconfigure(index=3, weight=5)


    warning_label = ttk.Label(root, text="Вы уверены что хотите удалить этот счет?\nБаланс этого счет будет утерян!",
                              style="Heading.TLabel", justify=tk.CENTER)
    warning_label.grid(column=1, columnspan=3, row=1)

    error_label = ttk.Label(root, text="", foreground="red", style="LargeText.TLabel")
    error_label.grid(column=1, columnspan=3, row=3)

    accept_button = ttk.Button(root, text="Удалить", style="Choice.TButton",
                               command=lambda: del_account(error_label=error_label,
                                                           account_id=number,
                                                           func=lambda: client_frame(window, root)))
    accept_button.grid(column=1, row=2, sticky=tk.NSEW)

    reject_button = ttk.Button(root, text="Отмена", style="Choice.TButton", command=lambda: frame_account(window, money=money, number=number, old_frame=root))
    reject_button.grid(column=3, row=2, sticky=tk.NSEW)