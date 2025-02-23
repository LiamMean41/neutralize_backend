from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import User
from database import SessionLocal  # Assuming you're using SQLAlchemy
from service.oauth import get_current_user

credits = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get current user's credits
@credits.get("/user/credits")
async def get_user_credits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"credits": user.credits}

# Buy credits (add credits to the user)
@credits.post("/user/credits/buy")
async def buy_credits(amount: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    user = db.query(User).filter(User.id == current_user.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.credits += amount
    db.commit()
    db.refresh(user)
    return {"message": "Credits successfully added", "new_credits": user.credits}
