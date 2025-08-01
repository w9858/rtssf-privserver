from flask import Blueprint, request, make_response
from proto import item_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("item", __name__, url_prefix="/item")

@bp.route("/sell", methods=["POST"])
def item_sell():
    return make_response('', 204)

@bp.route("/stamina_recover", methods=["POST"])
def item_stamina_recover():
    pbrs = pb.ResponseStaminaRecover()
    jf.Parse(cm.read("t_user_item_list"), pbrs)
    jf.Parse(cm.load_worker(), pbrs.t_user_worker)
    return make_response(pbrs.SerializeToString())
