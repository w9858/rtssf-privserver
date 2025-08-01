from flask import Blueprint, request, make_response
from proto import eventmap_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("eventmap", __name__, url_prefix="/eventmap")

@bp.route("/get", methods=["POST"])
def eventmap_get():
    pbrq = pb.RequestGet()
    pbrs = pb.ResponseGet()
    pbrq.ParseFromString(request.data)
    pbrs.t_user_event.event_id = pbrq.event_id
    pbrs.t_user_event.point = 10000000
    pbrs.t_user_event.max_point = 10000000
    pbrs.is_first_access = False
    pbrs.exists_new_clear_event_achievement = False
    pbrs.current_rank = 1
    jf.Parse(cm.read("t_user_quest_list"), pbrs)
    return make_response(pbrs.SerializeToString())
