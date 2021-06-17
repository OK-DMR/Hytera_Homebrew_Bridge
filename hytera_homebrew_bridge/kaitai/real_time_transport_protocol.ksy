meta:
  id: real_time_transport_protocol
  endian: be
  imports:
    - radio_id
doc: |
  each packet should contain 60ms of voice data for AMBE compatibility
enums:
  rtp_payload_types:
    # G.711 μ-law PCMU
    0: mu_law
    # G.711 a-law PCMA - default
    8: a_law
  call_types:
    0x00: private_call
    0x01: group_call
    0x02: all_call
types:
  fixed_header:
    seq:
      - id: version
        type: b2
        valid: 2
      - id: padding
        type: b1
        doc: if set, this packet contains padding bytes at the end
      - id: extension
        type: b1
        doc: if set, fixed header is followed by single header extension
      - id: num_csrc
        type: b4
        doc: number of csrc identifiers that follow fixed header (val. 0-15)
      - id: marker
        type: b1
        doc: marker meaning is defined by RTP profile, for HDAP should be always 0
      - id: payload_type
        type: b7
      - id: sequence_number
        type: u2
        doc: sequence does not start from 0, but from random number
      - id: timestamp
        type: u4
        doc: sampling instant of the first octet in this RTP packet
      - id: ssrc
        type: u4
        doc: synchronized source identifier
      - id: csrc
        type: u4
        doc: contributing sources
        repeat: expr
        repeat-expr: num_csrc
  header_extension:
    seq:
      - id: header_identifier
        type: u2
      - id: length
        type: u2
        doc: number of 32bit words following the header+length fields
      - id: slot
        type: b7
        doc: slot number 1 or 2
      - id: last_flag
        type: b1
        doc: indicates end of voice call
      - id: source_id
        type: radio_id
      - id: destination_id
        type: radio_id
      - id: call_type
        type: u1
        enum: call_types
      - id: reserved
        size: 4
        doc: reserved 32bits
instances:
  len_padding_if_exists:
    pos: _io.size - 1
    type: u1
    if: fixed_header.padding
  len_padding:
    value: 'fixed_header.padding ? len_padding_if_exists : 0'
seq:
  - id: fixed_header
    type: fixed_header
  - id: header_extension
    type: header_extension
    if: fixed_header.extension
  - id: audio_data
    size: _io.size - _io.pos - len_padding
  - id: padding
    size: len_padding
    if: fixed_header.padding