from flask import Blueprint, request, make_response
from proto import spy_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm
import random

bp = Blueprint("spy", __name__, url_prefix="/spy")

chara = [311001001, 311002001, 311003001, 311004001,311005001, 311006001,
         311007001, 311008001, 311009005, 311010001, 312001001, 312002001,
         312003001, 312004001, 313001001, 313002001, 396006001, 394001001,
         394002001, 394003001, 394004001, 396001001, 396002001, 396003001,
         396004001, 396005001]

@bp.route("/get_list", methods=["POST"])
def spy_get_list():
    pbrs = pb.ResponseGetList()
    for i in range(5):
        pbrs.t_user_spy_list.add()
        pbrs.t_user_spy_list[i].user_spy_id = i+1
        pbrs.t_user_spy_list[i].spy_id = 1000001+i
        pbrs.t_user_spy_list[i].state = 0
        pbrs.t_user_spy_list[i].subscription_flag = 1
    
    pbrs.today_work.max_count = 100
    pbrs.today_work.current_count = 0

    pbrs.t_user_spy_list.add()
    pbrs.t_user_spy_list[-1].user_spy_id = 1001
    pbrs.t_user_spy_list[-1].spy_id = 1000001
    rand1, rand2 = random.sample(chara, 2)
    pbrs.t_user_spy_list[-1].unit_id = rand1
    pbrs.t_user_spy_list[-1].sub_unit_id = rand2
    pbrs.t_user_spy_list[-1].state = 1
    pbrs.t_user_spy_list[-1].start_time = 1
    pbrs.t_user_spy_list[-1].is_force_clear = 1
    pbrs.t_user_spy_list[-1].subscription_flag = 1

    pbrs.t_user_spy_playing_list.add()
    pbrs.t_user_spy_playing_list[-1].idx = 1
    pbrs.t_user_spy_playing_list[-1].user_spy_id = 1001
    pbrs.t_user_spy_playing_list[-1].is_lock = 0

    return make_response(pbrs.SerializeToString())

@bp.route("/clear", methods=["POST"])
def spy_clear():
    pbrs = pb.ResponseClear()
    pbrs.is_great_success = random.choice([True, False])
    pbrs.t_user_spy_list.add()
    pbrs.t_user_spy_list[0].user_spy_id = 1001
    pbrs.t_user_spy_list[0].spy_id = 1000001
    pbrs.t_user_spy_list[0].state = 2
    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())

@bp.route("/start", methods=["POST"])
def spy_start():
    return make_response('', 204)