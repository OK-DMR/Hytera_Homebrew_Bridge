meta:
  id: ip_site_connect_heartbeat
  endian: le
doc: |
  Hytera IP Multi-Site Connect Protocol heartbeat packet, either simple KEEPALIVE/UP or PING/PONG
types:
  keepalive:
    seq:
      - id: nullbyte
        contents: [0x00]
  ping_pong:
    seq:
      - id: header
        contents: 'ZZZZ'
      - id: heartbeat_identitier
        contents: [0x0a, 0x00, 0x00, 0x00, 0x14]
      - id: nullbytes
        contents: [0x00, 0x00, 0x00]
      - id: heartbeat_seq
        type: u1
        doc: |
          raise this byte by one on response
      - id: tail
        contents: [0x5a, 0x59, 0x5a, 0x00, 0x00, 0x00, 0x00]
  unknown:
    seq:
      - id: data
        size-eos: true
seq:
  - id: data
    type:
      switch-on: _io.size
      cases:
        1: keepalive
        20: ping_pong
        _: unknown