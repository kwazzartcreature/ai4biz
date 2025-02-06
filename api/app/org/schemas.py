from pydantic import BaseModel


class OrgConfig(BaseModel): ...


class Org(BaseModel):
    id: int
    name: str
    schema_name: str

    class Config:
        orm_mode = True


class OrgCreate(BaseModel):
    name: str
    password: str


class OrgUpdate(BaseModel):
    name: str
