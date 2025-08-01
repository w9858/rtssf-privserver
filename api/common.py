from proto import common_pb2 as pb
from google.protobuf import json_format as jf
import json

def read(filename):
    with open("./data/"+ filename + ".json", mode="r", encoding="utf-8") as f:
        # data = json_format.Parse(f.read(), pb.TUser())
        # print(type(data))
        return f.read()

def update_resource_result():
    urr = pb.UpdateResourceResult()
    jf.Parse(read("t_user_unit_list"), urr)
    jf.Parse(read("t_user_item_list"), urr)
    jf.Parse(read("t_user"), urr)
    jf.Parse(read("t_user_event_list"), urr)
    jf.Parse(read("t_user_crystal"), urr)
    jf.Parse(load_worker(), urr.t_user_worker)
    return urr

def load_worker():
    with open("./data/t_user_worker_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
        data = data["t_user_worker_list"][0]
        data = json.dumps(data)
    return data

# user data

def add_user_exp(amount):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["exp"] += amount
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def add_user_gold(amount):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["gold"] += amount
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def add_user_friend_point(amount):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["friend_point"] += amount
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

# user profile

def change_comment(newdata):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["comment"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def change_emblem(newdata):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["emblem_id"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def change_friend_unit(newdata):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["friend_unit_id"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def change_home_bg(newdata):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["home_background_id"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def change_home_unit(newdata, num):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"][f"home_unit_id_{num}"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def change_name(newdata):
    with open("./data/t_user.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user"]["name"] = newdata
    with open("./data/t_user.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

# deck

def deck_load_one(num):
    with open("./data/t_user_deck_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data = data["t_user_deck_list"][num-1]
    data = json.dumps(data)
    return data

def deck_change_name(name, num):
    with open("./data/t_user_deck_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user_deck_list"][num - 1]["name"] = name
    with open("./data/t_user_deck_list.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

def deck_save(newdata):
    with open("./data/t_user_deck_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    data["t_user_deck_list"][newdata.deck_no - 1]["name"] = newdata.name
    data["t_user_deck_list"][newdata.deck_no - 1]["unit_id_1"] = newdata.unit_id_1
    data["t_user_deck_list"][newdata.deck_no - 1]["sub_unit_id_1"] = newdata.sub_unit_id_1
    data["t_user_deck_list"][newdata.deck_no - 1]["unit_id_2"] = newdata.unit_id_2
    data["t_user_deck_list"][newdata.deck_no - 1]["sub_unit_id_2"] = newdata.sub_unit_id_2
    data["t_user_deck_list"][newdata.deck_no - 1]["unit_id_3"] = newdata.unit_id_3
    data["t_user_deck_list"][newdata.deck_no - 1]["sub_unit_id_3"] = newdata.sub_unit_id_3
    with open("./data/t_user_deck_list.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

#quest

def quest_clear(num, m1, m2, m3):
    # print(num, m1, m2, m3)
    with open("./data/t_user_quest_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    quest_ids = [q['quest_id'] for q in data['t_user_quest_list']]
    if num in quest_ids:
        idx = quest_ids.index(num)
        quest = data['t_user_quest_list'][idx]
        quest['quest_mission_id_1'] = int(m1)
        quest['quest_mission_id_2'] = int(m2)
        quest['quest_mission_id_3'] = int(m3)
        quest['clear_count'] += 1
    else:
        data['t_user_quest_list'].append({
            "clear_count": 1,
            "quest_id": num,
            'quest_mission_id_1': int(m1),
            'quest_mission_id_2': int(m2),
            'quest_mission_id_3': int(m3)
        })
    with open("./data/t_user_quest_list.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, ensure_ascii=False)

def adv_clear(num):
    with open("./data/t_user_quest_list.json", mode="r", encoding="utf-8") as f:
        quest_data = json.load(f)
    quest_found = False
    for i, quest in enumerate(quest_data['t_user_quest_list']):
        if quest['quest_id'] == num:
            # already seen
            quest_data['t_user_quest_list'][i]['clear_count'] += 1
            quest_found = True
            break
    if not quest_found:
        # new clear data
        quest_data['t_user_quest_list'].append({"clear_count": 1, "quest_id": num})
    with open("./data/t_user_quest_list.json", mode="w", encoding="utf-8") as f:
        json.dump(quest_data, f, sort_keys=True, ensure_ascii=False)

    with open("./data/t_user_archive_list.json", mode="r", encoding="utf-8") as f:
        archive_data = json.load(f)
    archive_found = False
    for archive in archive_data['t_user_archive_list']:
        if archive['quest_id'] == num:
            archive_found = True
            break
    if not archive_found:
        # new clear data
        archive_data['t_user_archive_list'].append({"quest_id": num, "read_flag": 1})
    with open("./data/t_user_archive_list.json", mode="w", encoding="utf-8") as f:
        json.dump(archive_data, f, sort_keys=True, ensure_ascii=False)

# def boardup(unitid, sheet_no, progress_adj):

# weapon

def weapon_equip(unit_id, user_weapon_id):
    with open("./data/t_user_unit_weapon_list.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
    if user_weapon_id == 0:
        for i, item in enumerate(data["t_user_unit_weapon_list"]):
            if item["unit_id"] == unit_id:
                del data["t_user_unit_weapon_list"][i]
                break
    else:
        for i, item in enumerate(data["t_user_unit_weapon_list"]):
            if item["unit_id"] == unit_id:
                data["t_user_unit_weapon_list"][i]["user_id"] = 0
                data["t_user_unit_weapon_list"][i]["unit_id"] = unit_id
                data["t_user_unit_weapon_list"][i]["user_weapon_id"] = user_weapon_id
                break
        else:
            data["t_user_unit_weapon_list"].append({
                "user_id": 0,
                "unit_id": unit_id,
                "user_weapon_id": user_weapon_id
            })
    with open("./data/t_user_unit_weapon_list.json", mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
