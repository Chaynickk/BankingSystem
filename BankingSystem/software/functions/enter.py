from software.api_requests.admin import request_login_admin, request_registration_admin
from software.api_requests.client import request_login, request_registration
from software import config

def login(email, password, label, func):
    response = request_login(email, password)
    if response.status_code == 200:
        config.set_token(response.json()["access_token"])
        config.set_user_data({
          "first_name": response.json()["client"]["first_name"],
          "last_name": response.json()["client"]["last_name"],
          "patronymic": response.json()["client"]["patronymic"],
          "email": response.json()["client"]["email"],
          "phone_number": response.json()["client"]["phone_number"]
        })
        func()
    elif response.status_code == 401:
        label.config(text="Email или пароль неверный")
    else:
        label.config(text="Произошла ошибка, попробуйте позже")


def registration(first_name, last_name, phone_number, email, password, label, func, patronymic=None):
    if first_name == '':
        label.config(text="Имя не заполнено")
        return
    elif last_name == '':
        label.config(text="Фамилия не заполнено")
        return
    elif phone_number == '':
        label.config(text="Телефон не заполнено")
        return
    elif email == '':
        label.config(text="Email не заполнено")
        return
    elif password == '':
        label.config(text="Пароль не заполнено")
        return


    response = request_registration(first_name=first_name,
                         last_name=last_name,
                         phone_number=phone_number,
                         email=email,
                         password=password,
                         patronymic=patronymic)

    if response.status_code == 200:
        config.set_token(response.json()["access_token"])
        config.set_user_data({
            "first_name": response.json()["client"]["first_name"],
            "last_name": response.json()["client"]["last_name"],
            "patronymic": response.json()["client"]["patronymic"],
            "email": response.json()["client"]["email"],
            "phone_number": response.json()["client"]["phone_number"]
        })
        func()
    elif response.status_code == 409:
        if response.json()['detail'][0] == 'E':
            label.config(text="Такой email уже зарегистрирован")
        else:
            label.config(text="Такой номер телефона уже зарегистрирован")
    else:
        label.config(text="Произошла ошибка, попробуйте позже")

def login_admin(email, password, label, func):
    response = request_login_admin(email, password)
    if response.status_code == 200:
        config.set_token(response.json()["access_token"])
        config.set_user_data({
          "first_name": response.json()["client"]["first_name"],
          "last_name": response.json()["client"]["last_name"],
          "patronymic": response.json()["client"]["patronymic"],
          "email": response.json()["client"]["email"],
          "phone_number": response.json()["client"]["phone_number"]
        })
        func()
    elif response.status_code == 401:
        label.config(text="Email или пароль неверный")
    else:
        label.config(text="Произошла ошибка, попробуйте позже")


def registration_admin(first_name, last_name, email, password, label, func, patronymic=None):
    if first_name == '':
        label.config(text="Имя не заполнено")
        return
    elif last_name == '':
        label.config(text="Фамилия не заполнено")
        return
    elif email == '':
        label.config(text="Email не заполнено")
        return
    elif password == '':
        label.config(text="Пароль не заполнено")
        return


    response = request_registration_admin(first_name=first_name,
                         last_name=last_name,
                         email=email,
                         password=password,
                         patronymic=patronymic)

    if response.status_code == 200:
        config.set_token(response.json()["access_token"])
        config.set_user_data({
            "first_name": response.json()["client"]["first_name"],
            "last_name": response.json()["client"]["last_name"],
            "patronymic": response.json()["client"]["patronymic"],
            "email": response.json()["client"]["email"],
            "phone_number": response.json()["client"]["phone_number"]
        })
        func()
    elif response.status_code == 409:
        if response.json()['detail'][0] == 'E':
            label.config(text="Такой email уже зарегистрирован")
        else:
            label.config(text="Такой номер телефона уже зарегистрирован")
    else:
        label.config(text="Произошла ошибка, попробуйте позже")