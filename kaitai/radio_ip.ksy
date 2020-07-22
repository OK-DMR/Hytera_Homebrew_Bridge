meta:
  id: radio_ip
doc: |
  represented as 4 bytes, each byte interpreted as number (0-255)
  10.0.0.80 means the subnet is set to 10.x.x.x (C) and radio ID is 80
  10.22.0.0 means the subnet is set to 10.x.x.x (C) and radio ID is 2200
instances:
  radio_id:
    value: radio_id_1.to_s + radio_id_2.to_s + radio_id_3.to_s
seq:
  - id: subnet
    type: u1
  - id: radio_id_1
    type: u1
  - id: radio_id_2
    type: u1
  - id: radio_id_3
    type: u1