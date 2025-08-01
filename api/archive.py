from flask import Blueprint, request, make_response
from proto import archive_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("archive", __name__, url_prefix="/archive")

@bp.route("/read", methods=["POST"])
def archive_read():
    pbrq = pb.RequestRead()
    pbrs = pb.ResponseRead()
    pbrq.ParseFromString(request.data)
    cm.adv_clear(pbrq.quest_id)
    jf.Parse(cm.read("t_user_archive_list"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/release", methods=["POST"])
def archive_release():
    pbrq = pb.RequestRelease()
    pbrs = pb.ResponseRelease()
    pbrq.ParseFromString(request.data)
    cm.adv_clear(pbrq.quest_id)
    jf.Parse(cm.read("t_user_archive_list"), pbrs)
    pbrs.update_resource_result.MergeFrom(cm.update_resource_result())
    return make_response(pbrs.SerializeToString())
