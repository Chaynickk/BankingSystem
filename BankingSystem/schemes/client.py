from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

PasswordStr = Annotated[str, Field(min_lenght=10)]

class ClientRegistration(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: EmailStr
    phone_number: PhoneNumber
    password: PasswordStr

class ClientLogin(BaseModel):
    email: EmailStr
    password: PasswordStr
