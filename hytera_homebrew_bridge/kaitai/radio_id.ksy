meta:
  id: radio_id
  endian: le
doc: |
  represented as 3 bytes, each byte interpreted as number (0-255)
instances:
  radio_id:
    value: radio_id_raw >> 8
seq:
  - id: radio_id_raw
    type: u4le