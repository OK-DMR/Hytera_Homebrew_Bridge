meta:
  id: radio_id
doc: |
  represented as 3 bytes, each byte interpreted as number (0-255)
instances:
  radio_id:
    value: radio_id_1.to_s + radio_id_2.to_s + radio_id_3.to_s
seq:
  - id: radio_id_1
    type: u1
  - id: radio_id_2
    type: u1
  - id: radio_id_3
    type: u1