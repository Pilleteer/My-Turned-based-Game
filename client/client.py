import os
import json
import requests
import time

base_URL = "http://localhost:8000/"
creater_URL = base_URL + "creater/"
player_URL = base_URL + "player/"
enemy_URL = base_URL + "enemy/"
fight_URL = base_URL + "fight/"

def exit():
    os._exit(0)

def buy_item():
    os.system('cls')
    print("-"*36)
    print("             Item List              ")
    print("-"*36)
    pl_gold=json.loads(requests.get(player_URL + "status").text)['gold']
    it_list=json.loads(requests.get(player_URL + "store").text)
    print("Current gold: " + str(pl_gold) + " gold")
    for i in it_list:
        item_name=i['name']
        print(str(i['store_id']) + ". " + item_name + " : " + str(i['price']) + " gold")
        last_id=i['store_id']
    print("0. Back")
    print("-"*36)
    choice = input("Enter your choice(0 to back): ")
    if choice == "0":
        store()
    elif int(choice) > last_id:
        print("Invalid input! Press enter to continue...")
        input()
        buy_item()
    elif pl_gold < it_list[int(choice)-1]['price']:
        print("You don't have enough gold! Press enter to continue...")
        input()
        buy_item()
    else:
        requests.put(player_URL + "store/" + str(choice))
        print("You bought " + it_list[int(choice)-1]['name'] + "! Press enter to continue...")
        input()
        buy_item()

def store():
    os.system('cls')
    print("-"*36)
    print("    Hello! Welcome to the store!    ")
    print("-"*36)
    print("1. Buy item")
    print("2. Back")
    print("-"*36)
    choice = input("Enter your choice: ")
    if choice == "1":
        buy_item()
    elif choice == "2":
        in_game()
    else:
        print("Invalid input!")
        store()

def init_fight():
    os.system('cls')
    print("Loading...")
    fight_id=json.loads(requests.post(fight_URL).text)['fight_id']
    fight_status=json.loads(requests.get(fight_URL + str(fight_id)).text)
    for i in fight_status:
        if i["type"] == "monster":
            en_bar=i
            break
    en=json.loads(requests.get(enemy_URL+str(en_bar['type_id'])).text)
    os.system('cls')
    print("-"*36)
    print("            Fight Start!            ")
    vs_txt="Versus: " + str(en['name']) + "!!"
    print(vs_txt.center(36-len(vs_txt)))
    print("-"*36)
    print("Press enter to continue...")
    input()
    fight(fight_id)

def fight_win(fight_id):
    os.system('cls')
    win_txt=json.loads(requests.put(fight_URL + str(fight_id) + "/win").text)
    print("You win!")
    print("Gained " + str(win_txt['exp_drop']) + " exp and " + str(win_txt['gold_drop']) + " gold!")
    if win_txt['level_up']:
        print("Level up!")
    print("Press enter to continue...")
    input()

def attack(fight_id, attacker_type):
    if attacker_type == "player":#player attack,return 1 if enemy still alive,return 0 if enemy dead
        fight_text=json.loads(requests.put(fight_URL + str(fight_id) + "/player", json={"act_type": "attack","act_type_id": 0}).text)
        if "status" in fight_text and fight_text['status'] == "win":
            fight_win(fight_id)
            return 0
        return 1
    elif attacker_type == "enemy":#enemy attack,return 1 if player still alive,return 0 if player dead
        fight_text=json.loads(requests.put(fight_URL + str(fight_id) + "/enemy").text)
        if fight_text['status'] == "lose":
            os.system('cls')
            lose_txt=json.loads(requests.put(fight_URL + str(fight_id) + "/lose").text)
            print("You lose!")
            print("Lost " + str(lose_txt['exp_lose']) + " exp and " + str(lose_txt['gold_lose']) + " gold!")
            print("Press enter to continue...")
            input()
            return 0
        return 1
    else:
        print("Invalid input!")

def use_skill(fight_id, skill_id):
    fight_text=json.loads(requests.put(fight_URL + str(fight_id) + "/player", json={"act_type": "skill", "act_type_id": skill_id}).text)
    if fight_text['status'] == "win":
        fight_win(fight_id)
        return 0
    return 1

def skill(fight_id):
    sk=json.loads(requests.get(player_URL + "status").text)['skill']
    os.system('cls')
    if sk == []:
        print("You don't have any skill! Press enter to continue...")
        input()
        return fight(fight_id)
    else:
        print("-"*36)
        print("             Skill List             ")
        print("-"*36)
        for i in sk:
            print(i['skill_id'] + "." + i['name'] + " : " + str(i['mp']) + " mp")
            last_id=i['skill_id']
        print("0. Back")
        print("-"*36)
        choice = input("Enter your choice(0 to back): ")
        if choice == "0":
            fight(fight_id)
        elif choice > last_id:
            print("Invalid input! Press enter to continue...")
            input()
            skill()
        else:
            return use_skill(fight_id, choice)
            

def fight(fight_id):
    os.system('cls')
    print("Loading...") 
    #print(fight_id)
    fight_status=json.loads(requests.get(fight_URL + str(fight_id)).text)
    for i in fight_status:
        if i["type"] == "monster":
            en_bar=i
        else:
            pl_bar=i
    print(fight_URL + "data/" + str(en_bar['type_id']))
    data=json.loads(requests.get(fight_URL + "data/" + str(en_bar['type_id'])).text)
    #print(data)
    pl=data['player']
    en=data['enemy']
    os.system('cls') 
    print("-"*36)
    print(pl['name'].center(36-len(pl['name'])))
    hp_txt="HP: " + str(pl_bar['remain_hp']) + "/" + str(pl['max_hp'])
    mp_txt="MP: " + str(pl_bar['remain_mp']) + "/" + str(pl['max_mp'])
    print(hp_txt+" "*(36-len(hp_txt)-len(mp_txt))+mp_txt)
    print("-"*36)
    print("VS".center(36-2))
    print("-"*36)
    print(str(en['name']).center(36-len(str(en['name']))))
    hp_txt="HP: " + str(en_bar['remain_hp']) + "/" + str(en['max_hp'])
    print(hp_txt)
    print("-"*36)
    print("Select your action: ")
    print("1. Attack")
    print("2. Skill")
    print("3. Item")
    print("4. Run")
    print("-"*36) 
    choice = input("Enter your choice: ")
    if en["speed"] > pl["speed"]:# must be changed depends on status
        if not attack(fight_id, "enemy"):
            return
    if choice == "1":
        if not attack(fight_id, "player"):
            return
    elif choice == "2":
        #display skill list
        if not skill(fight_id):
            return
    elif choice == "3":
        #display inventory
        if not inventory(True,fight_id):#beta
            return
    elif choice == "4":
        return in_game()
    if en["speed"] <= pl["speed"]:
        if not attack(fight_id, "enemy"):
            return
    fight(fight_id)

def inventory(Is_infight, fight_id):
    os.system('cls')
    inven=json.loads(requests.get(player_URL + "inventory").text)["inventory"]
    print("-"*36)
    print("Inventory".center(36-11))
    print("-"*36)
    for i in inven:
        print(str(i['item_id']) + "." + i['name'])
    print("0. Back")
    print("-"*36)
    choice = input("Enter your choice: "*Is_infight + "Pres enter to continue..."*(not Is_infight))
    if choice == "0":
        if Is_infight:
            fight(fight_id)
        else:
            in_game()
    elif int(choice) > len(inven):
        print("Invalid input! Press enter to continue...")
        input()
        inventory(Is_infight, fight_id)
    elif Is_infight:
        return use_skill(fight_id, inven[choice-1]['skill_id'])
    else:
        return in_game()

def status():
    os.system('cls')
    pl=json.loads(requests.get(player_URL + "status").text)
    print("-"*36)
    print("Status".center(36-6))
    print("-"*36)
    print("Name: " + pl['name'])
    print("Level: " + str(pl['level']))
    print("Exp: " + str(pl['exp']))
    print("Gold: " + str(pl['gold']))
    print("HP: " + str(pl['max_hp']))
    print("MP: " + str(pl['max_mp']))
    print("Attack: " + str(pl['attack']))
    print("Defense: " + str(pl['defense']))
    print("Speed: " + str(pl['speed']))
    print("-"*36)
    print("Press enter to continue...")
    input()
    in_game()    


def in_game():
    os.system('cls')
    print("-"*36)
    print("      Please choose an option:      ")
    print("-"*36)
    print("1. Go to the store")
    print("2. Go to the fight")
    print("3. Go to the inventory")
    print("4. Go to the status")
    print("5. Exit")
    print("-"*36)
    choice = input("Enter your choice: ")
    if choice == "1":
        store()
    elif choice == "2":
        init_fight()
    elif choice == "3":
        inventory(False,0)
    elif choice == "4":
        status()
    elif choice == "5":
        print("Bye!")
        return exit()
    else:
        print("Invalid input!")
    in_game()

def init_game():
    os.system('cls')
    print("-"*36)
    print("Welcome to my little turn-based RPG!")
    print("-"*36)
    print("1. Start a new game")
    print("2. Continue")
    print("3. Exit")
    print("-"*36)
    choice = input("Enter your choice: ")
    if choice == "1":
        requests.delete(creater_URL + "delete/all")
        print("Please enter your name: ")
        name = input()
        requests.put(player_URL + name)
        return in_game()
    elif choice == "2":
        return in_game()
    elif choice == "3":
        print("Bye!")
        return exit()
        

init_game()