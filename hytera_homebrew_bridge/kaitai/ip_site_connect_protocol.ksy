meta:
  id: ip_site_connect_protocol
  endian: le
doc: |
  Hytera IP Multi-Site Protocol re-implementation from dmrshark original
enums:
  slot_types:
    0x0000: slot_type_privacy_indicator
    0x1111: slot_type_voice_lc_header
    0x2222: slot_type_terminator_with_lc
    0x3333: slot_type_csbk
    0x4444: slot_type_data_header
    0x5555: slot_type_rate_12_data
    0x6666: slot_type_rate_34_data
    0x7777: slot_type_data_c
    0x8888: slot_type_data_d
    0x9999: slot_type_data_e
    0xAAAA: slot_type_data_f
    0xBBBB: slot_type_data_a
    0xCCCC: slot_type_data_b
    0xDDDD: slot_type_wakeup_request
    # migh be data or voice sync as well
    0xEEEE: slot_type_sync
  frame_types:
    0x1111: frame_type_voice_sync
    0x3333: frame_type_data_sync_or_csbk
    0xEEEE: frame_type_sync
    0x6666: frame_type_data_header
    0xBBBB: frame_type_voice
    0x0000: frame_type_data
  packet_types:
    0x41: a
    0x42: b
  timeslots:
    0x1111: timeslot_1
    0x2222: timeslot_2
  call_types:
    0x00: private_call
    0x01: group_call
instances:
  source_radio_id:
    value: source_radio_id_raw >> 8
  destination_radio_id:
    value: destination_radio_id_raw >> 8
  color_code:
    value: color_code_raw & 0x000F
seq:
  - id: source_port
    size: 2
    doc: |
      UDP source port of IPSC packet
  - id: fixed_header
    size: 2
  - id: sequence_number
    type: u1
  - id: reserved_3
    size: 3
  - id: packet_type
    type: u1
    enum: packet_types
  - id: reserved_7a
    size: 7
  - id: timeslot_raw
    enum: timeslots
    type: u2be
  - id: slot_type
    type: u2be
    enum: slot_types
  - id: color_code_raw
    type: u2le
    doc: will be color code repeated, ie. cc=5 means two incoming bytes [0x55, 0x55]
  - id: frame_type
    type: u2be
    enum: frame_types
  - id: reserved_2a
    size: 2
  - id: ipsc_payload
    size: 34
  - id: reserved_2b
    size: 2
  - id: call_type
    type: u1
    enum: call_types
  - id: destination_radio_id_raw
    type: u4le
  - id: source_radio_id_raw
    type: u4le
  - id: reserved_1b
    type: u1
  - id: extra_data
    size-eos: true
    if: not _io.eof
