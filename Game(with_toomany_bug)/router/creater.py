from pydantic import BaseModel
from datetime import datetime,timedelta
from fastapi import APIRouter,HTTPException,Body
from config.database import *
from typing import Union,Optional,List

class Enemy(BaseModel):
    name:str
    id:int
    max_hp:int
    level:int
    attack:int
    defense:int
    speed:int
    ability:str
    gold_drop:int

class Skill(BaseModel):
    skill_id:int
    name:str
    type:str
    desc:str
    value:float
    duration:int

class Item(BaseModel):
    item_id:int
    name:str
    skill:str

router = APIRouter(prefix='/creater')

@router.post('/add/enemy')
def add_enemy(monster:Enemy):
    enemy.insert_one(monster.dict())
    return {"msg":"enemy added"}

@router.post('/add/skill')
def add_skill(sk:Skill):
    skill.insert_one(sk.dict())
    return {"msg":"skill added"}

@router.post('/add/item')
def add_item(it:Item):
    item.insert_one(it.dict())
    return {"msg":"item added"}

@router.delete('/delete/enemy')
def delete_enemy(monster:Enemy):
    enemy.delete_one(monster.dict())
    return {"msg":"enemy deleted"}

@router.delete('/delete/skill')
def delete_skill(sk:Skill):
    skill.delete_one(sk.dict())
    return {"msg":"skill deleted"}

@router.delete('/delete/item')
def delete_item(it:Item):
    item.delete_one(it.dict())
    return {"msg":"item deleted"}

@router.delete('/delete/all')
def delete_all():
    enemy.delete_many({})
    skill.delete_many({})
    item.delete_many({})
    player.delete_many({})
    store.delete_many({})
    fight_history.delete_many({})
    fight_count.delete_many({})
    not_find()
    return {"msg":"all deleted"}