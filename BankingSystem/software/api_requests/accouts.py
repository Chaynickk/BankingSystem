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


