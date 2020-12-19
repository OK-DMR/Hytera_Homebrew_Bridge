meta:
  id: gpsdata
seq:
  - id: gps_status
    size: 1
    doc: A=gps available/locked, V=gps unavailable/no data
  - id: gps_time
    size: 6
    doc: GMT format HHMMSS
  - id: gps_date
    size: 6
    doc: format DDMMYY
  - id: north_south
    size: 1
    doc: letter N or S
  - id: latitude
    size: 9
    doc: DDMM.MMMM D=degree(0-90) M=minute(0-59.9999)
  - id: east_west
    size: 1
    doc: letters E or W
  - id: longitude
    size: 10
    doc: DDDMM.MMMM D=degree(0-180) M=minute(0-59.9999)
  - id: speed
    size: 2
    doc: speed in knots, eg. 0.2
  - id: direction
    size: 3
    doc: azimuth(0-359), 0=north, increase is clockwise