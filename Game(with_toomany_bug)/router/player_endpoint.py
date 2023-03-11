from pydantic import BaseModel
from fastapi import APIRouter,HTTPException,Body
from config.database import *
from typing import Union,Optional,List
from random import randint

class Skill(BaseModel):
    skill_name:str
    skill_type:str
    skill_desc:str
    skill_mp:int
    skill_cd:int
    skill_duration:int

router = APIRouter(prefix='/player')

def update_player_inventory(item_id):
    pl=player.find_one({},{'_id':0})
    it=item.find_one({'item_id':item_id},{'_id':0})
    if not it:
        raise HTTPException(status_code=400,detail="item not found")
    if it not in pl['inventory']:
        pl['inventory'].append(it)
    else:#update item amount
        for i in pl['inventory']:
            if i['name']==it['name']:
                i['amount']+=1
    player.update_one({},{'$set':{'inventory':pl['inventory']}})
    return {"msg":"item added"}

@router.put('/{name}')
def update_player_name(name:str):
    player.update_one({},{'$set':{'player_name':name}})
    return {"msg":"name updated"}

@router.get('/status')
def get_player_status():
    return player.find_one({},{'_id':0})

@router.get('/inventory')
def get_player_inventory():
    return player.find_one({},{'_id':0,'inventory':1})

@router.put('/status/{stat}')
def update_player_status(stat:str):
    pl=player.find_one({},{'_id':0})
    if pl['status_point']==0:
        raise HTTPException(status_code=400,detail="insufficient status point")
    if stat=="hp":
        player.update_one({},{'$set':{'player_hp':pl['max_hp']}*1.1, 'status_point':pl['status_point']-1})
    elif stat=="mp":
        player.update_one({},{ '$set':{'max_mp':pl['max_mp']*1.1}, 'status_point':pl['status_point']-1})
    elif stat=="atk":
        player.update_one({},{ '$set':{'atk':pl['atk']+5}, 'status_point':pl['status_point']-1})
    elif stat=="def":
        player.update_one({},{ '$set':{'def':pl['def']+5}, 'status_point':pl['status_point']-1})
    elif stat=="spd":
        player.update_one({},{ '$set':{'spd':pl['spd']+1}, 'status_point':pl['status_point']-1})
    else:
        raise HTTPException(status_code=400,detail="status not found")
    return {"msg":"status updated"}

@router.put('/inventory/{item_id}')
def put_player_inventory(item_id:int):
    return update_player_inventory(item_id)

@router.delete('/inventory/{item_id}')
def delete_player_item(item_id:int):
    pl=player.find_one({},{'_id':0})
    it=item.find_one({'item_id':item_id},{'_id':0})
    if not it:
        raise HTTPException(status_code=400,detail="item not found")
    pl['inventory'].remove(it)
    player.update_one({},{'$set':{'inventory':pl['inventory']}})
    return {"msg":"item removed"}

@router.get('/store')
def get_store():
    return list(store.find({},{'_id':0}))

@router.put('/store/{store_id}')
def buy_item(store_id:int):
    pl=player.find_one({},{'_id':0})
    st=store.find_one({'store_id':store_id},{'_id':0})
    if pl['gold']<st['price']:
        raise HTTPException(status_code=400,detail="insufficient gold")
    if st['type']=="item":
        update_player_inventory(st['id'])
    elif st['type']=="skill":
        pl['skill'].append(st['skill'])
        player.update_one({},{'$set':{'skill':pl['skill']}})
        store.delete_one({'store_id':store_id})
    player.update_one({},{'$set':{'gold':pl['gold']-st['price']}})
    return {"msg":"item bought"}
