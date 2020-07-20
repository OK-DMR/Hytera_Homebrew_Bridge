meta:
  id: hytera_dmr_application_protocol
enums:
  message_header_types:
    0x02: radio_control_protocol
    0x08: location_protocol
    0x09: text_message_protocol
    0x11: radio_registration
    0x12: telemetry_protocol
    0x13: data_transmit_protocol
    0x14: data_delivery_states
seq:
  - id: message_header
    type: u1
  - id: is_reliable_message
    type: b1
  - id: opcode
    type:
      switch-on: message_header
      cases:
        0x02: u2le
        0x82: u2le
        _: u2be
  - id: payload_size
    type:
      switch-on: message_header
      cases:
        0x02: u2le
        0x82: u2le
        _: u2be
  - id: payload
    size: payload_size
  - id: checksum
    type: u1
  - id: message_footer
    contents: [0x03]
