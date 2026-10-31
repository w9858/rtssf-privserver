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
    cm.owned('t_user_unit_list', 'unit_id', pbrq.unit_id)
    if pbrq.sheet_no <= 0:
        from werkzeug.exceptions import BadRequest
        raise BadRequest('Sheet number must be positive')
    pbrs.t_user_board.unit_id = pbrq.unit_id
    pbrs.t_user_board.progress_1 = 2147483647
    pbrs.t_user_board.progress_2 = 2147483647
    pbrs.t_user_board.sheet_no = pbrq.sheet_no
    for i in range(4):
        pbrs.t_user_board.square_status_list.add()
        pbrs.t_user_board.square_status_list[i].is_release = True
        pbrs.t_user_board.square_status_list[i].square_id = i
    data = cm.document('t_user_board_list')
    data['t_user_board_list'] = [row for row in data['t_user_board_list']
        if (row['unit_id'], row['sheet_no']) != (pbrq.unit_id, pbrq.sheet_no)]
    data['t_user_board_list'].append(jf.MessageToDict(pbrs.t_user_board, preserving_proto_field_name=True))
    cm.save('t_user_board_list', data)
    jf.Parse(cm.read("t_user_item_list"), pbrs)
    jf.Parse(cm.read("t_user"), pbrs)
    jf.Parse(cm.read("t_user_archive_list"), pbrs)
    return make_response(pbrs.SerializeToString())
