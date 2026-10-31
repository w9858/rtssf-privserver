from flask import Blueprint, request
from google.protobuf import json_format as jf
from werkzeug.exceptions import BadRequest
from proto import tutorialhowtoplay_pb2 as pb
from api import common as cm

bp = Blueprint('tutorialhowtoplay', __name__, url_prefix='/tutorialhowtoplay')

@bp.post('/save')
def save():
    query = pb.RequestSave.FromString(request.data)
    if query.tutorial_type <= 0: raise BadRequest('Tutorial type must be positive')
    key = 't_user_tutorial_how_to_play_list'
    data = cm.document(key)
    if not any(row['tutorial_type'] == query.tutorial_type for row in data[key]):
        data[key].append({'tutorial_type': query.tutorial_type})
    cm.save(key, data)
    return jf.ParseDict(data, pb.ResponseSave()).SerializeToString()
