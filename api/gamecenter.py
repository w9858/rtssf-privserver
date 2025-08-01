from flask import Blueprint, request, make_response
from proto import gamecenter_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("gamecenter", __name__, url_prefix="/gamecenter")

@bp.route("/get_list", methods=["POST"])
def gamecenter_get_list():
    return make_response('', 204)
