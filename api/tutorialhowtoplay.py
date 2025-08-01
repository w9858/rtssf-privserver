from flask import Blueprint, request, make_response
from proto import tutorialhowtoplay_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("tutorialhowtoplay", __name__, url_prefix="/tutorialhowtoplay")

@bp.route("/save", methods=["POST"])
def tutorialhowtoplay_save():
    pbrs = pb.ResponseSave()
    pbrs.t_user_tutorial_how_to_play_list = [9901,9902,9903,9904,9905,
                                             9906,9907,9908,9909,9910,
                                             9911,9912,9913,9914,9915]
    return make_response(pbrs.SerializeToString())