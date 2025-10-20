import tkinter as tk
from tkinter import ttk
from software.functions.frames import login_frame, client_frame, frame_account, are_you_sure_frame

root = tk.Tk()
root.geometry("1500x900")

login_button_style = ttk.Style()
login_button_style.configure("Login.TButton", font=("Arial", 18))

registration_button_style = ttk.Style()
registration_button_style.configure("Reg.TButton", font=("Arial", 14), justify=tk.CENTER)

create_button_style = ttk.Style()
create_button_style.configure("CreateAccount.TButton", font=("Arial", 20))

exit_button_style = ttk.Style()
exit_button_style.configure("Exit.TButton", font=("Arial", 23))

enter_button_style = ttk.Style()
enter_button_style.configure("Enter.TButton", font=("Arial", 14))

heading_label_style = ttk.Style()
heading_label_style.configure("Heading.TLabel", font=("Arial", 30))

large_text_label_style = ttk.Style()
large_text_label_style.configure("LargeText.TLabel", font=("Arial", 25))

transaction_button_style = ttk.Style()
transaction_button_style.configure("Transaction.TButton", font=("Arial", 20))

choice_button_style = ttk.Style()
choice_button_style.configure("Choice.TButton", font=("Arial", 20))

login_frame(root)


root.mainloop()