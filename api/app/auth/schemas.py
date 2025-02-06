from pydantic import BaseModel


class Login(BaseModel):
    login: str
    password: str


class AuthPayload(BaseModel):
    id: int
    super: bool
    org: str
    schema_name: str
