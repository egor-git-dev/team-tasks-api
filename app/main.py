from fastapi import FastAPI, Depends, HTTPException
from .database import engine, Base, SessionLocal
from . import models, schemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext


app = FastAPI()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str):
    return pwd_context.hash(password)


@app.get("/")
def root():
    return {"message": "Team Tasks API работает"}


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email уже зарегестрирован")

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
