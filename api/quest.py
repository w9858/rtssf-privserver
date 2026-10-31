"""Sandbox quest lifecycle with persistent tokens and replay-safe settlement."""
import base64
from datetime import datetime, timezone
import random
import secrets
from flask import Blueprint, request, make_response
from google.protobuf import json_format as jf
from werkzeug.exceptions import BadRequest, Conflict
from proto import quest_pb2 as pb
from api import common as cm

bp = Blueprint('quest', __name__, url_prefix='/quest')


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def runs():
    try: return cm.document('quest_runs')
    except KeyError: return {}


def start(kind, request_class, response_class):
    query = request_class.FromString(request.data)
    if query.quest_id <= 0: raise BadRequest('Quest ID must be positive')
    if kind == 'battle': cm.deck_load_one(query.deck_no)
    history = runs()
    # Keep the most recent 32 runs, including completed replies for retries.
    while len(history) >= 32: history.pop(next(iter(history)))
    token = secrets.token_urlsafe(24)
    history[token] = dict(quest_id=query.quest_id, kind=kind, start_at=now())
    cm.save('quest_runs', history)
    response = response_class(token=token)
    jf.Parse(cm.load_worker(), response.t_user_worker)
    return make_response(response.SerializeToString())


def run_for(query, kind):
    history = runs()
    run = history.get(query.token)
    if run is None or run['quest_id'] != query.quest_id or run['kind'] != kind:
        raise Conflict('Quest token does not match an active run')
    if run.get('cancelled'): raise Conflict('Quest was already cancelled')
    return history, run


def status(response, query, run):
    response.t_user_quest_status.quest_id = query.quest_id
    response.t_user_quest_status.token = query.token
    response.t_user_quest_status.start_at = run['start_at']
    response.t_user_quest_status.end_at = now()


def settle(query, response, history, run):
    data = response.SerializeToString()
    run['reply'] = base64.b64encode(data).decode('ascii')
    cm.save('quest_runs', history)
    return make_response(data)


@bp.post('/start_adv')
def start_adv(): return start('adventure', pb.RequestStartAdv, pb.ResponseStartAdv)


@bp.post('/start')
def start_battle(): return start('battle', pb.RequestStart, pb.ResponseStart)


@bp.post('/clear_adv')
def clear_adv():
    query = pb.RequestClearAdv.FromString(request.data)
    history, run = run_for(query, 'adventure')
    if 'reply' in run: return make_response(base64.b64decode(run['reply']))
    response = pb.ResponseClearAdv()
    jf.ParseDict(cm.adv_clear(query.quest_id), response.t_user_quest)
    status(response, query, run)
    jf.Parse(cm.read('t_user'), response)
    jf.Parse(cm.read('t_user_archive_list'), response)
    jf.Parse(cm.load_worker(), response.t_user_worker)
    return settle(query, response, history, run)


@bp.post('/clear')
def clear_battle():
    query = pb.RequestClear.FromString(request.data)
    history, run = run_for(query, 'battle')
    if 'reply' in run: return make_response(base64.b64decode(run['reply']))
    response = pb.ResponseClear(is_friend=True, friend_point=1)
    previous = next((q for q in cm.document('t_user_quest_list')['t_user_quest_list']
                     if q['quest_id'] == query.quest_id), {})
    flags = (query.is_clear_mission_1, query.is_clear_mission_2, query.is_clear_mission_3)
    first_complete = all(flags) and not all(previous.get(f'quest_mission_id_{i}') for i in (1, 2, 3))
    jf.ParseDict(cm.quest_clear(query.quest_id, *flags), response.t_user_quest)
    status(response, query, run)
    # These are the upstream server's sandbox rewards, not original game tables.
    for item_id in (101070101, 101070201, 101070301, 101070401):
        response.drop_list.add(resource_type=1, resource_id=item_id, resource_value_id=1, amount=5)
    if first_complete:
        response.mission_complete_reward_list.add(resource_type=1, resource_id=190101001,
                                                  resource_value_id=1, amount=1)
    items = cm.document('t_user_item_list')
    for reward in [*response.drop_list, *response.mission_complete_reward_list]:
        row = next((i for i in items['t_user_item_list'] if i['item_id'] == reward.resource_id), None)
        if row is None:
            row = dict(user_id=1, item_id=reward.resource_id, amount=0)
            items['t_user_item_list'].append(row)
        if row['amount'] + reward.amount > 2147483647: raise BadRequest('Item amount out of range')
        row['amount'] += reward.amount
    cm.save('t_user_item_list', items)
    cm.add_user_exp(180)
    cm.add_user_friend_point(1)
    cm.add_user_gold(random.choice((8000, 5000, 12000, 2500)))
    jf.Parse(cm.read('t_user_character_friendly_list'), response)
    jf.Parse(cm.read('t_user_archive_list'), response)
    response.update_resource_result.CopyFrom(cm.update_resource_result())
    return settle(query, response, history, run)


def cancel(query, response_class):
    history = runs()
    if hasattr(query, 'token'):
        run = history.get(query.token)
        if run is None or run['quest_id'] != query.quest_id: raise Conflict('Unknown quest run')
        selected = [run]
    else:
        selected = [run for run in history.values() if run['quest_id'] == query.quest_id and 'reply' not in run]
        if not selected: raise Conflict('Unknown quest run')
    if any('reply' in run for run in selected): raise Conflict('Quest already settled')
    for run in selected: run['cancelled'] = True
    cm.save('quest_runs', history)
    response = response_class()
    response.update_resource_result.CopyFrom(cm.update_resource_result())
    return make_response(response.SerializeToString())


@bp.post('/fail')
def fail(): return cancel(pb.RequestFail.FromString(request.data), pb.ResponseFail)


@bp.post('/retire')
def retire(): return cancel(pb.RequestRetire.FromString(request.data), pb.ResponseRetire)


@bp.post('/continue')
def continue_battle():
    query = pb.RequestContinue.FromString(request.data)
    _, run = run_for(query, 'battle')
    if 'reply' in run: raise Conflict('Quest already settled')
    response = pb.ResponseContinue()
    response.update_resource_result.CopyFrom(cm.update_resource_result())
    return make_response(response.SerializeToString())


@bp.post('/get_continue_crystal')
def get_continue_crystal(): return make_response(pb.ResponseGetContinueCrystal(continue_crystal_amount=0).SerializeToString())
