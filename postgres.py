from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
from typing import List
from psycopg2.errors import UniqueViolation

app = FastAPI()

#AnnotatedCurrentUser
# json_response

#models
class User(BaseModel):
    username: str
    password: str

#config.py
def get_db_connection():
    connection = psycopg2.connect(
        dbname="fastapi_database",  
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    return connection

#main file
@app.post("/add_user/")
def add_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #database.py
    query = """INSERT INTO users (username, password) VALUES (%s, %s) RETURNING username;"""
    try:
        cursor.execute(query, (user.username, user.password))
    except UniqueViolation as e:
        return {"message":"Cannot insert user!"}
     
     
    username = cursor.fetchone()
    if username:
        user_id=username[0] 
    
    conn.commit()
    
    cursor.close()
    conn.close()
    
    #json response: message with status code plus exception handling.
    return {"username": user.username, "email": user.password}



@app.post("/admin")
def verify_admin(user:User):
    conn= get_db_connection()
    cursor= conn.cursor()
    return {"message":"Welcome admin!"} if(user.username=="admin") else {"message":"Invalid user"}