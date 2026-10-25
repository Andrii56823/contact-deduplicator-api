from pydantic import BaseModel, Field
from typing import Optional


class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=2, max_length=50)

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str

class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=2, max_length=50)
    phone: Optional[str] = None
    company: Optional[str] = None

class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None

    class Config:
        from_attributes=True






