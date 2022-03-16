import pandas as pd

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pymongo import MongoClient

# from secret_data import PASSWORD
from mypackage.secret_data import PASSWORD


class User(BaseModel):
    name: str
    roll_no: int
    branch: str

app = FastAPI()
URL = f"mongodb+srv://theera:{PASSWORD}@cluster0.lcjgr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = MongoClient(URL)
db = client.get_database("student_db")
records = db.student_record

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI with MongoDB",
        "document_counts": records.count_documents({})
    }

@app.get("/all_user/")
async def all_user():
    cursor = records.find({})
    data = []
    for item in cursor:
        data.append({
            "name": item["name"],
            "roll_no": item["roll_no"],
            "branch": item["branch"]
        })
    return {
        "data": data
    }

@app.post("/create_user/")
async def create_user(user: User):
    records.insert_one({
        "name": user.name,
        "roll_no": user.roll_no,
        "branch": user.branch
    })
    return {
        "status": "ok"
    }

@app.post("/upload_file/")
async def upload_file(upload_file: UploadFile = File(...)):
    df = pd.read_excel(upload_file.file.read())
    for i in range(len(df)):
        records.insert_one({
            "name": df.iloc[i]["name"],
            "roll_no": int(df.iloc[i]["roll_no"]),
            "branch": df.iloc[i]["branch"]
        })
    return {
        "status": "ok"
    }