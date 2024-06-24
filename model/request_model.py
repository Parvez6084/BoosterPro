from pydantic import BaseModel


class TaskModel(BaseModel):
    url: str
    userId: str

