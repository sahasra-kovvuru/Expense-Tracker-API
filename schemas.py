from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ExpenseCreate(BaseModel):
    user_name: str
    category: str
    amount: float