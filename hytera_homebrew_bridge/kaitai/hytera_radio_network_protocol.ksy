meta:
  id: hytera_radio_network_protocol
  imports:
    - hytera_dmr_application_protocol
enums:
  opcodes:
    0xFE: connect
    0xFD: accept
    0xFC: reject
    0xFB: close
    0xFA: close_ack
    0x00: data
    0x10: data_ack
seq:
  - id: header_identifier
    contents: [0x7E]
  - id: version
    type: u1
  - id: block
    type: u1
  - id: opcode
    type: u1
    enum: opcodes
  - id: source_id
    type: u1
  - id: destination_id
    type: u1
  - id: packet_number
    type: u2be
  - id: hrnp_packet_length
    type: u2be
  - id: checksum
    type: u2be
  - id: data
    if: opcode == opcodes::data
    type: hytera_dmr_application_protocol