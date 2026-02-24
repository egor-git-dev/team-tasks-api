from fastapi import FastAPI, Depends
from .database import engine, Base, SessionLocal
from . import models, schemas
from sqlalchemy.orm import Session


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Team Tasks API работает"}


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
