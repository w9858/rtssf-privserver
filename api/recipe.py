from flask import Blueprint, request, make_response
from proto import recipe_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("recipe", __name__, url_prefix="/recipe")

@bp.route("/create", methods=["POST"])
def recipe_create():
    return make_response('', 204)
    # pbrq = pb.RequestCreate()
    # pbrs = pb.ResponseCreate()
    # pbrq.ParseFromString(request.body)
    # pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    # return make_response(pbrs.SerializeToString())
