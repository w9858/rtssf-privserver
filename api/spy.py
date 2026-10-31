"""Persistent sandbox expeditions; no official expedition/reward master data."""
import time
from flask import Blueprint, current_app, request
from google.protobuf import json_format as jf
from werkzeug.exceptions import BadRequest, Conflict
from proto import spy_pb2 as pb
from api import common as cm

bp = Blueprint('spy', __name__, url_prefix='/spy')


def data():
    value = cm.document('t_user_spy_list')
    rows = value['t_user_spy_list']
    for number in range(1, 6):
        if not any(row['user_spy_id'] == number for row in rows):
            rows.append(dict(user_spy_id=number, spy_id=1000000 + number, state=0, subscription_flag=1))
    return value


def response(cls, value):
    result = jf.ParseDict(value, cls())
    jf.Parse(cm.read('t_user_spy_playing_list'), result)
    if hasattr(result, 'today_work'):
        result.today_work.max_count = 100
    return result


def row_for(value, number):
    row = next((row for row in value['t_user_spy_list'] if row['user_spy_id'] == number), None)
    if row is None: raise BadRequest('Unknown expedition slot')
    return row


@bp.post('/get_list')
def get_list():
    value = data()
    cm.save('t_user_spy_list', value)
    return response(pb.ResponseGetList, value).SerializeToString()


@bp.post('/start')
def start():
    query = pb.RequestStart.FromString(request.data)
    value = data()
    row = row_for(value, query.user_spy_id)
    if row['state'] == 1: raise Conflict('Expedition is already running')
    cm.owned('t_user_unit_list', 'unit_id', query.unit_id)
    if query.sub_unit_id:
        cm.owned('t_user_unit_list', 'unit_id', query.sub_unit_id)
        if query.unit_id == query.sub_unit_id: raise BadRequest('Expedition units must differ')
    selected = {query.unit_id, query.sub_unit_id} - {0}
    for other in value['t_user_spy_list']:
        if other['state'] == 1 and selected.intersection({other.get('unit_id'), other.get('sub_unit_id')}):
            raise Conflict('Unit is already on an expedition')
    row.update(unit_id=query.unit_id, sub_unit_id=query.sub_unit_id, state=1,
               start_time=int(time.time()), is_force_clear=0)
    cm.save('t_user_spy_list', value)
    return response(pb.ResponseStart, value).SerializeToString()


@bp.post('/clear')
def clear():
    query = pb.RequestClear.FromString(request.data)
    value = data()
    row = row_for(value, query.user_spy_id)
    if row['state'] != 1: raise Conflict('Expedition is not running')
    if int(time.time()) < row['start_time'] + current_app.config['SPY_DURATION_SECONDS']:
        raise Conflict('Expedition is not finished')
    row['state'] = 2
    cm.save('t_user_spy_list', value)
    result = response(pb.ResponseClear, value)
    result.update_resource_result.CopyFrom(cm.update_resource_result())
    return result.SerializeToString()


@bp.post('/stop')
def stop():
    query = pb.RequestStop.FromString(request.data)
    value = data()
    row = row_for(value, query.user_spy_id)
    if row['state'] != 1: raise Conflict('Expedition is not running')
    row.update(state=0, unit_id=0, sub_unit_id=0, start_time=0)
    cm.save('t_user_spy_list', value)
    return response(pb.ResponseStop, value).SerializeToString()
