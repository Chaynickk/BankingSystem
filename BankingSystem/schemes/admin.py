from pydantic import BaseModel, EmailStr, Field, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Annotated

PasswordStr = Annotated[str, StringConstraints(min_length=10)]

class AdminRegistration(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: EmailStr
    phone_number: PhoneNumber
    password: PasswordStr
