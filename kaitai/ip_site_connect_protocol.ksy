meta:
  id: ip_site_connect_protocol
  imports:
    - radio_ip
doc: |
  Hytera IP Multi-Site Protocol re-implementation from dmrshark original
enums:
  slot_types:
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
    0xEEEE: slot_type_ipsc_sync
    0x0000: slot_type_unknown
  packet_types:
    0x41: a
    0x42: b
  timeslots:
    0x1111: timeslot_1
    0x2222: timeslot_2
  call_types:
    0x00: private_call
    0x01: group_call
seq:
  - id: fixed_header
    contents: [0x5a, 0x5a, 0x5a, 0x5a]
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
  - id: delimiter
    contents: [0x11, 0x11]
    doc: should be 0x1111
  - id: frame_type
    type: u2be
  - id: reserved_2a
    size: 2
  - id: ipsc_payload
    size: 34
  - id: reserved_2b
    size: 2
  - id: call_type
    type: u1
    enum: call_types
  - id: destination_radio_id
    type: radio_ip
  - id: source_radio_id
    type: radio_ip
  - id: reserved_1b
    type: u1