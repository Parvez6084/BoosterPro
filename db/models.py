from sqlalchemy import BIGINT, Boolean, Column, Integer, String, DateTime, DECIMAL
from datetime import datetime
from db.db_credential import Base


class User(Base):
    __tablename__ = 'User_Information'
    Id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    FullName = Column(String(250))
    Email = Column(String(250), unique=True, index=True)
    Password = Column(String(250))
    IsSubscribed = Column(Boolean, default=False)
    URL = Column(String, nullable=True)
    CreateAt = Column(DateTime, default=datetime.now)

#
# class Tasks(Base):
#     __tablename__ = 'tasks'
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(100), index=True)
#     is_email_send = Column(Boolean, default=False)
#     title = Column(String)
#     summary = Column(String)
#     published = Column(DateTime)
#     link = Column(String)
#
#
# class Subscriptions(Base):
#     __tablename__ = 'subscriptions'
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(100), index=True)
#     subscription_id = Column(String(100), index=True)
#     subscription_amount = Column(DECIMAL(18, 4), default=0.0)
#     subscription_start_date = Column(DateTime)
#     subscription_end_date = Column(DateTime)
