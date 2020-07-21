meta:
  id: radio_ip
doc: |
  10.0.0.80 means the subnet is set to 10.x.x.x (C) and radio ID is 80
seq:
  - id: subnet
    type: u1
  - id: radio_id
    size: 3
    doc: |
      treat as 3 bytes that define radio ID such as 910099 91.00.99 (bytes 5B, 00, 63)
      maximum value of radio id is 255255255 (bytes FF, FF, FF)