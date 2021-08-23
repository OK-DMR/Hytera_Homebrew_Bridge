meta:
  id: dmr_data
  endian: le
doc: |
  ETSI TS 102 361-1 V2.5.1, section 9.2, Data PDUs
types:
  rate_34_confirmed:
    doc: |
      9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11: R_3_4_DATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 16
  rate_34_unconfirmed:
    doc: |
      9.2.2 Rate ¾ coded packet Data (R_3_4_DATA) PDU, Table 9.11A: R_3_4_DATA PDU content for unconfirmed data
    seq:
      - id: user_data
        size: 18
  rate_34_last_block_confirmed:
    doc: |
      9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12: R_3_4_LDATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 12
      - id: message_crc32
        size: 4
  rate_34_last_block_unconfirmed:
    doc: |
      9.2.3 Rate ¾ coded Last Data block (R_3_4_LDATA) PDU, Table 9.12A: R_3_4_LDATA PDU content for unconfirmed data
    seq:
      - id: user_data
        size: 14
      - id: message_crc32
        size: 4
  rate_12_confirmed:
    doc: |
      9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15A: R_1_2_DATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 10
  rate_12_unconfirmed:
    doc: |
      9.2.7 Rate ½ coded packet Data (R_1_2_DATA) PDU, Table 9.15AA: R_1_2_DATA PDU content for unconfirmed data
    seq:
      - id: user_data
        size: 12
  rate_12_last_block_confirmed:
    doc: |
      9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 6
      - id: message_crc32
        size: 4
  rate_12_last_block_unconfirmed:
    doc: |
      9.2.8 Rate ½ coded Last Data block (R_1_2_LDATA) PDU, Table 9.15B: R_1_2_LDATA PDU content for confirmed data
    seq:
      - id: user_data
        size: 8
      - id: message_crc32
        size: 4
  udt_last_block:
    doc: |
      9.2.14 Unified Data Transport Last Data block (UDT_LDATA) PDU, Table 9.17E: UDT_LDATA PDU content
    seq:
      - id: user_data
        size: 10
      - id: message_crc16
        size: 2
  rate_1_confirmed:
    doc: |
      9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18: R_1_DATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 22
  rate_1_unconfirmed:
    doc: |
      9.2.15 Rate 1 coded packet Data (R_1_DATA) PDU, Table 9.18A: R_1_DATA PDU content for unconfirmed data
    seq:
      - id: user_data
        size: 24
  rate_1_last_block_confirmed:
    doc: |
      9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18B: R_1_LDATA PDU content for confirmed data
    seq:
      - id: data_block_serial_number
        type: b7
      - id: crc9
        type: b9
      - id: user_data
        size: 18
      - id: message_crc32
        size: 4
  rate_1_last_block_unconfirmed:
    doc: |
      9.2.16 Rate 1 coded Last Data block (R_1_LDATA) PDU, Table 9.18C: R_1_LDATA PDU content for unconfirmed data
    seq:
      - id: user_data
        size: 20
      - id: message_crc32
        size: 4