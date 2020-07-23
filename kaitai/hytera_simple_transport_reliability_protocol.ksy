meta:
  id: hytera_simple_transport_reliability_protocol
  imports:
    - hytera_dmr_application_protocol
seq:
  - id: header
    type: str
    size: 2
    encoding: UTF-8
    doc: should be ascii 2B
  - id: version
    type: u1
    doc: current version is 0x00
  - id: reserved
    type: b2
  - id: has_option
    type: b1
  - id: is_reject
    type: b1
  - id: is_close
    type: b1
  - id: is_connect
    type: b1
  - id: is_heartbeat
    type: b1
  - id: is_ack
    type: b1
  - id: sequence_number
    type: u2be
    doc: number equal for ACK and retransmited messages, and raised for each reply/new message
  - id: options
    if: not _io.eof and not is_heartbeat
    type: option
    repeat: until
    repeat-until: not _.expect_more_options
  - id: data
    type: hytera_dmr_application_protocol
    if: not _io.eof and has_option == true and not is_reject and not is_close and not is_connect
    repeat: eos
enums:
  option_commands:
    1: realtime
    3: device_id
    4: channel_id
types:
  option:
    seq:
      - id: expect_more_options
        type: b1
      - id: command
        type: b7
        enum: option_commands
      - id: option_data_length
        type: u1
      - id: option_payload
        size: option_data_length
