import os
import json
import time
import socket
import requests
import datetime
import logging
import logging.config

import RPi.GPIO as GPIO
import Adafruit_DHT as DHT
import w1thermsensor as W1
import pyHS100 as SmartHome

# Define, in seconds, how long between polling intervals.
SLEEP_INTERVAL = 300

# Define IP addresses for external sensors.
SENSOR_IP_LIGHT = '192.0.2.0'

# Define pin numbers for GPIO reads.
SENSOR_PIN_SOIL = 2
SENSOR_PIN_AMBIENT = 3

# Define API sensor IDs.
API_SOIL_MOISTURE = 1
API_SOIL_TEMPERATURE = 2
API_AMBIENT_HUMIDITY = 3
API_AMBIENT_TEMPERATURE = 4
API_LIGHT_STATE = 5

# Define API endpoint.
API_BASE_URI = 'http://127.0.0.1:5000/v1'


def get_ambient_all():
    ''' Provides a helper to get all data from the ambient sensor. '''
    AMBIENT_SENSOR_TYPE = DHT.AM2302
    return DHT.read_retry(AMBIENT_SENSOR_TYPE, SENSOR_PIN_AMBIENT)


def get_ambient_temperature():
    ''' Provides a helper to get the ambient temperature. '''
    _, temperature = get_ambient_all()
    return temperature


def get_ambient_humidity():
    ''' Provides a helper to get the ambient humidity. '''
    humidity, _ = get_ambient_all()
    return humidity


def get_soil_temperature():
    ''' Provides a helper to get the soil temperature. '''
    sensor = W1.W1ThermSensor()
    return sensor.get_temperature()


def get_soil_moisture_state():
    ''' Provides a helper to get the soil moisture state (boolean). '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN_SOIL, GPIO.IN)

    # Change the output from Boolean to Binary. Where 1.0 is 'moisture required'
    # and 0.0 is 'moisture not required'.
    if not GPIO.input(SENSOR_PIN_SOIL):
        return 0.0
    else:
        return 1.0


def get_light_state():
    ''' Provides a helper to get the external light state (boolean). '''
    plug = SmartHome.SmartPlug(SENSOR_IP_LIGHT)

    # Where 0.0 is 'Light Off' and 1.0 is 'Light On'.
    if plug.get_sysinfo()['relay_state'] == 0:
        return 0.0
    else:
        return 1.0


def post_sensor_data(api_sensor_id, capture_time, value):
    ''' Provide a helper to POST sensor data to the API. '''
    # The captured time is submitted to the API 
    payload = json.dumps({
        'value': value,
        'created': capture_time,
    })

    # Don't catch exceptions, let our caller do that.
    requests.post(
        '{0}/sensor/{1}/data'.format(API_BASE_URI, api_sensor_id),
        data=payload,
        headers={
            'Content-Type': 'application/json'
        }
    )


def main():
    ''' Provides the main acquisition loop. '''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - [%(levelname)s] %(message)s'
    )
    log = logging.getLogger(__name__)

    # Print external sensor IPs.
    log.info('External light sensor configured as IP %s', SENSOR_IP_LIGHT)

    # Print GPIO pinout.
    log.info('Soil sensor configured as GPIO pin %s', SENSOR_PIN_SOIL)
    log.info('Ambient sensor configured as GPIO pin %s', SENSOR_PIN_AMBIENT)

    # Poll until heat-death of the universe... Or, y'know, until we crash.
    log.info('Entering polling loop')
    while True:
        # Standardise the capture time between all sensors. This is technically
        # incorrect, but hey, we're not that worried about timing precision.
        capture_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')

        # This doesn't need to be initialised every loop, but for simplicity
        # we'll keep it here.
        sensors = []
        sensors.append({
            'id': API_SOIL_MOISTURE, 
            'value': get_soil_moisture_state(),
            'name': 'Soil Moisture',
        })
        sensors.append({
            'id': API_SOIL_TEMPERATURE, 
            'value': get_soil_temperature(),
            'name': 'Soil Temperature',
        })
        sensors.append({
            'id': API_AMBIENT_HUMIDITY, 
            'value': get_ambient_humidity(),
            'name': 'Ambient Humidity',
        })
        sensors.append({
            'id': API_AMBIENT_TEMPERATURE, 
            'value': get_ambient_temperature(),
            'name': 'Ambient Temperature',
        })
        sensors.append({
            'id': API_LIGHT_STATE, 
            'value': get_light_state(),
            'name': 'Light State',
        })

        # Poll each sensor and report to the API.
        for sensor in sensors:
            try:
                log.info(
                    "Submitting '%s' for sensor '%s' to API",
                    sensor['value'],
                    sensor['name']
                )
                post_sensor_data(sensor['id'], capture_time, sensor['value'])
            except requests.exceptions.RequestException as err:
                log.error('Failed to POST sensor data: %s', err)

        # Sleep for the next run.
        log.info('Sleeping %s before the next poll', SLEEP_INTERVAL)
        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    main()
