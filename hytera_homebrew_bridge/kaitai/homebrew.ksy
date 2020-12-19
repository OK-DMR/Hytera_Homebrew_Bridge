meta:
  id: homebrew
  endian: be
doc: |
  Homebrew DMR protocol, based on PDF (DL5DI, G4KLX, DG1HT 2015) specification
types:
  type_dmr_data:
    seq:
      - id: sequence_no
        type: u1
      - id: source_id
        type: b24
      - id: target_id
        type: b24
      - id: repeater_id
        type: u4
      - id: slot_no
        type: b1
      - id: call_type
        type: b1
      - id: frame_type
        type: b2
      - id: data_type
        type: b4
      - id: stream_id
        type: u4
      - id: dmr_data
        size: 33
      - id: bit_error_rate
        type: u1
        if: not _io.eof
      - id: rssi
        type: u1
        if: not _io.eof
  type_repeater_login_request:
    seq:
      - id: repeater_id
        type: u4
  type_master_ping:
    seq:
      - id: magic
        contents: ING
      - id: repeater_id
        type: u4
  type_repeater_pong:
    seq:
      - id: magic
        contents: ONG
      - id: repeater_id
        type: u4
  type_master_closing:
    seq:
      - id: magic
        contents: L
      - id: repeater_id
        type: u4
  type_master_not_accept:
    seq:
      - id: magic
        contents: AK
      - id: repeater_id
        type: u4
  type_master_repeater_ack:
    seq:
      - id: magictype_master_repeater_ack
        contents: CK
      - id: repeater_id
        type: u4
      - id: random_number
        type: u4
        if: not _io.eof
  type_repeater_login_response:
    seq:
      - id: repeater_id
        type: u4
      - id: sha256
        size: 32
  type_repeater_configuration_or_closing:
    seq:
      - id: data
        type:
          switch-on: _root.fifth_letter
          cases:
            _: type_repeater_configuration
            '"L"': type_repeater_closing
  type_repeater_closing:
    seq:
      - id: magic
        contents: L
      - id: repeater_id
        type: u4
  type_repeater_configuration:
    seq:
      - id: repeater_id
        type: u4
      - id: call_sign
        type: str
        encoding: ASCII
        size: 8
      - id: rx_freq
        type: str
        encoding: ASCII
        size: 9
      - id: tx_freq
        type: str
        encoding: ASCII
        size: 9
      - id: tx_power
        type: str
        encoding: ASCII
        size: 2
      - id: color_code
        type: str
        encoding: ASCII
        size: 2
      - id: latitude
        type: str
        encoding: ASCII
        size: 8
      - id: longitude
        type: str
        encoding: ASCII
        size: 9
      - id: antenna_height_above_ground
        size: 3
        type: str
        encoding: ASCII
      - id: location
        type: str
        size: 20
        encoding: ASCII
      - id: description
        type: str
        size: 20
        encoding: ASCII
      - id: url
        type: str
        size: 124
        encoding: ASCII
      - id: software_id
        type: str
        size: 40
        encoding: ASCII
      - id: package_id
        type: str
        encoding: ASCII
        size: 40
      - id: unparsed_data
        size-eos: true
        type: str
        encoding: ASCII
  type_repeater_options:
    seq:
      - id: repeater_id
        type: u4
      - id: options
        type: str
        encoding: ASCII
        size-eos: true
        doc: structure probably key=value;key=value;...
instances:
  fifth_letter:
    pos: 4
    type: str
    encoding: ASCII
    size: 1
seq:
  - id: command_prefix
    type: str
    encoding: UTF-8
    size: 4
  - id: command_data
    type:
      switch-on: command_prefix
      cases:
        '"RPTL"': type_repeater_login_request
        '"MSTN"': type_master_not_accept
        '"MSTA"': type_master_repeater_ack
        '"RPTK"': type_repeater_login_response
        '"MSTP"': type_master_ping
        '"RPTP"': type_repeater_pong
        '"RPTC"': type_repeater_configuration_or_closing
        '"MSTC"': type_master_closing
        '"DMRD"': type_dmr_data