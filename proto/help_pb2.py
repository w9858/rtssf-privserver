# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: help.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nhelp.proto\x12\x08Spy.Help\x1a\x0c\x63ommon.proto\"\r\n\x0bRequestList\"\x9c\x02\n\x0cResponseList\x12\x31\n\x0bm_help_list\x18\x01 \x03(\x0b\x32\x1c.Spy.Help.ResponseList.MHelp\x12\x42\n\x14m_help_category_list\x18\x02 \x03(\x0b\x32$.Spy.Help.ResponseList.MHelpCategory\x1aU\n\x05MHelp\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\x05\x12\r\n\x05order\x18\x03 \x01(\x05\x12\r\n\x05title\x18\x04 \x01(\t\x12\x10\n\x08\x63ontents\x18\x05 \x01(\t\x1a>\n\rMHelpCategory\x12\x10\n\x08\x63\x61tegory\x18\x01 \x01(\x05\x12\r\n\x05order\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'help_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTLIST._serialized_start=38
  _REQUESTLIST._serialized_end=51
  _RESPONSELIST._serialized_start=54
  _RESPONSELIST._serialized_end=338
  _RESPONSELIST_MHELP._serialized_start=189
  _RESPONSELIST_MHELP._serialized_end=274
  _RESPONSELIST_MHELPCATEGORY._serialized_start=276
  _RESPONSELIST_MHELPCATEGORY._serialized_end=338
# @@protoc_insertion_point(module_scope)
