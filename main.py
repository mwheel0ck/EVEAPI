from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3


app = FastAPI()

class print(BaseModel):
    name: str
    id: int
    gid: int

class material(BaseModel):
    name: str
    id: int
    gid: int
    amount: int


@app.get("/v1/ListPrints")
def index():
    con = sqlite3.connect("sqlite-latest.sqlite")
    cur=con.cursor()
    prints = []

    for row in cur.execute("SELECT typeName, typeID, groupID from invTypes WHERE typeNAME like '%blueprint'"):
        prints.append(print(name=row[0], id=row[1], gid=row[2]))
        

    prints_json = jsonable_encoder(prints)
    return JSONResponse(content=prints_json)

@app.get("/v1/ListMaterials")
def ListMaterials(PrintID: int):
    Materials = []
    con = sqlite3.connect("sqlite-latest.sqlite")
    cur=con.cursor()
    query = "SELECT iam.materialTypeID,it.typename,it.groupid,iam.quantity FROM industryactivitymaterials iam join invtypes it on iam.materialtypeid = it.typeid WHERE iam.typeid = " + str(PrintID)
    for row in cur.execute(query):
        Materials.append(material(name=row[1], id=row[0], gid=row[2], amount=row[3]))
    materials_json = jsonable_encoder(Materials)
    return JSONResponse(content=materials_json)
