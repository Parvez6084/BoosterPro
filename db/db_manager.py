from typing import Annotated
from fastapi import Depends, HTTPException, status, FastAPI
from db.db_credential import SessionLocal, engine
from model.request_model import UserReqModel
from sqlalchemy.orm import Session
import db.models as models

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserReqModel, db: Session = Depends(get_db)):
    db_user = models.User(
        FullName=user.FullName,
        Email=user.Email,
        Password=user.Password
    )
    db.add(db_user)
    db.commit()
    return True
