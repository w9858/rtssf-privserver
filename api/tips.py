from flask import Blueprint, request, make_response
from proto import tips_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("tips", __name__, url_prefix="/tips")

@bp.route("/save", methods=["POST"])
def tips_save():
    pbrs = pb.ResponseSave()
    pbrs.t_user_tips_list = [1001,1002,1003,1004,1005,1006,1007,1008,1009,
                             1010,1011,1012,1013,1014,1015,1016,1017,1018,
                             1019,1020,1021,1022,1023,1024,1025,1026,1027]
    return make_response(pbrs.SerializeToString())
