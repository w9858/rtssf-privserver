from flask import Blueprint, request, make_response
from proto import mypage_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm
from datetime import datetime

bp = Blueprint("mypage", __name__, url_prefix="/mypage")

had_loginbonus = False

birthday = {
    (6, 29): [11001],(12, 14): [11002],
    (11, 22): [11003, 11004],
    (4, 2):  [11005], (8, 24): [11006],
    (9, 1):  [11007, 11008],
    (12, 21): [11009], (5, 28): [11010],
    (7, 26): [12001], (10, 6): [12002],
    (7, 14): [12003], (8, 10): [12004],
    (2, 23): [13001] #, (4, 22): [13002] ## nodata
}


@bp.route("/index", methods=["POST"])
def mypage_index():
    global had_loginbonus
    today = datetime.now()

    pbrs = pb.ResponseIndex()
    jf.Parse(cm.read("t_user"), pbrs)
    jf.Parse(cm.read("t_user_tips_list"), pbrs)
    jf.Parse(cm.read("t_user_crystal"), pbrs)
    jf.Parse(cm.read("t_user_count_list"), pbrs)
    
    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[0].banner_img = "Banner/1.png"
    pbrs.m_app_banner_list[0].order = 1
    pbrs.m_app_banner_list[0].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[0].end_at = "2038-01-01 23:59:59"
    pbrs.m_app_banner_list[0].transition_id = 14
    
    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[1].banner_img = "Banner/2.png"
    pbrs.m_app_banner_list[1].order = 2
    pbrs.m_app_banner_list[1].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[1].end_at = "2038-01-01 23:59:59"
    pbrs.m_app_banner_list[1].transition_id = 13

    pbrs.m_app_banner_list.add()
    pbrs.m_app_banner_list[2].banner_img = "Banner/3.png"
    pbrs.m_app_banner_list[2].order = 3
    pbrs.m_app_banner_list[2].start_at = "2019-01-03 20:02:44"
    pbrs.m_app_banner_list[2].end_at = "2038-01-01 23:59:59"

    if not had_loginbonus:
        had_loginbonus = True
        day_key = (today.month, today.day)

        if day_key in birthday:
            ids = birthday[day_key]
            for person_id in ids:
                birthday_bonus = pbrs.t_user_login_bonus_list.add()
                birthday_bonus.login_bonus_id = person_id * 100 + 40000001

        daily_logbo = pbrs.t_user_login_bonus_list.add()
        daily_logbo.login_bonus_id = 10000001
        daily_logbo.sheet_id = 1
        daily_logbo.day = today.weekday()

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
