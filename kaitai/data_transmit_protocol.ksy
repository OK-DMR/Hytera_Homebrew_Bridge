meta:
  id: data_transmit_protocol
  imports:
    - radio_ip
enums:
  service_types:
    0xA0: data_transmit_protocol
  service_specific_types:
    0x01: dtp_request
    0x11: dtp_answer
    0x02: data_slice_trasmit
    0x12: data_slice_answer
    0x03: last_data_slice
    0x13: last_data_slice_answer
  results:
    0x00: success
    0x01: failure
types:
  dtp_request:
    seq:
      - id: destination_ip
        type: radio_ip
      - id: source_ip
        type: radio_ip
      - id: file_size
        type: u2be
        doc: size in bytes
      - id: file_name
        type: str
        size: _parent.message_length - 10
        encoding: UTF16-LE
        doc: maximum of 256 bytes including file extension, if longer, recipient should refuse the transmission
  dtp_answer:
    seq:
      - id: destination_ip
        type: radio_ip
      - id: source_ip
        type: radio_ip
      - id: result
        type: u1
        enum: results
  data_slice_transmit:
    seq:
      - id: destination_ip
        type: radio_ip
      - id: source_ip
        type: radio_ip
      - id: block_number
        type: u2be
        doc: sequence number in transfer, starting with 1
      - id: file_data
        size: _parent.message_length - 10
        doc: 448 bytes slice of transmitted file, or shorter if current slice is the last one
  data_slice_answer:
    seq:
      - id: destination_ip
        type: radio_ip
      - id: source_ip
        type: radio_ip
      - id: block_number
        type: u2be
        doc: sequence number in transfer, same as data_slice_transmit.block_number the response is for
      - id: result
        type: u1
        enum: results
        doc: result of transmit from receiving end
  last_data_slice:
    doc: sent by transmit source, requires answer from the destination
    seq:
      - id: destination_ip
        type: radio_ip
        doc: transmit recipient ip
      - id: source_ip
        type: radio_ip
        doc: transmit sender ip
  last_data_slice_answer:
    seq:
      - id: destination_ip
        type: radio_ip
        doc: transmit sender ip
      - id: source_ip
        type: radio_ip
        doc: transmit recipient ip
      - id: result
        type: u1
        enum: results
seq:
  - id: service_type
    type: u1
    enum: service_types
    doc: should be always 0xA0 Data Transmit Protocol
  - id: service_specific_type
    type: u1
    enum: service_specific_types
  - id: message_length
    type: u2be
    doc: length of the message from next field to the end of DTP message
  - id: data
    type:
      switch-on: service_specific_type
      cases:
        service_specific_types::dtp_request: dtp_request
        service_specific_types::dtp_answer: dtp_answer
        service_specific_types::data_slice_transmit: data_slice_transmit
        service_specific_types::data_slice_answer: data_slice_answer
        service_specific_types::last_data_slice: last_data_slice
        service_specific_types::last_data_slice_answer: last_data_slice_answer