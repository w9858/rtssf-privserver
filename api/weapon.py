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
    print("\n"+str(pbrq))
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
    return make_response('', 204)

@bp.route("/sell", methods=["POST"])
def weapon_sell():
    return make_response('', 204)
