from flask import Blueprint, request, make_response
from proto import regist_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("regist", __name__, url_prefix="/regist")

@bp.route("/check", methods=["POST"])
def regist_check():
    pbrs = pb.ResponseCheck()
    pbrs.is_register = True
    pbrs.is_review = False
    pbrs.master_check_user = 0
    pbrs.sqlite_ver = 99

    return make_response(pbrs.SerializeToString())
