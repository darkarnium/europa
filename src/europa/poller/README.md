## Poller

This code is intended to provide a basic poller for fetching sensor readings
and pushing into the API.

### Dependencies

#### `RPi.GPIO`

The `RPi.GPIO` module is used to simplify Raspberry Pi GPIO reading.

#### `w1thermsensor`

The `w1thermsensor` module is used to simplify the 1-Wire reading.

#### `requests`

The `requests` module is used for HTTP operations against the API.

#### `Adafruit-DHT`

The `Adafruit-DHT` module is used to read sensor data from the AM2302. It should
be noted that `Adafruit-DHT` cannot be installed via PIP. This should instead be
installed from the GitHub source - via `python3 setup.py install`.
