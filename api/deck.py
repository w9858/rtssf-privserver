from flask import Blueprint, request, make_response
from proto import deck_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm

bp = Blueprint("deck", __name__, url_prefix="/deck")

@bp.route("/save", methods=["POST"])
def deck_save():
    pbrq = pb.RequestSave()
    pbrs = pb.ResponseSave()
    pbrq.ParseFromString(request.data)
    cm.deck_save(pbrq.t_user_deck)
    jf.Parse(cm.deck_load_one(pbrq.t_user_deck.deck_no),pbrs.t_user_deck)
    return make_response(pbrs.SerializeToString())

@bp.route("/change_name", methods=["POST"])
def deck_change_name():
    pbrq = pb.RequestChangeName()
    pbrs = pb.ResponseChangeName()
    pbrq.ParseFromString(request.data)
    cm.deck_change_name(pbrq.name, pbrq.deck_no)
    jf.Parse(cm.deck_load_one(pbrq.deck_no),pbrs.t_user_deck)
    return make_response(pbrs.SerializeToString())
