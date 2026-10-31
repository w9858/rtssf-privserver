from flask import Blueprint, request, make_response
from proto import present_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("present", __name__, url_prefix="/present")

@bp.route("/get_list", methods=["POST"])
def present_get_list():
    return make_response(pb.ResponseGetList().SerializeToString())

@bp.route("/get_received_list", methods=["POST"])
def present_get_received_list():
    return make_response(pb.ResponseGetReceivedList().SerializeToString())

@bp.route("/receive", methods=["POST"])
def present_receive():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')

@bp.route("/receive_all", methods=["POST"])
def present_receive_all():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')
