from flask import Blueprint, g

from .achievement import bp as achievement
from .archive import bp as archive
from .billing import bp as billing
from .board import bp as board
from .deck import bp as deck
from .eventmap import bp as eventmap
from .exchange import bp as exchange
from .friend import bp as friend
from .gacha import bp as gacha
from .gamecenter import bp as gamecenter
from .help import bp as help
from .information import bp as information
from .item import bp as item
from .load import bp as load
from .mypage import bp as mypage
from .present import bp as present
from .quest import bp as quest
from .recipe import bp as recipe
from .regist import bp as regist
from .shop import bp as shop
from .spy import bp as spy
from .tips import bp as tips
from .tutorial import bp as tutorial
from .tutorialhowtoplay import bp as tutorialhowtoplay
from .unit import bp as unit
from .user import bp as user
from .weapon import bp as weapon

api = Blueprint('api', __name__)

@api.before_request
def api_marking():
    g.is_api = True

bp_list = [achievement, archive, billing, board, deck, eventmap, exchange,
           friend, gacha, gamecenter, help, information, item, load, mypage,
           present, quest, recipe, regist, shop, spy, tips, tutorial, tutorialhowtoplay,
           unit, user, weapon]

for sub_bp in bp_list:
    api.register_blueprint(sub_bp)
