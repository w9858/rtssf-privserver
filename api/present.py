from flask import Blueprint, request, make_response
from proto import present_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("present", __name__, url_prefix="/present")

@bp.route("/get_list", methods=["POST"])
def present_get_list():
    return make_response('', 204)

@bp.route("/get_received_list", methods=["POST"])
def present_get_received_list():
    return make_response('', 204)

@bp.route("/receive", methods=["POST"])
def present_receive():
    return make_response('', 204)

@bp.route("/receive_all", methods=["POST"])
def present_receive_all():
    return make_response('', 204)
