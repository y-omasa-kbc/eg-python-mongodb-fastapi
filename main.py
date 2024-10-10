import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient



load_dotenv(verbose=True)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_SERVER = os.getenv("MONGO_SERVER")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")

mongo_connecter = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_SERVER}:{MONGO_PORT}/'

# 住所録エントリーのモデル
class AddressEntry(BaseModel):
    no: int
    name: str
    address: str
    phone_number: str

# サーバー起動時にMongoDBに接続してから開始。終了まで接続を維持
@asynccontextmanager
async def lifespan(app: FastAPI):
    with MongoClient(mongo_connecter) as client:
        app.db = client[MONGO_DB]
        yield
    
app = FastAPI(lifespan=lifespan)

# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)



# Create - 新しい住所録エントリーを作成
@app.post("/address/", response_model=AddressEntry)
def create_address(entry: AddressEntry):
    if (app.db['address'].find_one({"no": entry.no})) is None:
        app.db['address'].insert_one(entry.model_dump())    
        return entry
    raise HTTPException(status_code=400, detail="No. already exists")

# Read - すべての住所録エントリーを取得
@app.get("/address/", response_model=List[AddressEntry])
def get_all_addresses():
    address_all = list(app.db['address'].find())
    return address_all

# Read - 特定のIDの住所録エントリーを取得
@app.get("/address/{entry_no}", response_model=AddressEntry)
def get_address(entry_no: int):
    if (address := app.db['address'].find_one({"no": entry_no})) is not None:
        return address
    raise HTTPException(status_code=404, detail="Entry not found")

# Update - 特定のIDの住所録エントリーを更新
@app.put("/address/{entry_no}", response_model=AddressEntry)
def update_address(entry_no: int, updated_entry: AddressEntry):
    if (address := app.db['address'].find_one({"no": entry_no})) is not None:
        app.db['address'].update_one(
            {"_id": address["_id"]}, {"$set": updated_entry.model_dump()}
        )
        return updated_entry

    raise HTTPException(status_code=404, detail="Entry not found")

# Delete - 特定のIDの住所録エントリーを削除
@app.delete("/address/{entry_no}", response_model=AddressEntry)
def delete_address(entry_no: int):
    if (address := app.db['address'].find_one({"no": entry_no})) is not None:
        app.db['address'].delete_one( {"_id": address["_id"]} )
        return address

    raise HTTPException(status_code=404, detail="Entry not found")

