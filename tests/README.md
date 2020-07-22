# tests

run tests directly in this folder, like
```console
foo@bar:~$ python3 lp_test.py
----------
data/location_protocol.standard_answer.bin
3316221
{'_m_opcode_header_int': <LpSpecificTypes.standard_answer: 40962>,
 'data': {'gpsdata': {'direction': b'112',
                      'east_west': b'E',
                      'gps_date': b'261015',
                      'gps_status': b'A',
                      'gps_time': b'183648',
                      'latitude': b'4718.8051',
                      'longitude': b'01854.4387',
                      'north_south': b'N',
                      'speed': b'0.'},
          'radio_ip': {'_m_radio_id': '3316221',
                       'radio_id_1': 33,
                       'radio_id_2': 16,
                       'radio_id_3': 221,
                       'subnet': 10},
          'request_id': 1,
          'result': <ResultCodes.ok: 0>},
 'message_length': 50,
 'opcode_header': b'\xa0\x02'}

```
