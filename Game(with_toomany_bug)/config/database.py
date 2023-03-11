from pymongo import MongoClient
import json

MONGO_DB_URL = "mongodb://localhost"
MONGO_DB_PORT = 27017
DATABASE_NAME = "RPGTurnbasedGame"

client = MongoClient(f"{MONGO_DB_URL}:{MONGO_DB_PORT}")
db = client[DATABASE_NAME]
player = db['Player_Status']
enemy = db['Monster_Status']
skill = db['Skill_info']
store = db['Store']
item = db['Item']
fight_history = db['Fight_History']
fight_count = db['Fight_Count']

def not_find():
    if not player.find_one({}): #can make other save slot
        player.insert_one({"name":"player","gold":0,"max_hp":100,"max_mp":100,"attack":20,"defense":10,"speed":10,"exp":0,"level":1,"status_point":0,"inventory":[],"skill":[]})
    
    if not enemy.find_one({}):
        a = json.load(open('config/init_data/init_enemy.json'))
        for i in a['init_enemy']:
            enemy.insert_one(i)

    if not skill.find_one({}):
        a = json.load(open('config/init_data/init_skill.json'))
        for i in a['init_skill']:
            skill.insert_one(i)

    if not item.find_one({}):
        a = json.load(open('config/init_data/init_item.json'))
        for i in a['init_item']:
            item.insert_one(i)
            
    if not store.find_one({}):
        a = json.load(open('config/init_data/init_store.json'))
        for i in a['init_store']:
            store.insert_one(i)

    if not fight_count.find_one({}):
        fight_count.insert_one({"count":0})

not_find()