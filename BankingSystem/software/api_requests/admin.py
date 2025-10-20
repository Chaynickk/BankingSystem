import requests
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