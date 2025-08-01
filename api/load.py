from flask import Blueprint, request, make_response
from proto import load_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("load", __name__, url_prefix="/load")

@bp.route("/split", methods=["POST"])
def load_split():
    pbrq = pb.RequestSplit()
    pbrs = pb.ResponseSplit()
    pbrq.ParseFromString(request.data)
    #pbrq.section

    parse_functions = [
        "t_user",
        "t_user_crystal",
        "t_user_unit_list",
        "t_user_worker_list",
        "t_user_quest_list",
        # "t_user_quest_status",
        "t_user_archive_list",
        "t_user_count_list",
        "t_user_unit_weapon_list",
        "t_user_weapon_list",
        "t_user_weapon_skill_list",
        "t_user_weapon_status_list",
        # "t_user_recipe_list",
        # "t_user_board_list",
        "t_user_tips_list",
        "t_user_tutorial_how_to_play_list",
        "t_user_deck_list",
        "t_user_item_list",
        "t_user_character_friendly_list",
        "t_user_spy_list",
        "t_user_spy_playing_list",
        "t_user_subscription_list",
        "t_user_background_list",
        "t_user_emblem_list",
        "t_user_board_list",
    ]

    pbrs.current_section = pbrq.section
    pbrs.max_section = len(parse_functions)

    if 1 <= pbrq.section <= len(parse_functions):
        table_name = parse_functions[pbrq.section - 1]
        # print(f"Section {pbrq.section} / {pbrs.max_section} - {table_name}")
        jf.Parse(cm.read(table_name), pbrs)
    
    return make_response(pbrs.SerializeToString())

@bp.route("/sqlite_versions", methods=["POST"])
def load_sqlite_versions():
    pbrs = pb.ResponseSqliteVersions()
    pbrs.version_list.extend(["0", "81", "99"])
    return make_response(pbrs.SerializeToString())
