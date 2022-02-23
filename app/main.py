#from typing import List, Optional, Dict
from fastapi import FastAPI, Response, status, HTTPException, Depends
#from fastapi.params import Body
#from pydantic import BaseModel
#from .schemas import PostBase, UserCreate, PostCreate, PostResponse, UserResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import time  # for time.sleep
#from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . utils import *
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware


#from models import User, Post


#from  .database import engine, SessionLocal
#from sqlalchemy.orm import Session

# since we are using alembic we dont require the below
#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    
while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = 'localhost', database='Fastapi', user='postgres', password= 'Super@007', cursor_factory=RealDictCursor )

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as e:
        print(f"connecting to databse failed: {e}")
        time.sleep(2)


   

#def find_posts(id):
#    for p in my_posts:
#        if p["id"] == id:
#            return p
#
#def find_index_posts(id):
#    for i,p in enumerate(my_posts):
#        if p['id'] == id:
#            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "My App!!!"}


#@app.get("/posts/latest")
#def latest_post():
#    return my_posts[-1]

#@app.get("/sqlalchemy")    based on SQL alchemy
#def test_post(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return {"data": posts}






