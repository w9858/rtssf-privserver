# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: quest.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bquest.proto\x12\tSpy.Quest\x1a\x0c\x63ommon.proto\"\xb4\x03\n\x0cRequestClear\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\x12\x0f\n\x07\x64\x65\x63k_no\x18\x03 \x01(\x05\x12/\n\twave_list\x18\x04 \x03(\x0b\x32\x1c.Spy.Quest.RequestClear.Wave\x12:\n\x0fquest_item_list\x18\x05 \x03(\x0b\x32!.Spy.Quest.RequestClear.QuestItem\x12\x10\n\x08\x65vent_id\x18\x06 \x01(\x05\x12\x1a\n\x12is_clear_mission_1\x18\x07 \x01(\x08\x12\x1a\n\x12is_clear_mission_2\x18\x08 \x01(\x08\x12\x1a\n\x12is_clear_mission_3\x18\t \x01(\x08\x12\x1a\n\x12\x61\x63tive_skill_count\x18\n \x01(\x05\x12\x19\n\x11spyce_burst_count\x18\x0c \x01(\x05\x12\r\n\x05score\x18\r \x01(\x05\x1a,\n\tQuestItem\x12\x0f\n\x07item_id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x1a+\n\x04Wave\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x12\n\nis_success\x18\x02 \x01(\x05\"D\n\x0fRequestClearAdv\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\x12\x10\n\x08\x65vent_id\x18\x03 \x01(\x05\"2\n\x0fRequestContinue\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\"\x97\x02\n\x0bRequestFail\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\x0f\n\x07\x64\x65\x63k_no\x18\x02 \x01(\x05\x12\r\n\x05token\x18\x03 \x01(\t\x12\x10\n\x08\x65vent_id\x18\x04 \x01(\x05\x12.\n\twave_list\x18\x05 \x03(\x0b\x32\x1b.Spy.Quest.RequestFail.Wave\x12\x39\n\x0fquest_item_list\x18\n \x03(\x0b\x32 .Spy.Quest.RequestFail.QuestItem\x1a,\n\tQuestItem\x12\x0f\n\x07item_id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x1a+\n\x04Wave\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x12\n\nis_success\x18\x02 \x01(\x05\"&\n\x12RequestGetBookList\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\"<\n\x19RequestGetContinueCrystal\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\",\n\x12RequestGetUserList\x12\x16\n\x0equest_category\x18\x01 \x01(\x05\"\x8c\x01\n\rRequestRetire\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12;\n\x0fquest_item_list\x18\x02 \x03(\x0b\x32\".Spy.Quest.RequestRetire.QuestItem\x1a,\n\tQuestItem\x12\x0f\n\x07item_id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\"0\n\rRequestReturn\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\r\n\x05token\x18\x02 \x01(\t\"\xf3\x01\n\x0cRequestStart\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\x0f\n\x07\x64\x65\x63k_no\x18\x02 \x01(\x05\x12\x16\n\x0e\x66riend_user_id\x18\x03 \x01(\x05\x12:\n\x0fquest_item_list\x18\x04 \x03(\x0b\x32!.Spy.Quest.RequestStart.QuestItem\x12\x10\n\x08\x65vent_id\x18\x05 \x01(\x05\x12\x14\n\x0citem_id_list\x18\x06 \x03(\x05\x12\x16\n\x0e\x66riend_unit_id\x18\x07 \x01(\x05\x1a,\n\tQuestItem\x12\x0f\n\x07item_id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\"5\n\x0fRequestStartAdv\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\x10\n\x08\x65vent_id\x18\x02 \x01(\x05\"\x8f\x04\n\rResponseClear\x12\'\n\tdrop_list\x18\x02 \x03(\x0b\x32\x14.Spy.Common.Resource\x12:\n\x1cmission_complete_reward_list\x18\x03 \x03(\x0b\x32\x14.Spy.Common.Resource\x12,\n\x0ct_user_quest\x18\x05 \x01(\x0b\x32\x16.Spy.Common.TUserQuest\x12\x39\n\x13t_user_quest_status\x18\x06 \x01(\x0b\x32\x1c.Spy.Common.TUserQuestStatus\x12J\n\x1et_user_character_friendly_list\x18\x07 \x03(\x0b\x32\".Spy.Common.TUserCharacterFriendly\x12\x1b\n\x13is_unlock_spy_frame\x18\x08 \x01(\x08\x12@\n\x16update_resource_result\x18\t \x01(\x0b\x32 .Spy.Common.UpdateResourceResult\x12\x14\n\x0c\x66riend_point\x18\n \x01(\x05\x12\x11\n\tis_friend\x18\x0b \x01(\x08\x12\x12\n\nis_invited\x18\x0c \x01(\x08\x12\x11\n\tis_invete\x18\r \x01(\x08\x12\x35\n\x13t_user_archive_list\x18\x0e \x03(\x0b\x32\x18.Spy.Common.TUserArchive\"\x85\x02\n\x10ResponseClearAdv\x12,\n\x0ct_user_quest\x18\x01 \x01(\x0b\x32\x16.Spy.Common.TUserQuest\x12\x39\n\x13t_user_quest_status\x18\x02 \x01(\x0b\x32\x1c.Spy.Common.TUserQuestStatus\x12!\n\x06t_user\x18\x03 \x01(\x0b\x32\x11.Spy.Common.TUser\x12.\n\rt_user_worker\x18\x04 \x01(\x0b\x32\x17.Spy.Common.TUserWorker\x12\x35\n\x13t_user_archive_list\x18\x05 \x03(\x0b\x32\x18.Spy.Common.TUserArchive\"T\n\x10ResponseContinue\x12@\n\x16update_resource_result\x18\x01 \x01(\x0b\x32 .Spy.Common.UpdateResourceResult\"P\n\x0cResponseFail\x12@\n\x16update_resource_result\x18\x02 \x01(\x0b\x32 .Spy.Common.UpdateResourceResult\"\xd1\x01\n\x13ResponseGetBookList\x12L\n\x15_user_quest_book_list\x18\x01 \x03(\x0b\x32-.Spy.Quest.ResponseGetBookList.TUserQuestBook\x1al\n\x0eTUserQuestBook\x12\x10\n\x08quest_id\x18\x01 \x01(\x05\x12\x11\n\tbook_type\x18\x02 \x01(\x05\x12\x13\n\x0btarget_type\x18\x03 \x01(\x05\x12\x11\n\ttarget_id\x18\x04 \x01(\x05\x12\r\n\x05\x63ount\x18\x05 \x01(\x05\"=\n\x1aResponseGetContinueCrystal\x12\x1f\n\x17\x63ontinue_crystal_amount\x18\x01 \x01(\x05\"H\n\x13ResponseGetUserList\x12\x31\n\x11t_user_quest_list\x18\x01 \x03(\x0b\x32\x16.Spy.Common.TUserQuest\"R\n\x0eResponseRetire\x12@\n\x16update_resource_result\x18\x01 \x01(\x0b\x32 .Spy.Common.UpdateResourceResult\"\xf6\x02\n\x0eResponseReturn\x12\x0f\n\x07\x64\x65\x63k_no\x18\x01 \x01(\x05\x12<\n\x0f\x65nemy_drop_list\x18\x03 \x03(\x0b\x32#.Spy.Quest.ResponseReturn.EnemyDrop\x12@\n\x11gimmick_drop_list\x18\x04 \x03(\x0b\x32%.Spy.Quest.ResponseReturn.GimmickDrop\x12-\n\x0cuser_profile\x18\x05 \x01(\x0b\x32\x17.Spy.Common.UserProfile\x12\x14\n\x0citem_id_list\x18\x07 \x03(\x05\x1a\\\n\tEnemyDrop\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x16\n\x0e\x65nemy_group_id\x18\x02 \x01(\x05\x12\x11\n\tenenmy_id\x18\x03 \x01(\x05\x12\x13\n\x0bposition_id\x18\x04 \x01(\x05\x1a\x30\n\x0bGimmickDrop\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x10\n\x08\x64rop_num\x18\x02 \x01(\x05\"\xdc\x02\n\rResponseStart\x12\r\n\x05token\x18\x01 \x01(\t\x12;\n\x0f\x65nemy_drop_list\x18\x02 \x03(\x0b\x32\".Spy.Quest.ResponseStart.EnemyDrop\x12?\n\x11gimmick_drop_list\x18\x03 \x03(\x0b\x32$.Spy.Quest.ResponseStart.GimmickDrop\x12.\n\rt_user_worker\x18\x04 \x01(\x0b\x32\x17.Spy.Common.TUserWorker\x1a\\\n\tEnemyDrop\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x16\n\x0e\x65nemy_group_id\x18\x02 \x01(\x05\x12\x11\n\tenenmy_id\x18\x03 \x01(\x05\x12\x13\n\x0bposition_id\x18\x04 \x01(\x05\x1a\x30\n\x0bGimmickDrop\x12\x0f\n\x07wave_id\x18\x01 \x01(\x05\x12\x10\n\x08\x64rop_num\x18\x02 \x01(\x05\"Q\n\x10ResponseStartAdv\x12\r\n\x05token\x18\x01 \x01(\t\x12.\n\rt_user_worker\x18\x02 \x01(\x0b\x32\x17.Spy.Common.TUserWorkerb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'quest_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTCLEAR._serialized_start=41
  _REQUESTCLEAR._serialized_end=477
  _REQUESTCLEAR_QUESTITEM._serialized_start=388
  _REQUESTCLEAR_QUESTITEM._serialized_end=432
  _REQUESTCLEAR_WAVE._serialized_start=434
  _REQUESTCLEAR_WAVE._serialized_end=477
  _REQUESTCLEARADV._serialized_start=479
  _REQUESTCLEARADV._serialized_end=547
  _REQUESTCONTINUE._serialized_start=549
  _REQUESTCONTINUE._serialized_end=599
  _REQUESTFAIL._serialized_start=602
  _REQUESTFAIL._serialized_end=881
  _REQUESTFAIL_QUESTITEM._serialized_start=388
  _REQUESTFAIL_QUESTITEM._serialized_end=432
  _REQUESTFAIL_WAVE._serialized_start=434
  _REQUESTFAIL_WAVE._serialized_end=477
  _REQUESTGETBOOKLIST._serialized_start=883
  _REQUESTGETBOOKLIST._serialized_end=921
  _REQUESTGETCONTINUECRYSTAL._serialized_start=923
  _REQUESTGETCONTINUECRYSTAL._serialized_end=983
  _REQUESTGETUSERLIST._serialized_start=985
  _REQUESTGETUSERLIST._serialized_end=1029
  _REQUESTRETIRE._serialized_start=1032
  _REQUESTRETIRE._serialized_end=1172
  _REQUESTRETIRE_QUESTITEM._serialized_start=388
  _REQUESTRETIRE_QUESTITEM._serialized_end=432
  _REQUESTRETURN._serialized_start=1174
  _REQUESTRETURN._serialized_end=1222
  _REQUESTSTART._serialized_start=1225
  _REQUESTSTART._serialized_end=1468
  _REQUESTSTART_QUESTITEM._serialized_start=388
  _REQUESTSTART_QUESTITEM._serialized_end=432
  _REQUESTSTARTADV._serialized_start=1470
  _REQUESTSTARTADV._serialized_end=1523
  _RESPONSECLEAR._serialized_start=1526
  _RESPONSECLEAR._serialized_end=2053
  _RESPONSECLEARADV._serialized_start=2056
  _RESPONSECLEARADV._serialized_end=2317
  _RESPONSECONTINUE._serialized_start=2319
  _RESPONSECONTINUE._serialized_end=2403
  _RESPONSEFAIL._serialized_start=2405
  _RESPONSEFAIL._serialized_end=2485
  _RESPONSEGETBOOKLIST._serialized_start=2488
  _RESPONSEGETBOOKLIST._serialized_end=2697
  _RESPONSEGETBOOKLIST_TUSERQUESTBOOK._serialized_start=2589
  _RESPONSEGETBOOKLIST_TUSERQUESTBOOK._serialized_end=2697
  _RESPONSEGETCONTINUECRYSTAL._serialized_start=2699
  _RESPONSEGETCONTINUECRYSTAL._serialized_end=2760
  _RESPONSEGETUSERLIST._serialized_start=2762
  _RESPONSEGETUSERLIST._serialized_end=2834
  _RESPONSERETIRE._serialized_start=2836
  _RESPONSERETIRE._serialized_end=2918
  _RESPONSERETURN._serialized_start=2921
  _RESPONSERETURN._serialized_end=3295
  _RESPONSERETURN_ENEMYDROP._serialized_start=3153
  _RESPONSERETURN_ENEMYDROP._serialized_end=3245
  _RESPONSERETURN_GIMMICKDROP._serialized_start=3247
  _RESPONSERETURN_GIMMICKDROP._serialized_end=3295
  _RESPONSESTART._serialized_start=3298
  _RESPONSESTART._serialized_end=3646
  _RESPONSESTART_ENEMYDROP._serialized_start=3153
  _RESPONSESTART_ENEMYDROP._serialized_end=3245
  _RESPONSESTART_GIMMICKDROP._serialized_start=3247
  _RESPONSESTART_GIMMICKDROP._serialized_end=3295
  _RESPONSESTARTADV._serialized_start=3648
  _RESPONSESTARTADV._serialized_end=3729
# @@protoc_insertion_point(module_scope)
