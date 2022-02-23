from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
#from typing import List, Optional
from ..database import get_db
from .. schemas import PostBase, UserCreate, PostCreate, PostResponse, UserResponse
from .. import models, schemas, utils

router = APIRouter(prefix = "/users", tags = ["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= UserResponse)
def create_user(user : UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    #new_user = models.user(** user.dict())
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    #cursor.execute(""" INSERT INTO users(email) VALUES (%s) """,(user.email))
    #new_user = cursor.fetchone()
    #conn.commit()
    #return None

@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with {id}not found")

    return user