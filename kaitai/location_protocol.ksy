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
  subtypes:
    # emergency report_stop_request
    0x01: report_request
    # emergency report_stop_answer
    0x02: report_answer
    0x03: report
    # triggered only
    0x04: report_stop_request
    0x05: report_stop_answer
    # conditional only
    0x11: quick_gps_request
    0x12: quick_gps_answer
types:
  request_id:
    seq:
      - id: request_id
        size: 4
  append_standard_answer:
    seq:
      - id: result
        size: 2
      - id: gpsdata
        type: gpsdata
  append_result:
    doc: |
      applies to emergency.stop_answer, triggered.report_answer, triggered.report_stop_answer
    seq:
      - id: result
        size: 2
  append_emergency_report:
    seq:
      - id: emergency_type
        size: 1
      - id: gpsdata
        type: gpsdata
  append_triggered_report_request:
    seq:
      - id: starttime
        type: datetimestring
      - id: stoptime
        type: datetimestring
      - id: interval
        type: intervalstring
seq:
  - id: opcode
    enum: lp_general_types
    type: u1
  - id: subtype
    type: u1
    enum: subtypes
  - id: request_id
    size: 4
    if: opcode != lp_general_types::emergency_location_immediate_service and subtype != subtypes::report
  - id: radio_ip
    type: radio_ip