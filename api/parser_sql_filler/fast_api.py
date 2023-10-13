from fastapi import FastAPI
from sqlalc import engine,Sql_connect
import os, sys
from config.config import API_UPDATE_PASSWORD, yar_link
from pars_main import Combine


app = FastAPI()
db = Sql_connect(engine)

@app.get("/")
def start():
    return {"DDSD":"ddwed"}
    
@app.get("/api/score")
def func(sn:int):
    a = db.search_db_as_dict(sn)
    return a

@app.get("/update")
def update_database(password:str):
    if password == API_UPDATE_PASSWORD:
        a = Combine(yar_link)
        a.db_filling()
 



