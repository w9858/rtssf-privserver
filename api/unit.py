from flask import Blueprint, request, make_response
from proto import unit_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("unit", __name__, url_prefix="/unit")

@bp.route("/evolve", methods=["POST"])
def unit_evolve():
    return make_response('', 204)

@bp.route("/level_up", methods=["POST"])
def unit_level_up():
    return make_response('', 204)
