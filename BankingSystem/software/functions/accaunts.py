from software.api_requests.accouts import request_account_registration, request_account_del, request_transaction


def add_account(func, error_label):
    response = request_account_registration()
    if response.status_code == 200:
        func()
        return response
    else:
        error_label.config(text="Произошла ошибка попробуйте позже")
        return response

def del_account(func, error_label, account_id):
    response = request_account_del(account_id)
    if response.status_code == 200:
        func()
        return response
    else:
        error_label.config(text="Произошла ошибка попробуйте позже")
        return response

def transaction(error_label, balance, money, from_account_id, to_account_id, func):

    try:
        money = float(money)
        to_account_id = int(to_account_id)
    except:
        error_label.config(text="В сумму перевода и номер счета необходимо ввести число", foreground="red")
        return None

    if money < 0.01:
        error_label.config(text="Сумма должна быть больше нуля", foreground="red")
        return None

    if balance - money <= 0:
        error_label.config(text="У вас недостаточно средств на балансе", foreground="red")
        return None

    response = request_transaction(int(money * 100), from_account_id, to_account_id)


    if response.status_code == 200:
        func()
        return response
    elif response.status_code == 404:
        error_label.config(text="Счет не найдет", foreground="red")
        return response
    elif response.status_code == 422:
        error_label.config(text="Может быть превышен лимит баланса", foreground="red")
        return response
    elif response.status_code == 403:
        error_label.config(text="Счет заморожен", foreground="red")
        return response
    else:
        error_label.config(text="Произошла ошибка попробуйте позже", foreground="red")
        return response