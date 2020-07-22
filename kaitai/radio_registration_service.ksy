meta:
  id: radio_registration_service
  imports:
    - radio_ip
enums:
  rrs_types:
    0x03: registration
    0x80: registration_ack
    0x01: de_registration
    0x02: online_check
    0x82: online_check_ack
seq:
  - id: opcode
    contents: [0x00]
  - id: rrs_type
    enum: rrs_types
    type: u1
  - id: message_length
    type: u2le
    doc: length of the message from next field to the end of RRS message
  - id: radio_ip
    type: radio_ip
  - id: result
    type: u1
    if: rrs_type == rrs_types::registration_ack or rrs_type == rrs_types::online_check_ack
  - id: valid_time
    type: u4be
    doc: number of seconds the online registration message shall be resended from terminal
    if: rrs_type == rrs_types::registration_ack
