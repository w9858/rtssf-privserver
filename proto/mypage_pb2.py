# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mypage.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmypage.proto\x12\nSpy.MyPage\x1a\x0c\x63ommon.proto\"$\n\x0cRequestIndex\x12\x14\n\x0ctips_id_list\x18\x01 \x03(\x05\"\x90\x08\n\rResponseIndex\x12J\n\x17t_user_login_bonus_list\x18\x01 \x03(\x0b\x32).Spy.MyPage.ResponseIndex.TUserLoginBonus\x12!\n\x06t_user\x18\x07 \x01(\x0b\x32\x11.Spy.Common.TUser\x12\x31\n\x11t_user_count_list\x18\x08 \x03(\x0b\x32\x16.Spy.Common.TUserCount\x12$\n\x1c\x65xists_new_clear_achievement\x18\t \x01(\x05\x12\x15\n\rpresent_count\x18\n \x01(\x05\x12\x1a\n\x12shop_new_item_flag\x18\x0b \x01(\x05\x12\x30\n\x0et_user_crystal\x18\x0c \x01(\x0b\x32\x18.Spy.Common.TUserCrystal\x12?\n\x11m_app_banner_list\x18\r \x03(\x0b\x32$.Spy.MyPage.ResponseIndex.MAppBanner\x12\x30\n\tm_ad_list\x18\x0e \x03(\x0b\x32\x1d.Spy.MyPage.ResponseIndex.MAd\x12\x1d\n\x15\x65xists_friend_invited\x18\x0f \x01(\x05\x12/\n\x10t_user_tips_list\x18\x10 \x03(\x0b\x32\x15.Spy.Common.TUserTips\x12!\n\x19no_read_information_count\x18\x11 \x01(\x05\x12\x36\n\nt_user_ban\x18\x12 \x01(\x0b\x32\".Spy.MyPage.ResponseIndex.TUserBan\x12\x1a\n\x12gamecenter_id_list\x18\x13 \x03(\x05\x1aH\n\x0fTUserLoginBonus\x12\x16\n\x0elogin_bonus_id\x18\x01 \x01(\x05\x12\x10\n\x08sheet_id\x18\x02 \x01(\x05\x12\x0b\n\x03\x64\x61y\x18\x03 \x01(\x05\x1a\xa0\x01\n\nMAppBanner\x12\x12\n\nbanner_img\x18\x01 \x01(\t\x12\r\n\x05order\x18\x02 \x01(\x05\x12\x15\n\rtransition_id\x18\x03 \x01(\x05\x12\x18\n\x10transition_value\x18\x04 \x01(\x05\x12\x10\n\x08start_at\x18\x05 \x01(\t\x12\x0e\n\x06\x65nd_at\x18\x06 \x01(\t\x12\x1c\n\x14\x65nd_of_tutorial_from\x18\x07 \x01(\x05\x1aY\n\x03MAd\x12\x0f\n\x07\x61\x64_type\x18\x01 \x01(\x05\x12\x11\n\ttarget_id\x18\x02 \x01(\x05\x12\x14\n\x0c\x66\x61\x64\x65_pattern\x18\x03 \x01(\x05\x12\x18\n\x10particle_pattern\x18\x04 \x01(\x05\x1aP\n\x08TUserBan\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x16\n\x0enotice_message\x18\x02 \x01(\t\x12\x10\n\x08start_at\x18\x03 \x01(\t\x12\x0e\n\x06\x65nd_at\x18\x04 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mypage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTINDEX._serialized_start=42
  _REQUESTINDEX._serialized_end=78
  _RESPONSEINDEX._serialized_start=81
  _RESPONSEINDEX._serialized_end=1121
  _RESPONSEINDEX_TUSERLOGINBONUS._serialized_start=713
  _RESPONSEINDEX_TUSERLOGINBONUS._serialized_end=785
  _RESPONSEINDEX_MAPPBANNER._serialized_start=788
  _RESPONSEINDEX_MAPPBANNER._serialized_end=948
  _RESPONSEINDEX_MAD._serialized_start=950
  _RESPONSEINDEX_MAD._serialized_end=1039
  _RESPONSEINDEX_TUSERBAN._serialized_start=1041
  _RESPONSEINDEX_TUSERBAN._serialized_end=1121
# @@protoc_insertion_point(module_scope)
