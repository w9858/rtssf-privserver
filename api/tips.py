from flask import Blueprint, request
from google.protobuf import json_format as jf
from werkzeug.exceptions import BadRequest
from proto import tips_pb2 as pb
from api import common as cm

bp = Blueprint('tips', __name__, url_prefix='/tips')

@bp.post('/save')
def save():
    query = pb.RequestSave.FromString(request.data)
    if any(value <= 0 for value in query.tips_id_list): raise BadRequest('Tips IDs must be positive')
    data = cm.document('t_user_tips_list')
    ids = {row['tips_id'] for row in data['t_user_tips_list']}
    data['t_user_tips_list'].extend({'tips_id': value} for value in sorted(set(query.tips_id_list) - ids))
    cm.save('t_user_tips_list', data)
    return jf.ParseDict(data, pb.ResponseSave()).SerializeToString()
