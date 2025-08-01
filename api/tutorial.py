from flask import Blueprint, request, make_response
from proto import tutorial_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("tutorial", __name__, url_prefix="/tutorial")

@bp.route("/adv_start", methods=["POST"])
def tutorial_adv_start():
    pbrs = pb.ResponseAdvStart()
    pbrs.script_file = "2001000017" # script file name
    return make_response(pbrs.SerializeToString())

@bp.route("/adv_clear", methods=["POST"])
def tutorial_adv_clear():
    return make_response('', 204)

@bp.route("/update_progress", methods=["POST"])
def tutorial_update_progress():
    pbrs = pb.ResponseUpdateProgress()
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/register_name", methods=["POST"])
def tutorial_register_name():
    pbrs = pb.ResponseRegisterName()
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())
