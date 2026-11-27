from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def display():
    return{
        "message":"api running"
    }
def db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="myuser",
        password="mypassword",
        dbname="mydb"
    )

class login(BaseModel):
    user_name:str
    password:str

class register(BaseModel):
    user_name:str
    password:str    

@app.post("/login_check")
def login_check(l:login):
    conn=db_connection()
    cursor=conn.cursor()
    s="select * from login_data where user_name=%s AND password=%s"
    values=[l.user_name,l.password]
    cursor.execute(s,values)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return{
            "message":"Login successful"
        }
    return{
        "message":"Invalide user name and password"
    }

@app.post("/register_data")
def register_data(r:register):
    conn=db_connection()
    cursor=conn.cursor()
    s="INSERT INTO login_data (user_name, password) VALUES (%s, %s)"
    values=[r.user_name,r.password]
    cursor.execute(s,values)
    conn.commit()
    cursor.close()
    conn.close()
    return{
        "message":"sign up successful"
    }

