from flask import Blueprint, request, make_response
from proto import achievement_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("achievement", __name__, url_prefix="/achievement")

@bp.route("/get_list", methods=["POST"])
def achievement_get_list():
    result = pb.ResponseGetList()
    for key in ('t_user_achievement_list', 't_user_achievement_daily_list', 't_user_achievement_weekly_list'):
        data = cm.document(key)
        data[key] = [row for row in data[key] if row['achievement_id'] > 0]
        jf.ParseDict(data, result)
    return make_response(result.SerializeToString())

@bp.route("/receive", methods=["POST"])
def achievement_receive():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')

@bp.route("/receive_all", methods=["POST"])
def achievement_receive_all():
    from werkzeug.exceptions import NotImplemented
    raise NotImplemented('This operation requires unavailable game master data or account services')
