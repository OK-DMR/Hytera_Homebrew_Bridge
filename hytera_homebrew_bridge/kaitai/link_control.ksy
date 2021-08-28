meta:
  id: link_control
  endian: le
doc: |
  ETSI TS 102 361-2 V2.4.1 (2017-10), Section 7.1.1
enums:
  flcos:
    0b000000: group_voice
    0b000011: unit_to_unit_voice
    0b001000: gps_info
    0b000100: talker_alias_header
    0b000101: talker_alias_block1
    0b000110: talker_alias_block2
    0b000111: talker_alias_block3
  position_errors:
    0b000: less_than_2m
    0b001: less_than_20m
    0b010: less_than_200m
    0b011: less_than_2km
    0b100: less_than_20km
    0b101: less_than_or_equal_200km
    0b110: more_than_200km
    0b111: position_error_unknown_or_invalid
  talker_data_formats:
    0b00: coding_7bit
    0b01: coding_8bit
    0b10: unicode_utf8
    0b11: unicode_utf16
  feature_set_ids:
    0b00000000: standardized_ts_102_361_2
    0b00000001: reserved1
    0b00000010: reserved2
    0b00000011: reserved3
    0b00000100: mfid_start
    0b01111111: mfid_end
    0b10000000: mfid_reserved_start
    0b11111111: mfid_reserved_end
types:
  group_voice_channel_user:
    seq:
      - id: service_options
        type: b8
      - id: group_address
        type: b24
      - id: source_address
        type: b24
  unit_to_unit_voice_channel_user:
    seq:
      - id: service_options
        type: b8
      - id: target_address
        type: b24
      - id: source_address
        type: b24
  gps_info_lc_pdu:
    seq:
      - id: reserved
        type: b4
      - id: position_error
        type: b3
        enum: position_errors
      - id: longitude
        type: b25
      - id: latitude
        type: b24
  talker_alias_header:
    seq:
      - id: talker_alias_data_format
        type: b2
        enum: talker_data_formats
      - id: talker_alias_data_length
        type: b5
      - id: talker_alias_data
        type: b49
        doc: 8-bit/16-bit coded => 1st bit reserved (6 or 3 characters), 7-bit coded => all used (7 characters)
  talker_alias_continuation:
    seq:
      - id: talker_alias_data
        type: b56
        doc: 7-bit => 8 characters, 8-bit => 7 characters, 16-bit => 3 characters
seq:
  - id: protect_flag
    type: b1
  - id: reserved
    type: b1
  - id: full_link_control_opcode
    type: b6
    enum: flcos
  - id: feature_set_id
    type: b8
    doc: fid
    enum: feature_set_ids
  - id: specific_data
    type:
      switch-on: full_link_control_opcode
      cases:
        'flcos::group_voice': group_voice_channel_user
        'flcos::unit_to_unit_voice': unit_to_unit_voice_channel_user
        'flcos::gps_info': gps_info_lc_pdu
        'flcos::talker_alias_header': talker_alias_header
        'flcos::talker_alias_block1': talker_alias_continuation
        'flcos::talker_alias_block2': talker_alias_continuation
        'flcos::talker_alias_block3': talker_alias_continuation