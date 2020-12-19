meta:
  id: radio_control_protocol
  endian: le
enums:
  service_types:
    0x0841: call_request
    0x8841: call_reply
  call_types:
    0x00: private_call
    0x01: group_call
    0x02: all_call
    0x03: emergency_group_call
    0x04: remote_monitor_call
    0x05: reserved
    0x06: priority_private_call
    0x07: priority_group_call
    0x08: priority_all_call
  call_reply_results:
    0x00: success
    0x01: failure
types:
  call_request:
    seq:
      - id: call_type
        enum: call_types
        type: u1
      - id: target_id
        type: u4le
        doc: ignored for all_call
  call_reply:
    seq:
      - id: result
        type: u1
        enum: call_reply_results
  generic_data:
    seq:
      - id: data
        size: _parent.message_length
seq:
  - id: service_type
    type: u2le
    enum: service_types
  - id: message_length
    type: u2le
    doc: length of the message from next field to the end of RCP message
  - id: data
    type:
      switch-on: service_type
      cases:
        service_types::call_request: call_request
        service_types::call_reply: call_reply
        _: generic_data