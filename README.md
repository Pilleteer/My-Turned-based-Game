# Database
### Player
Player information
|    Attributes    | Data type |
|------------------|-----------|
|     Player_ID    |    int    |//coming soon...
|       Name       |    str    |
|       Gold       |    int    |
|      Max_HP      |    int    |
|      Max_Mp      |    int    |
|       Level      |    int    |
|        EXP       |    int    |
|   Status_Point   |    int    |
|   Attack_Power   |    int    |
|      Defense     |    int    |
|       Speed      |    int    |
|       Skill      | list(str) |
|     inventory    | list(str) |//let do it later!!

### Player_count//coming soon...
|    Attributes    | Data type |
|------------------|-----------|
Exp gain can calculate in from of (monster'level/player's level)*10
### Equipment //coming soon...

### Enemy
Enemy Information
|    Attributes    | Data type |
|------------------|-----------|
|    Monster_ID    |    int    |//use for random monster
|       Name       |    str    |
|      Max_HP      |    int    |
|       Level      |    int    |
|   Attack_Power   |    int    |
|      Defense     |    int    |
|       Speed      |    int    |
|      Ability     |    str    |//["Buff","ATK+"] get after attacked
|     Gold_drop    |    int    |
### Skill
| Attributes | Data_type |
|------------|-----------|
|  Skill_ID  |    int    |
| Skill_Name |    str    |
|    Type    |    str    |//Buff,DeBuff or Attack
|    Value   |    int    |
|     MP     |    int    |
|    desc    |    str    |//what stat will increase/decrease
|  Duration  |    int    |//turn
|  Cooldown  |    int    |//turn

### Fight_History
history about previous and current fight
| Attributes | Data_type |
|------------|-----------|
|  Fight_ID  |    int    |
|    Type    |    str    |//monster or player
|  Type_name |    str    |
|   Type_ID  |    int    |//only monster for now
|Remaining_HP|    int    |
|   Max_HP   |    int    |
|Remaining_MP|    int    |//only Player
|   Max_MP   |    int    |
|   Status   | list(str) |//check if get buff or debuff
|    Date    |  datetime |

### Item
| Attributes | Data_type |
|------------|-----------|
|  Item_Id   |    int    |
|  Item_Name |    str    |
|   skill    |    int    |//add attribute later ex.skill book etc.
|   Amount   |    int    |

### Store
| Attributes | Data_type |
|------------|-----------|
|  Store_ID  |    int    |
|    Name    |    str    |
|    type    |    str    |//item or skill
|     ID     |    int    |//item or skill's id
|    price   |    int    |
//can add unlock condition

### player_act_info
| Attributes | Data_type |
|------------|-----------|
|    type    |    str    |//item,attack or skill
|   type_id  |    int    |

### Fight_Count
| Attributes | Data_type |
|------------|-----------|
|Fight_Count |    int    |

### Buff_info
| Attributes | Data_type |
|------------|-----------|
| buff_name  |    str    |
|  fight_id  |    int    |

# method

## def damage_calc(attack,defense,attacker_type)
update fighthistory after calculate damage from attack ,defense and attacker_type(player or monster)
return {"msg":"enemy/player was attacked/dead"}

## def use_skill(skill_name,fight_id)
player use skill and send to this function to update fight_history
return {"msg":"player/enemy was buffed/debuffed"} or damage_calc 

## GET get_status
get player's status

endpoint: /player/status   
return Player form

## PUT update_player_name(name:str)
update player and return msg to client

endpoint: /player/{name}
return {"msg":"name updated"}

## PUT update_player_status(stat:str)
player choose stat to upgrade and update to database

endpoint: /player/status/{stat}
return {"msg":"status updated"}

## PUT update_player_inventory(item_id:int)
player buy item from store and update inventory to database

endpoint: /player/inventory/{item_id}
return {"msg":"item added"}

## DELETE delete_player_item(item_id:int)
player have used item and update in datebase

endpoint: /player/inventory/{item_id}
return {"msg":"item removed"}

## GET get_store
player want to go to store and database return store data

endpoint: /player/store
return Store from

## PUT buy_item(store_id:int)
player buy item and update player inventory

endpoint: /player/store/{store_id}

## POST get_fight_enemy
player select to fight enemy and backend update random monster to fight_history and update to database

endpoint: /fight/
return fight_id

## GET get_fight_history(fight_id:int)
player want to view current fight

endpoint: /fight/{fight_id}
return fight_history from

## PUT update_player_attacked(fight_id:int)
enemy attack player and update to database

endpoint: /fight/{fight_id}/enemy
return {"msg":attack success,"status"}

## PUT update_enemy_attacked(fight_id:int,Actioninfo)
player use action and update to database

endpoint: /fight/{fight_id}/player
return {"msg":action success,"status"}

## PUT update_player_win(fight_id:int)
player win the fight and update player status

endpoint: /fight/{fight_id}/win
return {"msg":Status update}

## PUT update_player_lose(fight_id:int)
player lose the fight and lose some exp

endpoint: /fight/{fight_id}/lose
return {"msg":Status update}

## GET get_buff_duration(buff_name:str)
client get buff duration data from database

endpoint: /fight/buff/{buff_name}
return buff duration(int)

## PUT update_buff_end(Buff_info)
client update player status that buff has end

endpoint: /fight/buff/end
return {"msg":"Buff ended"}

## DELETE delete_all
client want to restart database and send to backend

endpoint /creater/delete/all
return {"msg":"all deleted"}