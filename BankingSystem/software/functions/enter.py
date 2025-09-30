from software.api_requests.enter import request_login
from software.config import token

def login(email, password, label, func):
    response = request_login(email, password)
    if response.status_code == 200:
        token = response.json()["access_token"]
        func()
    elif response.status_code == 401:
        label.config(text="Email или пароль неверный")


def registration(first_name, last_name, phone_number, email, password, label, func, patronymic=None):
    pass