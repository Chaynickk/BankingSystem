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

def transaction(func, error_label, money, from_account_id, to_account_id):
    response = request_transaction(money, from_account_id, to_account_id)
    if response.status_code == 200:
        func()
        return response
    elif response.status_code == 404:
        error_label.config(text="Счет не найдет")
        return response
    elif response.status_code == 422:
        error_label.config(text="Может быть превышен лимит баланса")
        return response
    elif response.status_code == 403:
        error_label.config(text="Счет заморожен")
        return response
    else:
        error_label.config(text="Произошла ошибка попробуйте позже")
        return response