from software.api_requests.admin import request_login_admin, request_registration_admin, request_find_clients, \
    request_activate_admin, request_reject_admin, request_frieze_account, request_unfreeze_account
from software.api_requests.client import request_login, request_registration
from software import config

def find_clients(func):
    func()

def activate_admin(admin_id, funk):

    response = request_activate_admin(admin_id)
    funk()

    return response


def reject_admin(admin_id, funk):

    response = request_reject_admin(admin_id)
    funk()

    return response

def frieze_account(account_id, func):
    func()
    return request_frieze_account(account_id)

def unfreeze_account(account_id, func):
    response = request_unfreeze_account(account_id)
    func()
    return response