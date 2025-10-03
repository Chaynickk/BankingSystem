from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

token = None
user_data = {
  "first_name": None,
  "last_name": None,
  "patronymic": None,
  "email": None,
  "phone_number": None
}