meta:
  id: data_delivery_states
  imports:
    - radio_ip
enums:
  state_types:
    0x08: location_protocol_state
    0x11: radio_registration_service_state
    0x12: telemetry_protocol_state
    0x13: data_transmit_protocol_state
  results:
    0: ok
    1: fail
    4: limited_timeout
    5: no_ack
    6: error_ack
    7: repeater_wakeup_fail
    8: tx_interrupted
    9: tx_deny
    10: invalid_params
seq:
  - id: reserved
    size: 1
    doc: should be 0x00
  - id: state_type
    type: u1
    enum: state_types
  - id: message_length
    type: u2be
    doc: length of the message from next field to the end of DDS message
  - id: radio_ip
    type: radio_ip
  - id: protocol_opcode
    type: u2be
    doc: state_type+protocol_opcode should correspond to sent message, that this status is about
  - id: result
    type: u1
    enum: results