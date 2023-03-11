from pydantic import BaseModel
from datetime import datetime,timedelta
from fastapi import APIRouter,HTTPException,Body
from config.database import *
from typing import Union,Optional,List
from random import randint

class Act_info(BaseModel):
    act_type:str
    act_type_id:int

class Buff_info(BaseModel):
    buff_name:str
    fight_id:int

class Fight_history(BaseModel):
    fight_id:int
    type:str
    type_id:int
    remain_hp:int
    status:List[str]=[]

router = APIRouter(prefix='/fight')

# def damage_calc(attack,defense):
#     dmg=attack-defense
#     if dmg<0:
#         dmg=1
#     return dmg
def damage_calc(attack,defense,attacker_type,fight_id):
    fh_pl=fight_history.find_one({'fight_id':fight_id,'type':"player"},{'_id':0})
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    dmg=attack-defense
    if dmg<=0:
        dmg=1
    if attacker_type=="monster":
        if fh_pl['remain_hp']<=0:
            raise HTTPException(status_code=400,detail="player already dead")
        if fh_pl['remain_hp']-dmg<=0:
            fh_pl['remain_hp']=0
        else:
            fh_pl['remain_hp']-=dmg
        if ('ability'in en and en['ability']!="normal") and fh_pl['status'].count(en['ability'])==0:
            fh_pl['status'].append(en['ability'])
        fight_history.update_one({'fight_id':fight_id,'type':"player"},{'$set':{'remain_hp':fh_pl['remain_hp'],'status':fh_pl['status']}})
        if fh_pl['remain_hp']<=0:
            return {"msg":"Enemy deal " + dmg + " damage,You was dead",'status':'lose'}
        return {"msg":"player was attacked for " + str(dmg) + " damage",'status':'fighting'}
    if attacker_type=="player":
        if fh_en['remain_hp']<=0:
            raise HTTPException(status_code=400,detail="enemy already dead")
        if fh_en['remain_hp']-dmg<=0:
            fh_en['remain_hp']=0
        else:
            fh_en['remain_hp']-=dmg
        if ('ability' in pl and pl['ability']!="normal") and fh_en['status'].count(pl['ability'])==0:
            fh_en['status'].append(pl['ability'])
        fight_history.update_one({'fight_id':fight_id,'type':"monster"},{'$set':{'remain_hp':fh_en['remain_hp'],'status':fh_en['status']}})
        if fh_en['remain_hp']<=0:
            return {"msg":"player deal " + str(dmg) + " damage,Enemy was dead",'status':'win'}
        return {"msg":"enemy was attacked",'status':'fighting'}
    else:
        raise HTTPException(status_code=400,detail="attacker type error")

def use_skill(skill_name,fight_id):
    fh_pl=fight_history.find_one({'fight_id':fight_id,'type':"player"},{'_id':0})
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    sk=skill.find_one({'name':skill_name},{'_id':0})
    if not sk:
        raise HTTPException(status_code=400,detail="skill not found")
    if sk['skill_type']=="attack":
        return damage_calc(pl['attack']*sk['value'],en['defense'],"player",fight_id)
    if fh_pl['remain_mp']<sk['mp']:
        return {"msg":"not enough mp"}
    elif sk['skill_type']=="buff":
        if fh_pl['status'].count(sk['desc'])==0:
            fh_pl['status'].append(sk['desc'])
        fight_history.update_one({'fight_id':fight_id,'type':"player"},{'$set':{'status':fh_pl['status']}})
        return {"msg":"player was buffed"}
    elif sk['skill_type']=="debuff":
        if fh_en['status'].count(sk['desc'])==0:
            fh_en['status'].append(sk['desc'])
        fight_history.update_one({'fight_id':fight_id,'type':"monster"},{'$set':{'status':fh_en['status']}})
        return {"msg":"enemy was debuffed"}
    else:
        raise HTTPException(status_code=400,detail="skill type error")

@router.get('/')
def get_fight_id():
    fight_cnt=fight_count.find_one({},{'_id':0})
    return {"fight_id":fight_cnt['count']}

@router.post('/')
def get_fight_enemy():
    en=list(enemy.find({},{'_id':0}))
    pl=player.find_one({},{'_id':0})
    fight_cnt=fight_count.find_one({},{'_id':0})
    rand_enemy=randint(0,len(en)-1)
    fight_history.insert_one({'fight_id':fight_cnt['count']+1,'type':"monster",'type_name':en[rand_enemy]["name"],'type_id':en[rand_enemy]['id'],'remain_hp':en[rand_enemy]['max_hp'],'max_hp':en[rand_enemy]['max_hp'],'status':[],'fight_date':str(datetime.now())})
    fight_history.insert_one({'fight_id':fight_cnt['count']+1,'type':"player",'type_name':pl["name"],'type_id':1,'remain_hp':pl['max_hp'],'max_hp':pl['max_hp'],'remain_mp':pl['max_mp'],'max_mp':pl['max_mp'],'status':[],'fight_date':str(datetime.now())})
    fight_count.update_one({},{'$set':{'count':fight_cnt['count']+1}})
    return {"fight_id":fight_cnt['count']+1}

@router.get('/data/{enemy_id}')
def get_monster_and_playerinfo(enemy_id:int):
    return {"player":player.find_one({},{'_id':0}),"enemy":enemy.find_one({"id":enemy_id},{"_id":0})}

@router.get('/{fight_id}')
def get_fight_history(fight_id:int):
    return list(fight_history.find({'fight_id':fight_id},{'_id':0}))

@router.put('/{fight_id}/enemy')
def update_player_attacked(fight_id:int):
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    return damage_calc(en['attack'],pl['defense'],"monster",fight_id)

@router.put('/{fight_id}/player')
def update_enemy_attacked(fight_id:int,act_info:Act_info):
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    if fh_en['remain_hp']<=0:
        raise HTTPException(status_code=400,detail="enemy already dead")
    if act_info.act_type=="attack":
        return damage_calc(pl['attack'],en['defense'],"player",fight_id)
    elif act_info.act_type=="item":
        it=item.find_one({'item_id':act_info.act_type_id},{'_id':0})
        if not it:
            raise HTTPException(status_code=400,detail="item not found")
        if not it['name'] in pl['inventory']:
            raise HTTPException(status_code=400,detail="item not found in player's item") 
        else:
            pl["inventory"]["amount"]-=1
            if pl["inventory"]["amount"]==0:
                pl["inventory"].remove(it['name'])
            player.update_one({},{'$set':{'inventory':pl['inventory']}})
            return use_skill(it['skill'],fight_id)   
    elif act_info.act_type=="skill":
        sk=skill.find_one({'skill_id':act_info.act_type_id},{'_id':0})
        return use_skill(sk['name'],fight_id)
    
@router.put('/{fight_id}/win')
def update_player_win(fight_id:int):
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    exp_drop=(en['level']/pl['level'])*10
    lv_up=0
    pl['exp']+=exp_drop
    pl['gold']+=en['gold_drop']
    while pl['exp']>=100:
        pl['level']+=1
        pl['exp']-=100
    player.update_one({},{'$set':{'exp':pl['exp'],'gold':pl['gold'],'level':pl['level']}})
    return {"msg":"player win","exp_drop":exp_drop,"gold_drop":en['gold_drop'],'level_up':lv_up}

@router.put('/{fight_id}/lose')
def update_player_lose(fight_id:int):
    fh_en=fight_history.find_one({'fight_id':fight_id,'type':"monster"},{'_id':0})
    en=enemy.find_one({'id':fh_en['type_id']},{'_id':0})
    pl=player.find_one({},{'_id':0})
    exp_lose=pl['exp']*0.5
    gold_lose=pl['gold']*0.1
    if pl['exp']<exp_lose:
        exp_lose=pl['exp']
    if pl['gold']<gold_lose:
        gold_lose=pl['gold']
    pl['exp']-=exp_lose
    pl['gold']-=gold_lose
    player.update_one({},{'$set':{'exp':pl['exp'],'gold':pl['gold']}})
    return {"msg":"player lose","exp_lose":exp_lose,"gold_lose":gold_lose}

@router.get("/buff/{buff_name}")
def get_buff_duration(buff_name:str):
    sk=skill.find_one({'name':buff_name},{'_id':0})
    return sk['duration']

@router.put("/buff/end")
def update_buff_end(buff_info:Buff_info):
    sk=skill.find_one({'name':buff_info.buff_name},{'_id':0})
    fh_pl=fight_history.find_one({'fight_id':buff_info.fight_id,'type':"player"},{'_id':0})
    fh_pl['status'].remove(sk['desc'])
    fight_history.update_one({'fight_id':buff_info.fight_id,'type':"player"},{'$set':{'status':fh_pl['status']}})
    return {"msg":"buff ended"}