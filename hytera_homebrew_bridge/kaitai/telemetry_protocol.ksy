meta:
  id: telemetry_protocol
  imports:
    - radio_ip
enums:
  service_types:
    0xA0: status_report_service
    0xB0: remote_control_service
  service_specific_types:
    0xA001: standard_status_request
    0xA081: standard_status_report
    0xA082: extended_status_report
    0xB001: remote_control_request
    0xB081: remote_control_answer
  pc_flag_types:
    0x00: controller_is_radio
    0x01: controller_is_telemetry_application
  call_types:
    0x00: private_call
    0x01: group_call
    0x02: all_call
  result_types:
    0x00: effective
    0x01: ineffective
  control_result_types:
    0x00: success
    0x01: failure
  operation_types:
    0x00: set_ineffective_level
    0x01: set_effective_level
    0x02: reverse_level
    0x03: output_one_pulse
instances:
  specific_service:
    pos: 0
    type: u2be
    enum: service_specific_types
types:
  vio_extended_status:
    seq:
      - id: result
        type: u1
        enum: result_types
      - id: message_length
        type: u2be
      - id: message
        type: str
        encoding: UTF16-LE
        size: message_length
  standard_status_request:
    seq:
      - id: source_ip
        type: radio_ip
      - id: target_ip
        type: radio_ip
      - id: pc_flag
        type: u1
        enum: pc_flag_types
      - id: call_type
        type: u1
        enum: call_types
      - id: vio_select
        size: 1
        doc: reserved
  standard_status_report:
    seq:
      - id: source_ip
        type: radio_ip
      - id: target_ip
        type: radio_ip
      - id: pc_flag
        type: u1
        enum: pc_flag_types
      - id: call_type
        type: u1
        enum: call_types
        doc: answer should be always of type private call for now
      - id: vio_select
        size: 1
        doc: reserved
      - id: result
        type: u1
        enum: result_types
  extended_status_report:
    seq:
      - id: source_ip
        type: radio_ip
      - id: target_ip
        type: radio_ip
      - id: pc_flag
        type: u1
        enum: pc_flag_types
      - id: call_type
        type: u1
        enum: call_types
        doc: answer should be always of type private call for now
      - id: vio_select
        size: 1
        doc: reserved
      - id: result_messages
        type: vio_extended_status
  remote_control_request:
    seq:
      - id: source_ip
        type: radio_ip
      - id: target_ip
        type: radio_ip
      - id: pc_flag
        type: u1
        enum: pc_flag_types
      - id: call_type
        type: u1
        enum: call_types
        doc: answer should be always of type private call for now
      - id: vio_select
        size: 1
        doc: Bit 0-5 correspond to VIO1-VIO6, 1=selected, 0=not selected, only one can be selected in request
      - id: operation
        type: u1
        enum: operation_types
  remote_control_answer:
    seq:
      - id: source_ip
        type: radio_ip
      - id: target_ip
        type: radio_ip
      - id: pc_flag
        type: u1
        enum: pc_flag_types
      - id: call_type
        type: u1
        enum: call_types
        doc: answer should be always of type private call for now
      - id: vio_select
        size: 1
        doc: Bit 0-5 correspond to VIO1-VIO6, 1=selected, 0=not selected, corresponds to request
      - id: result
        type: u1
        enum: control_result_types
seq:
  - id: service_type_opcode
    type: u1
    enum: service_types
  - id: specific_service_opcode
    type: u1
  - id: message_length
    type: u2be
    doc: length of the message from next field to the end of TP message
  - id: data
    type:
      switch-on: specific_service
      cases:
        service_specific_types::standard_status_request: standard_status_request
        service_specific_types::standard_status_report: standard_status_report
        service_specific_types::extended_status_report: extended_status_report
        service_specific_types::remote_control_request: remote_control_request
        service_specific_types::remote_control_answer: remote_control_answer