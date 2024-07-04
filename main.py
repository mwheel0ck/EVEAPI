from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3


app = FastAPI()

class resp(BaseModel):
    name: str
    id: int
    gid: int

@app.get("/v1/ListPrints")
def index():
    con = sqlite3.connect("sqlite-latest.sqlite")
    cur=con.cursor()
    prints = []

    for row in cur.execute("SELECT typeName, typeID, groupID from invTypes WHERE typeNAME like '%blueprint'"):
        prints.append(resp(name=row[0], id=row[1], gid=row[2]))
        

    prints_json = jsonable_encoder(prints)
    return JSONResponse(content=prints_json)
    