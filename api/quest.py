from flask import Blueprint, request, make_response
from proto import quest_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm
import random

bp = Blueprint("quest", __name__, url_prefix="/quest")

@bp.route("/start_adv", methods=["POST"])
def quest_start_adv():
    pbrq = pb.RequestStartAdv()
    pbrs = pb.ResponseStartAdv()
    pbrq.ParseFromString(request.data)
    pbrs.token = "token"
    return make_response(pbrs.SerializeToString())

@bp.route("/clear_adv", methods=["POST"])
def quest_clear_adv():
    pbrq = pb.RequestClearAdv()
    pbrs = pb.ResponseClearAdv()
    pbrq.ParseFromString(request.data)
    pbrs.t_user_quest.quest_id = pbrq.quest_id
    pbrs.t_user_quest.clear_count = 1
    pbrs.t_user_quest_status.quest_id = pbrq.quest_id
    pbrs.t_user_quest_status.token = "token"
    pbrs.t_user_quest_status.start_at = "2020-03-31 15:00:00"
    pbrs.t_user_quest_status.end_at = "2020-03-31 15:00:00"
    cm.adv_clear(pbrq.quest_id)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/start", methods=["POST"])
def quest_start():
    pbrq = pb.RequestStart()
    pbrs = pb.ResponseStart()
    pbrq.ParseFromString(request.data)
    pbrs.token = "token"
    return make_response(pbrs.SerializeToString())

@bp.route("/clear", methods=["POST"])
def quest_clear():
    pbrq = pb.RequestClear()
    pbrs = pb.ResponseClear()
    pbrq.ParseFromString(request.data)
    pbrs.is_friend = True
    pbrs.is_unlock_spy_frame = False
    pbrs.t_user_quest.quest_id = pbrq.quest_id
    pbrs.t_user_quest.clear_count = 1
    pbrs.t_user_quest_status.quest_id = pbrq.quest_id
    pbrs.t_user_quest.quest_mission_id_1 = pbrq.is_clear_mission_1
    pbrs.t_user_quest.quest_mission_id_2 = pbrq.is_clear_mission_2
    pbrs.t_user_quest.quest_mission_id_3 = pbrq.is_clear_mission_3
    pbrs.t_user_quest_status.token = "token"
    pbrs.t_user_quest_status.start_at = "2019-02-12 15:00:00"
    pbrs.t_user_quest_status.end_at = "2019-02-12 15:00:00"
    pbrs.t_user_quest.rank = 0
    pbrs.drop_list.add()
    pbrs.drop_list[0].resource_type = 1
    pbrs.drop_list[0].resource_id = 101070101
    pbrs.drop_list[0].resource_value_id = 1
    pbrs.drop_list[0].amount = 5
    pbrs.drop_list.add()
    pbrs.drop_list[1].resource_type = 1
    pbrs.drop_list[1].resource_id = 101070201
    pbrs.drop_list[1].resource_value_id = 1
    pbrs.drop_list[1].amount = 5
    pbrs.drop_list.add()
    pbrs.drop_list[2].resource_type = 1
    pbrs.drop_list[2].resource_id = 101070301
    pbrs.drop_list[2].resource_value_id = 1
    pbrs.drop_list[2].amount = 5
    pbrs.drop_list.add()
    pbrs.drop_list[3].resource_type = 1
    pbrs.drop_list[3].resource_id = 101070401
    pbrs.drop_list[3].resource_value_id = 1
    pbrs.drop_list[3].amount = 5
    pbrs.mission_complete_reward_list.add()
    pbrs.mission_complete_reward_list[0].resource_type = 1
    pbrs.mission_complete_reward_list[0].resource_id = 190101001
    pbrs.mission_complete_reward_list[0].resource_value_id = 1
    pbrs.mission_complete_reward_list[0].amount = 1
    jf.Parse(cm.read("t_user_character_friendly_list"), pbrs)
    jf.Parse(cm.read("t_user_archive_list"), pbrs)

    cm.add_user_exp(180)
    cm.add_user_friend_point(1)
    cm.add_user_gold(random.choice([8000, 5000, 12000, 2500]))

    cm.quest_clear(pbrq.quest_id,pbrq.is_clear_mission_1,pbrq.is_clear_mission_2,pbrq.is_clear_mission_3)

    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())

@bp.route("/fail", methods=["POST"])
def quest_fail():
    pbrs = pb.ResponseFail()
    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())

@bp.route("/retire", methods=["POST"])
def quest_retire():
    pbrs = pb.ResponseRetire()
    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())

@bp.route("/continue", methods=["POST"])
def quest_continue():
    pbrs = pb.ResponseContinue()
    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())

@bp.route("/get_continue_crystal", methods=["POST"])
def quest_get_continue_crystal():
    return make_response('', 204)
