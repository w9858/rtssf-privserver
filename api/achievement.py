from flask import Blueprint, request, make_response
from proto import achievement_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("achievement", __name__, url_prefix="/achievement")

@bp.route("/get_list", methods=["POST"])
def achievement_get_list():
    return make_response('', 204)

@bp.route("/receive", methods=["POST"])
def achievement_receive():
    return make_response('', 204)

@bp.route("/receive_all", methods=["POST"])
def achievement_receive_all():
    return make_response('', 204)
