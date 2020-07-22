meta:
  id: location_protocol
  imports:
    - radio_ip
    - datetimestring
    - intervalstring
    - gpsdata
enums:
  lp_general_types:
    0xA0: standard_location_immediate_service
    0xB0: emergency_location_reporting_service
    0xC0: triggered_location_reporting_service
    0xD0: condition_triggered_reporting_service
  lp_specific_types:
    0xA001: standard_request
    0xA002: standard_answer
    0xB001: emergency_report_stop_request
    0xB002: emergency_report_stop_answer
    0xB003: emergency_report
    0xC001: triggered_report_request
    0xC002: triggered_report_answer
    0xC003: triggered_report
    0xC004: triggered_report_stop_request
    0xC005: triggered_report_stop_answer
    0xD001: condition_report_request
    0xD002: condition_report_answer
    0xD003: condition_report
    0xD011: condition_quick_gps_request
    0xD012: condition_quick_gps_answer
  cmd_types:
    0x00: cancel_request
    0x01: start_request
  trigger_types:
    0x00: cancel_request
    0x01: distance
    0x02: time
    0x03: distance_and_time
    0x04: distance_or_time
  result_codes:
    0x00: ok
    0x06: position_method_failure
    0x69: request_format_error
seq:
  - id: opcode_header
    size: 2
  - id: message_length
    type: u2be
    doc: length of the message from next field to the end of LP message
  - id: data
    type:
      switch-on: opcode_header_int
      cases:
        lp_specific_types::standard_request: standard_request
        lp_specific_types::standard_answer: standard_answer
        lp_specific_types::emergency_report_stop_request: emergency_report_stop_request
        lp_specific_types::emergency_report_stop_answer: emergency_report_stop_answer
        lp_specific_types::emergency_report: emergency_report
        lp_specific_types::triggered_report_request: triggered_report_request
        lp_specific_types::triggered_report_answer: triggered_report_answer
        lp_specific_types::triggered_report: triggered_report
        lp_specific_types::triggered_report_stop_request: triggered_report_stop_request
        lp_specific_types::triggered_report_stop_answer: triggered_report_stop_answer
        lp_specific_types::condition_report_request: condition_report_request
        lp_specific_types::condition_report_answer: condition_report_answer
        lp_specific_types::condition_report: condition_report
        lp_specific_types::condition_quick_gps_request: condition_quick_gps_request
        lp_specific_types::condition_quick_gps_answer: condition_quick_gps_answer
types:
  standard_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
  standard_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: result
        type: u2be
        enum: result_codes
      - id: gpsdata
        type: gpsdata
  emergency_report_stop_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
  emergency_report_stop_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: result
        type: u2be
        enum: result_codes
  emergency_report:
    seq:
      - id: radio_ip
        type: radio_ip
      - id: emergency_type
        type: u1
      - id: gpsdata
        type: gpsdata
  triggered_report_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: start_time
        type: datetimestring
      - id: stop_time
        type: datetimestring
      - id: interval
        type: intervalstring
  triggered_report_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: result
        type: u2be
        enum: result_codes
  triggered_report:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: time_remaining
        type: intervalstring
      - id: gpsdata
        type: gpsdata
  triggered_report_stop_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
  triggered_report_stop_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: result
        type: u2be
        enum: result_codes
  condition_report_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: trigger_type
        type: u1
      - id: distance
        type: u4be
      - id: start_time
        type: datetimestring
      - id: stop_time
        type: datetimestring
      - id: interval
        type: intervalstring
      - id: max_interval
        type: intervalstring
  condition_report_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: trigger_type
        type: u1
        enum: trigger_types
      - id: result
        type: u2be
        enum: result_codes
  condition_report:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: gpsdata
        type: gpsdata
  condition_quick_gps_request:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: cmd_type
        type: u1
        enum: cmd_types
      - id: quick_gps_payload
        type: quick_gps_payload
        if: cmd_type == cmd_types::start_request
  quick_gps_payload:
    seq:
      - id: start_time
        type: datetimestring
      - id: stop_time
        type: datetimestring
      - id: interval
        type: intervalstring
      - id: send_step
        type: u2be
        doc: milliseconds
      - id: channel_use_percentage
        type: u1
      - id: send_order
        type: u2be
        doc: sequence number, ie. n-th radio to report position once the interval time is up
  condition_quick_gps_answer:
    seq:
      - id: request_id
        type: u4be
      - id: radio_ip
        type: radio_ip
      - id: cmd_type
        type: u1
        enum: cmd_types
      - id: result
        type: u2be
        enum: result_codes
instances:
  opcode:
    pos: 0
    enum: lp_general_types
    type: u1
  opcode_header_int:
    pos: 0
    enum: lp_specific_types
    type: u2be