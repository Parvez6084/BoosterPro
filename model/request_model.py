from pydantic import BaseModel


class UserReqModel(BaseModel):
    userId: str
    url: str


