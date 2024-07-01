from pydantic import BaseModel


class UserReqModel(BaseModel):
    FullName: str
    Email: str
    Password: str



