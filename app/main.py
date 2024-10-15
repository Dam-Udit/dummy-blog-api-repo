import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth


load_dotenv(dotenv_path=".env")

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWD = os.getenv('POSTGRES_PASSWD')

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print(f"Connecting to database failed: {e}")
        time.sleep(5)


@app.get("/")
def root():
    return {"message": "Welcome to my API!"}
