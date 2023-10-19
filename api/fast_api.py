from fastapi import FastAPI
from sqlalc import engine, Sql_connect
import os
from config.config import yar_link
from pars_main import Combine
from dotenv import load_dotenv


app = FastAPI()
db = Sql_connect(engine)
load_dotenv("api\config\.env")


@app.get("/")
def start():
    return {"DDSD": "ddwed"}


@app.get("/api/score")
def func(sn: int):
    a = db.search_db_as_dict(sn)
    return a


@app.get("/update")
def update_database(password: str):
    if password == os.getenv("API_UPDATE_PASSWORD"):
        a = Combine(yar_link)
        a.db_filling()
