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

### Initial Setup

In order to use the Poller, sensors must already have been setup in the API.
A few Curl commands have been included below, which can be used to ensure that
the API has been setup as the Poller will expect. This only needs to be
performed ONCE.

```
# Setup a new Vessel.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "pot1", "location": "Kitchen"}' \
  http://127.0.0.1:5000/v1/vessel

# Setup a new Plant.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Sweet Basil", "vessel": 1, "description": "Left-Most Pot"}' \
  http://127.0.0.1:5000/v1/plant

# Setup a new temperature sensor category.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Temperature", "units": "°C"}' \
  http://127.0.0.1:5000/v1/sensor/category

# Setup a new moisture sensor category.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Moisture", "units": "Is Required"}' \
  http://127.0.0.1:5000/v1/sensor/category

# Setup a new humidity sensor category.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Humidity", "units": "%"}' \
  http://127.0.0.1:5000/v1/sensor/category

# Setup a new Soil Moisture sensor.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Soil", "category": 2, "vessel": 1}' \
  http://127.0.0.1:5000/v1/sensor

# Setup a new Soil Temperature sensor.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Soil", "category": 1, "vessel": 1}' \
  http://127.0.0.1:5000/v1/sensor

# Setup a new Ambient Humidity sensor.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Ambient", "category": 3, "vessel": 1}' \
  http://127.0.0.1:5000/v1/sensor

# Setup a new Ambient Temperature sensor.
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name": "Ambient", "category": 1, "vessel": 1}' \
  http://127.0.0.1:5000/v1/sensor

```
