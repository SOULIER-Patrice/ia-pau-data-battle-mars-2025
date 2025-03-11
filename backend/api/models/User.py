from pydantic import BaseModel, Field
import uuid


class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    email: str
    first_name: str
    last_name: str
    roles: list[str] = ["user"]
    hashed_password: str


class UserOutput(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    roles: list[str] = ["user"]


class UserForCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserForUpdate(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserForLogin(BaseModel):
    email: str
    password: str
