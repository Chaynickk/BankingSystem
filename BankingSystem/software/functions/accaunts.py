from software.api_requests.accouts import request_account_registration


def add_account(func, error_label):
    response = request_account_registration()
    if response.status_code == 200:
        func()
        return response
    else:
        error_label.config(text="Произошла ошибка попробуйте позже")
        return response
