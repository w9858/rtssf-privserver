from flask import Blueprint, request, make_response
from proto import weapon_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("weapon", __name__, url_prefix="/weapon")

@bp.route("/equip", methods=["POST"])
def weapon_equip():
    pbrq = pb.RequestEquip()
    pbrs = pb.ResponseEquip()
    pbrq.ParseFromString(request.data)
    cm.weapon_equip(pbrq.unit_id, pbrq.user_weapon_id)
    jf.Parse(cm.read("t_user_unit_weapon_list"), pbrs)
    if(pbrq.user_weapon_id == 0):
        pbrs.deleted_list.add()
        pbrs.deleted_list[0].user_id = 0
        pbrs.deleted_list[0].unit_id = pbrq.unit_id
        pbrs.deleted_list[0].user_weapon_id = 0
    return make_response(pbrs.SerializeToString())

@bp.route("/lock", methods=["POST"])
def weapon_lock():
    pbrq = pb.RequestLock.FromString(request.data)
    if pbrq.flag not in (0, 1):
        from werkzeug.exceptions import BadRequest
        raise BadRequest('Lock flag must be 0 or 1')
    data = cm.document('t_user_weapon_list')
    ids = {weapon.user_weapon_id for weapon in pbrq.weapon_list}
    for value in ids: cm.owned('t_user_weapon_list', 'user_weapon_id', value)
    for row in data['t_user_weapon_list']:
        if row['user_weapon_id'] in ids: row['lock_flag'] = pbrq.flag
    cm.save('t_user_weapon_list', data)
    return jf.ParseDict(data, pb.ResponseLock()).SerializeToString()

@bp.route("/sell", methods=["POST"])
def weapon_sell():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')
