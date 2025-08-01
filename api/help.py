from flask import Blueprint, request, make_response
from proto import help_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("help", __name__, url_prefix="/help")

@bp.route("/list", methods=["POST"])
def help_list():
    pbrs = pb.ResponseList()
    pbrs.m_help_list.add()
    pbrs.m_help_list[-1].id = 1
    pbrs.m_help_list[-1].category = 1
    pbrs.m_help_list[-1].order = 1
    pbrs.m_help_list[-1].title = "Styles"
    pbrs.m_help_list[-1].contents = "<img>1</img>\n   <color=#d6083b>紅蓮</color>, <color=#005198>靑藍</color>, <color=#191c1f>黑鉄</color>, "+\
    "<color=#b83d96>紫電</color>, <color=#5cc151>翡翠</color>, <color=#ffcc00>琥珀</color>"

    pbrs.m_help_list.add()
    pbrs.m_help_list[-1].id = 2
    pbrs.m_help_list[-1].category = 1
    pbrs.m_help_list[-1].order = 2
    pbrs.m_help_list[-1].title = "Contact"
    pbrs.m_help_list[-1].contents = """\n
    <color=#00acee>Twitter</color> : @w9858__  (two underbar)\n
    <color=#ea4335>Email</color> : w9858@proto.me\n
    <color=#6e5494>GitHub</color> : https://github.com/w9858
    """

    pbrs.m_help_list.add()
    pbrs.m_help_list[-1].id = 3
    pbrs.m_help_list[-1].category = 1
    pbrs.m_help_list[-1].order = 3
    pbrs.m_help_list[-1].title = "Website Backups"
    pbrs.m_help_list[-1].contents = """RELEFRA Game site backup

    https://w9858.pages.dev/

RELEASE THE SPYCE (Anime) old site backups

    https://w9858.pages.dev/220206/
    https://w9858.pages.dev/180129/
    https://w9858.pages.dev/180325/

The anime site is still alive at releasethespyce.com"""

    pbrs.m_help_list.add()
    pbrs.m_help_list[-1].id = 4
    pbrs.m_help_list[-1].category = 1
    pbrs.m_help_list[-1].order = 4
    pbrs.m_help_list[-1].title = "some old asset"
    pbrs.m_help_list[-1].contents = "<img>2</img>"

    pbrs.m_help_category_list.add()
    pbrs.m_help_category_list[0].category = 1
    pbrs.m_help_category_list[0].order = 1
    pbrs.m_help_category_list[0].name = "Help"

    return make_response(pbrs.SerializeToString())
