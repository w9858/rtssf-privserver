from flask import Blueprint, request, make_response
from proto import unit_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("unit", __name__, url_prefix="/unit")

@bp.route("/evolve", methods=["POST"])
def unit_evolve():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')

@bp.route("/level_up", methods=["POST"])
def unit_level_up():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')
