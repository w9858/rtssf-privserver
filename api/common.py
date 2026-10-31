"""Compatibility helpers backed by the current request's SQLite transaction."""
import json
from flask import g
from google.protobuf import json_format as jf
from werkzeug.exceptions import BadRequest
from proto import common_pb2 as pb
from storage import read_document, write_document


def document(name):
    return read_document(g.db, name)


def save(name, value):
    write_document(g.db, name, value)


def read(filename):
    return json.dumps(document(filename), ensure_ascii=False)


def update_resource_result():
    result = pb.UpdateResourceResult()
    for name in ('t_user_unit_list', 't_user_item_list', 't_user', 't_user_event_list',
                 't_user_crystal', 't_user_weapon_list', 't_user_weapon_skill_list',
                 't_user_weapon_status_list'):
        jf.Parse(read(name), result)
    jf.Parse(load_worker(), result.t_user_worker)
    return result


def load_worker():
    return json.dumps(document('t_user_worker_list')['t_user_worker_list'][0])


def set_user(field, value):
    data = document('t_user')
    data['t_user'][field] = value
    save('t_user', data)


def add_user(field, amount):
    user = document('t_user')['t_user']
    value = user.get(field, 0) + amount
    if not 0 <= value <= 2147483647:
        raise BadRequest('Resource amount out of range')
    set_user(field, value)


def add_user_exp(amount): add_user('exp', amount)
def add_user_gold(amount): add_user('gold', amount)
def add_user_friend_point(amount): add_user('friend_point', amount)


def change_comment(value):
    if len(value) > 200: raise BadRequest('Comment exceeds 200 characters')
    set_user('comment', value)


def change_name(value):
    if not value.strip() or len(value) > 32: raise BadRequest('Name must contain 1–32 characters')
    set_user('name', value)


def owned(name, field, value):
    if not any(row.get(field) == value for row in document(name)[name]):
        raise BadRequest(f'Unknown {field}')


def change_emblem(value):
    if value: owned('t_user_emblem_list', 'emblem_id', value)
    set_user('emblem_id', value)


def change_friend_unit(value):
    owned('t_user_unit_list', 'unit_id', value)
    set_user('friend_unit_id', value)


def change_home_bg(value):
    owned('t_user_background_list', 'background_id', value)
    set_user('home_background_id', value)


def change_home_unit(value, num):
    if value: owned('t_user_unit_list', 'unit_id', value)
    set_user(f'home_unit_id_{num}', value)


def deck_load_one(num):
    decks = document('t_user_deck_list')['t_user_deck_list']
    deck = next((d for d in decks if d['deck_no'] == num), None)
    if deck is None: raise BadRequest('Unknown deck number')
    return json.dumps(deck)


def deck_change_name(name, num):
    if not name.strip() or len(name) > 32: raise BadRequest('Deck name must contain 1–32 characters')
    data = document('t_user_deck_list')
    deck = json.loads(deck_load_one(num))
    deck['name'] = name
    data['t_user_deck_list'] = [deck if d['deck_no'] == num else d for d in data['t_user_deck_list']]
    save('t_user_deck_list', data)


def deck_save(newdata):
    deck_change_name(newdata.name, newdata.deck_no)
    data = document('t_user_deck_list')
    deck = next(d for d in data['t_user_deck_list'] if d['deck_no'] == newdata.deck_no)
    units = []
    for field in ('unit_id_1', 'unit_id_2', 'unit_id_3', 'sub_unit_id_1', 'sub_unit_id_2', 'sub_unit_id_3'):
        value = getattr(newdata, field)
        if value:
            owned('t_user_unit_list', 'unit_id', value)
            if value in units: raise BadRequest('A unit cannot occupy two deck slots')
            units.append(value)
        deck[field] = value
    save('t_user_deck_list', data)


def quest_clear(num, m1=False, m2=False, m3=False):
    if num <= 0: raise BadRequest('Quest ID must be positive')
    data = document('t_user_quest_list')
    quests = data['t_user_quest_list']
    quest = next((q for q in quests if q['quest_id'] == num), None)
    if quest is None:
        quest = {'quest_id': num, 'clear_count': 0}
        quests.append(quest)
    quest['clear_count'] += 1
    for i, flag in enumerate((m1, m2, m3), 1):
        field = f'quest_mission_id_{i}'
        # Never erase an already completed mission on a later run.
        quest[field] = max(quest.get(field, 0), int(flag))
    save('t_user_quest_list', data)
    return quest


def mark_archive(num):
    if num <= 0: raise BadRequest('Quest ID must be positive')
    data = document('t_user_archive_list')
    archive = next((q for q in data['t_user_archive_list'] if q['quest_id'] == num), None)
    if archive is None:
        archive = {'quest_id': num}
        data['t_user_archive_list'].append(archive)
    archive['read_flag'] = 1
    save('t_user_archive_list', data)


def adv_clear(num):
    quest = quest_clear(num)
    mark_archive(num)
    return quest


def weapon_equip(unit_id, user_weapon_id):
    owned('t_user_unit_list', 'unit_id', unit_id)
    if user_weapon_id: owned('t_user_weapon_list', 'user_weapon_id', user_weapon_id)
    data = document('t_user_unit_weapon_list')
    # A weapon belongs to one unit; moving it removes its previous assignment.
    data['t_user_unit_weapon_list'] = [row for row in data['t_user_unit_weapon_list']
        if row['unit_id'] != unit_id and (not user_weapon_id or row['user_weapon_id'] != user_weapon_id)]
    if user_weapon_id:
        data['t_user_unit_weapon_list'].append({'user_id': 1, 'unit_id': unit_id, 'user_weapon_id': user_weapon_id})
    save('t_user_unit_weapon_list', data)
