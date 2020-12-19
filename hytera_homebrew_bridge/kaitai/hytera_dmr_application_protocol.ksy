meta:
  id: hytera_dmr_application_protocol
  imports:
    - location_protocol
    - radio_registration_service
    - data_transmit_protocol
    - text_message_protocol
    - telemetry_protocol
    - data_delivery_states
    - radio_control_protocol
enums:
  message_header_types:
    0x02: radio_control_protocol
    0x08: location_protocol
    0x09: text_message_protocol
    0x11: radio_registration
    0x12: telemetry_protocol
    0x13: data_transmit_protocol
    0x14: data_delivery_states
types:
  undefined_protocol:
    seq:
      - id: data
        size-eos: true
instances:
  is_reliable_message:
    type: b1
    pos: 0
  message_type:
    enum: message_header_types
    value: message_header & 0x8F
seq:
  - id: message_header
    type: u1
  - id: data
    doc: |
      contains opcode (2 bytes), payload length (2 bytes) and payload (if length > 0)
    type:
      switch-on: message_type
      cases:
        message_header_types::radio_control_protocol: radio_control_protocol
        message_header_types::location_protocol: location_protocol
        message_header_types::text_message_protocol: text_message_protocol
        message_header_types::radio_registration: radio_registration_service
        message_header_types::telemetry_protocol: telemetry_protocol
        message_header_types::data_transmit_protocol: data_transmit_protocol
        message_header_types::data_delivery_states: data_delivery_states
  - id: checksum
    type: u1
  - id: message_footer
    contents: [0x03]
