import requests

from software import config
from software.config import API_URL

def request_login_admin(username, password):
    data = {"username": username, "password": password}
    response = requests.post(API_URL + "admin/login", data=data)
    return response

def request_registration_admin(first_name, last_name, email, password, patronymic=None):
    data = {
  "first_name": first_name,
  "last_name": last_name,
  "patronymic": patronymic,
  "email": email,
  "password": password
}
    response = requests.post(API_URL + "admin/registration", json=data)
    return response

def request_find_clients(first_name=None, last_name=None, email=None, id_client=None, patronymic=None, phone_number=None):

    params = {"first_name": first_name,
              "last_name": last_name,
              "patronymic": patronymic,
              "email": email,
              "client_id": id_client,
              "phone_number": phone_number}

    params = {k: v for k, v in params.items() if v != ''}

    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.get(API_URL + f"admin/get_clients", params=params, headers=headers)
    return response.json()

def request_get_accounts_admin(client_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.get(API_URL + f"admin/get_accounts?client_id={client_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def request_get_admins():
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.get(API_URL + f"admin/get_not_activate_admins", headers=headers)
    print(response.json())
    return response

def request_activate_admin(admin_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.put(API_URL + f"admin/activate_admin?admin_id={admin_id}", headers=headers)
    return response

def request_reject_admin(admin_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.delete(API_URL + f"admin/reject_admin?admin_id={admin_id}", headers=headers)
    return response

def request_frieze_account(account_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.put(API_URL + f"admin/frieze_account?account_id={account_id}", headers=headers)
    return response

def request_unfreeze_account(account_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.put(API_URL + f"admin/unfreeze_account?account_id={account_id}", headers=headers)
    return response
