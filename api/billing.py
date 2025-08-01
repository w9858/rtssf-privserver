from flask import Blueprint, request, make_response
from proto import billing_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("billing", __name__, url_prefix="/billing")

@bp.route("/top", methods=["POST"])
def billing_top():
    pbrs = pb.ResponseTop()
    pbrs.registered_birthday = 1
    return make_response(pbrs.SerializeToString())
