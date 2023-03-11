from fastapi import FastAPI,HTTPException,Body
from typing import Union,Optional
from pydantic import BaseModel
from router import player_endpoint,creater,fight
from config.database import *

app = FastAPI()

origins = ["*"]

app.include_router(player_endpoint.router)
app.include_router(creater.router)
app.include_router(fight.router)

@app.get("/")
def root():
    return {"msg":"welcome to my little turn-based RPG!"}

@app.get("/enemy")
def get_all_enemy():
    return list(enemy.find({},{"_id":0}))

@app.get("/enemy/{enemy_id}")
def get_enemy(enemy_id:int):
    return enemy.find_one({"id":enemy_id},{"_id":0})

@app.get("/item/{item_id}")
def get_item(item_id:int):
    return item.find_one({"item_id":item_id},{"_id":0})

@app.get("/skill/{skill_id}")
def get_skill(skill_id:int):
    return skill.find_one({"skill_id":skill_id},{"_id":0})
