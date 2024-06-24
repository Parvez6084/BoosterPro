from pydantic import BaseModel
from datetime import datetime


class TaskResponseModel(BaseModel):
    id: int
    user_id: str
    is_email_send: bool
    title: str
    summary: str
    published: datetime
    link: str
    email: str
