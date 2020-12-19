meta:
  id: self_defined_message_protocol
  imports:
    - radio_ip
enums:
  ack_flags:
    0: ack_required
    1: ack_not_required
  option_flags:
    0: option_len_and_field_disabled
    1: option_len_and_field_enabled
  service_types:
    0xAC: private_work_order
    0xAD: private_work_order_ack
    0xBC: group_work_order
    0xBD: group_work_order_ack
    0xAE: private_short_data
    0xAF: private_short_data_ack
    0xBE: group_short_data
    0xBF: group_short_data_ack
  result_codes:
    0: ok
    1: fail
    3: invalid_params
    4: channel_busy
    5: rx_only
    6: low_battery
    7: pll_unlock
    8: private_call_no_ack
    9: repeater_wakeup_fail
    10: no_contact
    11: tx_deny
    12: tx_interrupted
  work_states:
    0x00: new
    0x01: delete
    0x10: decline
    0x20: state_1
    0x21: state_2
    0x22: state_3
    0x23: state_4
    0x24: state_5
instances:
  is_ack_service:
    value: |
      service_type == service_types::private_work_order_ack
      or service_type == service_types::group_work_order_ack
      or service_type == service_types::private_short_data_ack
      or service_type == service_types::group_short_data_ack
  is_work_order:
    value: |
      service_type == service_types::private_work_order
      or service_type == service_types::private_work_order_ack
      or service_type == service_types::group_work_order
      or service_type == service_types::group_work_order_ack
  is_short_data:
    value: |
      service_type == service_types::private_short_data
      or service_type == service_types::private_short_data_ack
      or service_type == service_types::group_short_data
      or service_type == service_types::group_short_data_ack
types:
  date:
    seq:
      - id: year
        type: u2be
      - id: month
        type: u1
      - id: day
        type: u1
  work_order:
    seq:
      - id: work_order_header
        contents: [0xFF, 0xFF, 0xFF, 0xFF]
      - id: date
        type: date
      - id: sequence_number
        type: u4be
      - id: work_state
        type: u2be
        enum: work_states
      - id: reserved
        size: 38
      - id: contents
        type: str
        terminator: 0x0000
        encoding: UTF16-LE
seq:
  - id: ack_flag
    type: b1
    enum: ack_flags
  - id: option_flag
    type: b1
    enum: option_flags
    doc: option fields might not be supported yet
  - id: reserved
    type: b6
  - id: service_type
    type: u1
    enum: service_types
  - id: message_length
    type: u2be
    doc: length of the message from next field to the end of SDMP message
  - id: option_field_len
    type: u2be
    if: option_flag.to_i == 1
  - id: request_id
    type: u4be
  - id: destination_ip
    type: radio_ip
    doc: destination, either single or group ID in ipv4 format
  - id: source_ip
    type: radio_ip
    if: is_ack_service != true
  - id: result
    type: u1
    enum: result_codes
    if: is_ack_service == true
  - id: work_order
    if: is_ack_service == false and is_work_order == true
    type: work_order
  - id: short_data
    type: str
    encoding: UTF16-LE
    terminator: 0
    if: is_ack_service == false and is_short_data == true
  - id: option_field
    type: str
    encoding: UTF16-LE
    size: option_field_len
    if: option_flag.to_i == 1