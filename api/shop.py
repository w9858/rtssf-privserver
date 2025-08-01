from flask import Blueprint, request, make_response
from proto import shop_pb2 as pb
from google.protobuf import json_format as jf
from api import common as cm
import random

bp = Blueprint("shop", __name__, url_prefix="/shop")

ssr_chara = [311001001, 311001008, 311001009, 311001010, 311001013, 311001014, 311001015, 311001020,
             311002001, 311002008, 311002009, 311002010, 311002013, 311002014, 311002021, 311003001,
             311003012, 311003010, 311003013, 311003014, 311003017, 311003018, 311004001, 311004008,
             311004010, 311004012, 311004013, 311004014, 311004015, 311004016, 311004019, 311004018,
             311005001, 311005008, 311005009, 311005010, 311005012, 311005013, 311005018, 311006001,
             311006008, 311006011, 311006013, 311006012, 311006015, 311006014, 311006018, 311006019,
             311007001, 311007003, 311007005, 311007009, 311008001, 311008005, 311008009, 311009005,
             311009010, 311009013, 311010008, 311010001, 311010012, 311010009, 311010013, 311010014,
             312001001, 312001007, 312001008, 312002001, 312002007, 312002008, 312003001, 312004001,
             312003007, 312004007, 312004008, 312004011, 313001001, 313001006, 313002001, 313002005,
             396006001, 394001001, 394002001, 394003001, 394004001, 396001001, 396002001, 396003001,
             396004001, 396005001]

@bp.route("/list", methods=["POST"])
def shop_list():
    pbrs = pb.ResponseList()
    pbrs.shop_list.add()
    pbrs.shop_list[-1].shop_id = 1
    pbrs.shop_list[-1].name = "極スパイス"
    pbrs.shop_list[-1].balloon_msg = "Main"
    pbrs.shop_list[-1].point_resource_type = 6
    pbrs.shop_list[-1].button_type = 0
    
    pbrs.shop_list.add()
    pbrs.shop_list[-1].shop_id = random.choice(ssr_chara)
    pbrs.shop_list[-1].name = "コイン"
    pbrs.shop_list[-1].balloon_msg = str(pbrs.shop_list[-1].shop_id)
    pbrs.shop_list[-1].point_resource_type = 4
    pbrs.shop_list[-1].button_type = 1
    
    pbrs.shop_list.add()
    pbrs.shop_list[-1].shop_id = random.choice(ssr_chara)
    pbrs.shop_list[-1].name = "フレンドポイント"
    pbrs.shop_list[-1].balloon_msg = str(pbrs.shop_list[-1].shop_id)
    pbrs.shop_list[-1].point_resource_type = 9
    pbrs.shop_list[-1].button_type = 2
    
    pbrs.shop_list.add()
    pbrs.shop_list[-1].shop_id = random.choice(ssr_chara)
    pbrs.shop_list[-1].name = "ブーツ"
    pbrs.shop_list[-1].balloon_msg = str(pbrs.shop_list[-1].shop_id)
    pbrs.shop_list[-1].point_resource_type = 5
    pbrs.shop_list[-1].button_type = 3

    return make_response(pbrs.SerializeToString())

@bp.route("/item_list", methods=["POST"])
def shop_item_list():
    pbrs = pb.ResponseItemList()
    pbrq = pb.RequestItemList()
    pbrq.ParseFromString(request.data)
    pbrs.point = 0
    if(pbrq.shop_id == 1):
        pbrs.shop_unit_id = 311009003
        pbrs.point = 10000
    else: pbrs.shop_unit_id = pbrq.shop_id

    return make_response(pbrs.SerializeToString())
