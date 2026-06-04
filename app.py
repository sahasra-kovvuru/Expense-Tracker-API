from fastapi import FastAPI
from models import Base, User, Expense
from database import SessionLocal, engine
from schemas import UserCreate, ExpenseCreate, UserOut


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users/add", response_model=UserOut, status_code=201)
def add_user(user: UserCreate):

    db = SessionLocal()

    try:
        new_user = User(name=user.name)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    finally:
        db.close()

@app.delete("/users/remove")
def remove_user(name: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.name == name
    ).first()

    if not user:
        return {"message":"User not found"}

    db.delete(user)
    db.commit()

    return {
        "message":"User removed successfully"
    }

@app.post("/expenses")
def add_expense(expense: ExpenseCreate):

    db = SessionLocal()

    user = db.query(User).filter(
        User.name == expense.user_name
    ).first()

    if not user:
        return {"message":"User not found"}

    new_expense = Expense(
        user_id=user.id,
        category=expense.category,
        amount=expense.amount
    )

    db.add(new_expense)
    db.commit()

    return {
        "message":"Expense added successfully"
    }

@app.get("/expenses")
def get_expenses(name: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.name == name
    ).first()

    if not user:
        return {"message":"User not found"}

    expenses = db.query(Expense).filter(
        Expense.user_id == user.id
    ).all()

    return expenses

@app.get("/expenses/settlement")
def settlement(name: str):

    db = SessionLocal()

    user = db.query(User).filter(
        User.name == name
    ).first()

    if not user:
        return {"message":"User not found"}

    expenses = db.query(Expense).filter(
        Expense.user_id == user.id
    ).all()

    total = sum(e.amount for e in expenses)

    return {
        "name": user.name,
        "total_expense": total
    }

@app.get("/monthly_summary")
def monthly_summary():

    db = SessionLocal()

    users = db.query(User).all()

    summary = {}

    for user in users:

        expenses = db.query(Expense).filter(
            Expense.user_id == user.id
        ).all()

        total = sum(e.amount for e in expenses)

        summary[user.name] = {
            "total_expense": total
        }

    return summary



