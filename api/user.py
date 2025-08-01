from flask import Blueprint, request, make_response
from proto import user_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/change_comment", methods=["POST"])
def user_change_comment():
    pbrq = pb.RequestChangeComment()
    pbrs = pb.ResponseChangeComment()
    pbrq.ParseFromString(request.data)
    cm.change_comment(pbrq.comment)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_emblem", methods=["POST"])
def user_change_emblem():
    pbrq = pb.RequestChangeEmblem()
    pbrs = pb.ResponseChangeEmblem()
    pbrq.ParseFromString(request.data)
    cm.change_emblem(pbrq.emblem_id)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_friend_unit", methods=["POST"])
def user_change_friend_unit():
    pbrq = pb.RequestChangeFriendUnit()
    pbrs = pb.ResponseChangeFriendUnit()
    pbrq.ParseFromString(request.data)
    cm.change_friend_unit(pbrq.unit_id)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_home_bg", methods=["POST"])
def user_change_home_bg():
    pbrq = pb.RequestChangeHomeBg()
    pbrs = pb.ResponseChangeHomeBg()
    pbrq.ParseFromString(request.data)
    cm.change_home_bg(pbrq.background_id)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_home_unit_main", methods=["POST"])
def user_change_home_unit_main():
    pbrq = pb.RequestChangeHomeUnitMain()
    pbrs = pb.ResponseChangeHomeUnitMain()
    pbrq.ParseFromString(request.data)
    cm.change_home_unit(pbrq.unit_id, 1)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_home_unit_sub", methods=["POST"])
def user_change_home_unit_sub():
    pbrq = pb.RequestChangeHomeUnitSub()
    pbrs = pb.ResponseChangeHomeUnitSub()
    pbrq.ParseFromString(request.data)
    cm.change_home_unit(pbrq.unit_id, 2)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_name", methods=["POST"])
def user_change_name():
    pbrq = pb.RequestChangeName()
    pbrs = pb.ResponseChangeName()
    pbrq.ParseFromString(request.data)
    cm.change_name(pbrq.name)
    jf.Parse(cm.read("t_user"), pbrs)
    return make_response(pbrs.SerializeToString())

@bp.route("/stamina_recover", methods=["POST"])
def user_stamina_recover():
    pbrs = pb.ResponseStaminaRecover()
    jf.Parse(cm.load_worker(), pbrs.t_user_worker)
    return make_response(pbrs.SerializeToString())

@bp.route("/get_stamina_recover", methods=["POST"])
def user_get_stamina_recover():
    return make_response('', 204)

@bp.route("/set_transfer_password", methods=["POST"])
def user_set_transfer_password():
    return make_response('', 204)
