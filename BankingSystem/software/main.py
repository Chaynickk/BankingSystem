import tkinter as tk
from tkinter import ttk
from software.functions.frames import login_frame, client_frame

root = tk.Tk()
root.geometry("1500x900")

login_button_style = ttk.Style()
login_button_style.configure("Login.TButton", font=("Arial", 18))

registration_button_style = ttk.Style()
registration_button_style.configure("Reg.TButton", font=("Arial", 14))

create_button_style = ttk.Style()
create_button_style.configure("CreateAccount.TButton", font=("Arial", 20))

exit_button_style = ttk.Style()
exit_button_style.configure("Exit.TButton", font=("Arial", 23))

enter_button_style = ttk.Style()
enter_button_style.configure("Enter.TButton", font=("Arial, 14"))


client_frame(root)
#login_frame(root)

root.mainloop()