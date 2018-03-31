''' Version 1 Sensor Data endpoints of the Europa project API. '''

import datetime
import sqlalchemy

from flask import g
from flask import jsonify
from flask import request

from europa.models import db
from europa.models import Sensor
from europa.models import SensorData

from europa.api.v1 import decorators
from europa.api.v1 import exceptions

from europa.api.v1 import router


@router.route('/sensor/<int:sensor_id>/data', methods=['POST'])
@decorators.validated(fields=['value'])
def create_sensor_data(sensor_id):
    ''' Attempt to create a new sensor data entry. '''
    sensor = Sensor.query.filter(
        Sensor.id == sensor_id,
        Sensor.deleted == None,
    ).first_or_404()

    # Ensure the sensor value is in the correct format.
    document = request.get_json()
    value = document.get('value')
    if type(value) != float:
        raise exceptions.InvalidClientRequest('Value must be a float!')

    # Create a new sensor data entry from the provided payload.
    candidate = SensorData(value=value, sensor_id=sensor.id)
    db.session.add(candidate)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to create sensor data')

    # Confirm addition with an HTTP 201.
    response = jsonify()
    response.status_code = 201
    return response


@router.route('/sensor/<int:sensor_id>/data', methods=['GET'])
def retrieve_sensor_data(sensor_id):
    ''' Attempt to retrieve data for a given sensor. '''
    candidates = SensorData.query.filter(
        sensor_id == sensor_id,
        Sensor.deleted == None,
        SensorData.created >= (
            datetime.datetime.utcnow() - datetime.timedelta(days=1)
        )
    ).all()

    # Construct a JSON friendly response.
    sensors = [candidate.for_json() for candidate in candidates]
    return jsonify(sensors)
