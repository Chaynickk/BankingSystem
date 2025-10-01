from dotenv import load_dotenv
from argon2 import PasswordHasher
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
MAX_BALANCE = int(os.getenv("MAX_BALANCE"))

password_hasher = PasswordHasher(time_cost=3,
                                 hash_len=32,
                                 salt_len=16)

