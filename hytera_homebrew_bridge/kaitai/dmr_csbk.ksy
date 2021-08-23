meta:
  id: dmr_csbk
  endian: le
doc: |
  TS 102 361-2 V2.3.1 CSBK decoding
enums:
  csbko_types:
    0b111000: bs_outbound_activation_csbk_pdu
    0b000100: unit_to_unit_voice_service_request
    0b000101: unit_to_unit_voice_service_answer_response
    0b100110: negative_acknowledge_response
    0b111101: preamble
    0b000111: channel_timing
  csbk_data_or_csbk:
    0: csbk_content_follows_preambles
    1: data_content_follows_preambles
  csbk_group_or_individual:
    0: target_address_is_an_individual
    1: target_address_is_a_group
seq:
  - id: last_block
    type: b1
    doc: LB
  - id: protect_flag
    type: b1
    doc: PF
  - id: csbk_opcode
    type: b6
    doc: CSBKO
    enum: csbko_types
  - id: feature_set_id
    type: b8
    doc: FID
  - id: preamble_data_or_csbk
    type: b1
    if: csbk_opcode == csbko_types::preamble
    enum: csbk_data_or_csbk
  - id: preamble_group_or_individual
    type: b1
    enum: csbk_group_or_individual
    if: csbk_opcode == csbko_types::preamble
  - id: preamble_reserved_1
    type: b6
  - id: preamble_csbk_blocks_to_follow
    type: b8
  - id: preamble_target_address
    type: b24
  - id: preamble_source_address
    type: b24