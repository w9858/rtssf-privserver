from flask import Blueprint, request, make_response
from proto import board_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("board", __name__, url_prefix="/board")

@bp.route("/release", methods=["POST"])
def board_release():
    pbrq = pb.RequestRelease()
    pbrs = pb.ResponseRelease()
    pbrq.ParseFromString(request.data)
    pbrs.t_user_board.unit_id = pbrq.unit_id
    pbrs.t_user_board.progress_1 = 2147483647
    pbrs.t_user_board.progress_2 = 2147483647
    pbrs.t_user_board.sheet_no = pbrq.sheet_no
    for i in range(4):
        pbrs.t_user_board.square_status_list.add()
        pbrs.t_user_board.square_status_list[i].is_release = True
        pbrs.t_user_board.square_status_list[i].square_id = i
    jf.Parse(cm.read("t_user_item_list"), pbrs)
    jf.Parse(cm.read("t_user"), pbrs)
    jf.Parse(cm.read("t_user_archive_list"), pbrs)
    return make_response(pbrs.SerializeToString())
