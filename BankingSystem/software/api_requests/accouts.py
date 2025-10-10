import requests
from software import config
from software.config import API_URL

def request_get_accounts():
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.get(API_URL + "account/get", headers=headers)
    return response

def request_account_registration():
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.post(API_URL + "account/registration", headers=headers)
    return response

def request_account_del(account_id):
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.delete(API_URL + f"account/del?account_id={account_id}", headers=headers)
    return response

def request_transaction(money, from_account_id, to_account_id):
    data = {"from_account_id": int(from_account_id),
            "to_account_id": int(to_account_id),
            "money": int(money)}
    headers = {"Authorization": f"Bearer {config.token}"}
    response = requests.put(API_URL + f"account/transaction", headers=headers, json=data)
    return response

