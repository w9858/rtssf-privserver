from flask import Blueprint, request, make_response
from proto import mypage_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("mypage", __name__, url_prefix="/mypage")

@bp.route("/index", methods=["POST"])
def mypage_index():
    pbrs = pb.ResponseIndex()
    jf.Parse(cm.read("t_user"), pbrs)
    jf.Parse(cm.read("t_user_tips_list"), pbrs)
    jf.Parse(cm.read("t_user_crystal"), pbrs)
    jf.Parse(cm.read("t_user_count_list"), pbrs)
    
    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[0].banner_img = "Banner/1.png"
    pbrs.m_app_banner_list[0].order = 0
    pbrs.m_app_banner_list[0].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[0].end_at = "2033-05-03 20:02:44"
    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[1].banner_img = "Banner/2.png"
    pbrs.m_app_banner_list[1].order = 0
    pbrs.m_app_banner_list[1].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[1].end_at = "2033-05-03 20:02:44"
    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[2].banner_img = "Banner/3.png"
    pbrs.m_app_banner_list[2].order = 0
    pbrs.m_app_banner_list[2].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[2].end_at = "2033-05-03 20:02:44"

    #pbrs.t_user_login_bonus_list.add()
    #pbrs.t_user_login_bonus_list[-1].login_bonus_id = 41300201
    #pbrs.t_user_login_bonus_list[-1].day = 0

    ## daily login bonus  10000001
    ## comeback bonus  50000001
    ## shin sama 4[11010]01

    # pbrs.m_ad_list.add()
    # pbrs.m_ad_list[0].ad_type = 1
    # pbrs.m_ad_list[0].target_id = 3010001
    # pbrs.m_ad_list[0].fade_pattern = 1
    # pbrs.m_ad_list[0].particle_pattern = 2

    pbrs.exists_new_clear_achievement = 0
    pbrs.shop_new_item_flag = 0
    pbrs.exists_friend_invited = 0
    pbrs.no_read_information_count = 0
    pbrs.present_count = 0

    return make_response(pbrs.SerializeToString())
