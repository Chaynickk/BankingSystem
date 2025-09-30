import requests
from software.config import API_URL

def request_login(username, password):
    data = {"username": username, "password": password}
    response = requests.post(API_URL + "client/login", data=data)
    return response













