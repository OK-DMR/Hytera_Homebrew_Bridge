meta:
  id: dmr_data_header
  endian: le
doc: |
  TS 102 361-1 V2.5.1 Data Header
enums:
  data_packet_formats:
    0b0000: unified_data_transport
    0b0001: response_packet
    0b0010: data_packet_unconfirmed
    0b0011: data_packet_confirmed
    0b1101: short_data_defined
    0b1110: short_data_raw_or_status_or_precoded
    0b1111: proprietary
  sap_identifiers:
    0b0000: unified_data_transport
    0b0010: tcp_ip_header_compression
    0b0011: udp_ip_header_compression
    0b0100: ip_based_packet_data
    0b0101: arp_address_resolution_protocol
    0b1001: proprietary_packet_data
    0b1010: short_data
  udt_formats:
    0b0000: binary
    0b0001: ms_or_tg_address
    0b0010: bcd_4bit
    0b0011: iso_7bit_coded_characters
    0b0100: iso_8bit_coded_characters
    0b0101: nmea_location_coded
    0b0110: ip_address
    0b0111: unicode_16bit_characters
    0b1000: manufacturer_specific
    0b1001: manufacturer_specific_2
    0b1010: mixed_address_and_16bit_utf16be_characters
  udt_opcodes:
    0b110000: pv_grant
    0b110001: tv_grant
    0b110010: btv_grant
    0b110011: pd_grant
    0b110100: td_grant
    0b110101: pv_grant_dx
    0b110110: pd_grant_dx
    0b110111: pd_grant_mi
    0b111000: td_grant_mi
    0b111001: c_move
    0b011001: c_aloha
    0b101000: c_bcast
    0b101110: p_clear
    0b101111: p_protect
    0b011100: c_or_p_ahoy
    0b100000: c_ackd
    0b100001: c_acku
    0b100010: p_ackd
    0b100011: p_acku
    0b011010: c_udthd
    0b011011: c_udthu
    0b100100: c_dgnahd
    0b100101: c_dgnahu
    0b011111: c_rand
    0b011110: c_ackvit
    0b101010: p_maint
types:
  data_undefined:
    seq:
      - id: bytedata
        size-eos: true
  data_proprietary:
    doc: 9.2.9 Proprietary Header (P_HEAD) PDU
    seq:
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: format
        type: b4
        enum: data_packet_formats
      - id: mfid
        doc: manufacturer's id
        type: b8
      - id: proprietary_data
        size: 8
        doc: 64bits / 8bytes of proprietary data
      - id: crc
        size: 2
  data_udt:
    doc: 9.2.13 Unified Data Transport Header (UDT_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
        doc: 0b0 expected
      - id: reserved1
        type: b2
        doc: See ETSI TS 102 361-4 [11] clause 7.1.1.1.8 and 7.1.1.2.4 for information elements and values
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: udt_format
        type: b4
        enum: udt_formats
        doc: ETSI TS 102 361-4 V1.9.1, 7.2.27 UDT Format
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: pad_nibble
        type: b5
      - id: reserved2
        type: b1
      - id: appended_blocks
        type: b2
      - id: supplementary_flag
        type: b1
      - id: protect_flag
        type: b1
      - id: udt_opcode
        type: b6
        enum: udt_opcodes
        doc: ETSI TS 102 361-4 V1.2.1, Annex B, B.1 CSBK/MBC/UDT Opcode List
      - id: crc
        size: 2
  data_response:
    doc: 9.2.4 Confirmed Response packet Header (C_RHEAD) PDU
    seq:
      - id: reserved1
        type: b1
        doc: 0b0 expected
      - id: response_requested
        type: b1
        doc: 0b0 expected
      - id: reserved2
        type: b2
        doc: 0b00 expected
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: reserved3
        type: b4
        doc: 0b0000 expected
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: full_message_flag
        type: b1
        doc: 0b0 expected
      - id: blocks_to_follow
        type: b7
      - id: response_class
        type: b2
      - id: response_type
        type: b3
      - id: response_status
        type: b3
      - id: crc
        size: 2
  data_unconfirmed:
    doc: 9.2.6 Unconfirmed data packet Header (U_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
        doc: 0b0 expected
      - id: reserved1
        type: b1
        doc: 0b0 expected
      - id: pad_octet_count_msb
        type: b1
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: pad_octet_count
        type: b4
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: full_message_flag
        type: b1
      - id: blocks_to_follow
        type: b7
      - id: reserved2
        type: b4
        doc: 0b0000 expected
      - id: fragment_sequence_number
        type: b4
      - id: crc
        size: 2
  data_confirmed:
    doc: 9.2.1 Confirmed packet Header (C_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
      - id: reserved1
        type: b1
        doc: 0b0 expected
      - id: pad_octet_count_msb
        type: b1
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: pad_octet_count
        type: b4
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: full_message_flag
        type: b1
      - id: blocks_to_follow
        type: b7
      - id: resynchronize_flag
        type: b1
      - id: send_sequence_number
        type: b3
      - id: fragment_sequence_number
        type: b4
      - id: crc
        size: 2
  data_short_raw:
    doc: 9.2.11 Raw short data packet Header (R_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
      - id: appended_blocks_msb
        type: b2
        doc: 0b00 expected
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: appended_blocks_lsb
        type: b4
        doc: 0b0000 expected
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: source_port
        type: b3
      - id: destination_port
        type: b3
      - id: selective_automatic_repeat_request
        doc: SARQ
        type: b1
      - id: full_message_flag
        type: b1
      - id: bit_padding
        type: b8
        doc: 0b00000000 expected
      - id: crc
        size: 2
  data_short_defined:
    doc: 9.2.12 Defined Data short data packet Header (DD_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
      - id: appended_blocks_msb
        type: b2
        doc: 0b00 expected
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: appended_blocks_lsb
        type: b4
        doc: 0b0000 expected
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: defined_data
        type: b6
        doc: data format
      - id: selective_automatic_repeat_request
        doc: SARQ
        type: b1
      - id: full_message_flag
        type: b1
      - id: bit_padding
        type: b8
      - id: crc
        size: 2
  data_short_status_precoded:
    doc: 9.2.10 Status/Precoded short data packet Header (SP_HEAD) PDU
    seq:
      - id: llid_destination_is_group
        type: b1
      - id: response_requested
        type: b1
      - id: appended_blocks_msb
        type: b2
        doc: 0b00 expected
      - id: format
        type: b4
        enum: data_packet_formats
      - id: sap_identifier
        type: b4
        enum: sap_identifiers
      - id: appended_blocks_lsb
        type: b4
        doc: 0b0000 expected
      - id: llid_destination
        type: b24
      - id: llid_source
        type: b24
      - id: source_port
        type: b3
      - id: destination_port
        type: b3
      - id: status_precoded
        type: b10
      - id: crc
        size: 2
seq:
  - id: skip4
    type: b4
  - id: data_packet_format
    doc: Data packet format / identification, section 9.3.17
    type: b4
    enum: data_packet_formats
instances:
  data:
    io: _root._io
    pos: 0
    size: 12
    type:
      switch-on: data_packet_format
      cases:
        'data_packet_formats::unified_data_transport': data_udt
        'data_packet_formats::response_packet': data_response
        'data_packet_formats::data_packet_unconfirmed': data_unconfirmed
        'data_packet_formats::data_packet_confirmed': data_confirmed
        'data_packet_formats::short_data_defined': data_short_defined
        'data_packet_formats::short_data_raw_or_status_precoded': data_short_status_precoded
        'data_packet_formats::proprietary': data_proprietary
        _: data_undefined