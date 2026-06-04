from sqlalchemy import Column,Integer,String,ForeignKey,Float,Date
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    amount = Column(Float)
    expense_date = Column(Date, default=date.today)