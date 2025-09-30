import requests
from software.config import API_URL

def request_login(username, password):
    data = {"username": username, "password": password}
    response = requests.post(API_URL + "client/login", data=data)
    return response

def request_registration(first_name, last_name, email, phone_number, password, patronymic=None):
    data = {
  "first_name": first_name,
  "last_name": last_name,
  "patronymic": patronymic,
  "email": email,
  "phone_number": phone_number,
  "password": password,
}
    response = requests.post(API_URL + "client/registration", json=data)
    return response