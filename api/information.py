from flask import Blueprint, request, make_response
from proto import information_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm
import random

bp = Blueprint("information", __name__, url_prefix="/information")

@bp.route("/index", methods=["POST"])
def information_index():
    pbrs = pb.ResponseIndex()
    chara_name = random.choice(["byakko","dolte","fu","goe","hatsume","kamari","katrina","lappa","mei","momo","monomi","theresia","yuki"])

    pbrs.m_information_tab_list.add()
    pbrs.m_information_tab_list[0].tab_id = 1
    pbrs.m_information_tab_list[0].name = "Information"
    pbrs.m_information_tab_list[0].order = 1

    pbrs.m_information_list.add()
    pbrs.m_information_list[-1].information_id = 1
    pbrs.m_information_list[-1].tab_id = 1
    pbrs.m_information_list[-1].title = "Contact"
    pbrs.m_information_list[-1].contents = "<color=#00acee>Twitter</color> : @w9858__  (two underbar)\n\n<color=#ea4335>Email</color> : w9858@proton.me\n\n"+\
    "<color=#6e5494>GitHub</color> : https://github.com/w9858\n<img>https://w9858.pages.dev/220206/character/img/chara_"+chara_name+"_face.png</img>"
    pbrs.m_information_list[-1].view_android = 1
    pbrs.m_information_list[-1].pin_flag = 1

    pbrs.m_information_list.add()
    pbrs.m_information_list[-1].information_id = 2
    pbrs.m_information_list[-1].tab_id = 1
    pbrs.m_information_list[-1].title = "Features that dosen't work"
    pbrs.m_information_list[-1].contents = """
    Base

        Crafting weapons, items (Recipe isn't available)
        Spy expedition
        Always maximum friendly point (Lv10)
        Shop & Exchange

    Achievement & Present

    Battle result

        It returns wrong rewards
        Recipe isn't available
        Stamina & Items will not consume

    Stamina setted max
    Stamina valued 5000 but system shows under level limit
    Items are moderately preloaded

    Spy Units

    Fixed values at all (max lv, max board)
    """
    pbrs.m_information_list[-1].view_android = 1
    pbrs.m_information_list[-1].pin_flag = 2

    pbrs.t_user_information_list.add()
    pbrs.t_user_information_list[-1].information_id = 1
    pbrs.t_user_information_list.add()
    pbrs.t_user_information_list[-1].information_id = 2

    return make_response(pbrs.SerializeToString())

@bp.route("/read", methods=["POST"])
def information_read():
    return make_response('', 204)