''' Version 1 Sensor endpoints of the Europa project API. '''

import datetime
import sqlalchemy

from flask import g
from flask import jsonify
from flask import request

from europa.models import db
from europa.models import Plant
from europa.models import Vessel
from europa.models import Sensor
from europa.models import SensorCategory
from europa.models import SensorData

from europa.api.v1 import decorators
from europa.api.v1 import exceptions

from europa.api.v1 import router


@router.route('/sensor', methods=['POST'])
@decorators.validated(fields=['name', 'vessel', 'category'])
def create_sensor():
    ''' Attempt to create a sensor. '''
    document = request.get_json()

    # Ensure the provided vessel exists, or 404.
    _ = Vessel.query.filter(
        Vessel.id == document.get('vessel'),
    ).first_or_404()

    # Ensure the provided category exists, or 404.
    _ = SensorCategory.query.filter(
        SensorCategory.id == document.get('category'),
    ).first_or_404()

    # Create a new plant from the provided payload.
    candidate = Sensor(
        name=document.get('name'),
        vessel_id=document.get('vessel'),
        category_id=document.get('category'),
    )
    db.session.add(candidate)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to create sensor')

    # Return the newly created vessel to the user.
    # TODO: Perhaps reference the account in the HTTP 'Location' header, rather
    #       than returning a body on the HTTP 201?
    response = jsonify(candidate.for_json())
    response.status_code = 201
    return response


@router.route('/sensors', methods=['GET'])
def retrieve_sensors():
    ''' Attempt to retrive sensors the user is authorised to access. '''
    candidates = Sensor.query.filter(
        Sensor.deleted == None,
    ).order_by(Sensor.id).all()

    # Construct a JSON friendly response.
    sensors = [candidate.for_json() for candidate in candidates]
    return jsonify(sensors)


@router.route('/sensor/<int:sensor_id>', methods=['GET'])
def retrieve_sensor(sensor_id):
    ''' Attempt to retrieve a given sensor. '''
    candidate = Sensor.query.filter(
        Sensor.id == sensor_id,
    ).first_or_404()

    # Return the given sensor to the user.
    response = jsonify(candidate.for_json())
    response.status_code = 200
    return response


@router.route('/sensor/<int:sensor_id>', methods=['PUT'])
@decorators.validated(fields=['name', 'vessel', 'category'], optional=True)
def update_sensor(sensor_id):
    ''' Attempt to update a given sensor. '''
    candidate = Sensor.query.filter(
        Sensor.id == sensor_id,
    ).first_or_404()

    # Map in all fields that can be modified.
    document = request.get_json()
    if document.get('name'):
        candidate.name = document.get('name')

    # Ensure the provided category exists, or 404.
    if document.get('category'):
        _ = SensorCategory.query.filter(
            SensorCategory.id == document.get('category'),
        ).first_or_404()
        candidate.category_id = document.get('category')

    # Ensure the provided vessel exists, or 404.
    if document.get('vessel'):
        _ = Vessel.query.filter(
            Vessel.id == document.get('vessel'),
        ).first_or_404()
        candidate.vessel_id = document.get('vessel')

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to update sensor')

    # Confirm update with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response


@router.route('/sensor/<int:sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    ''' Attempt to delete a given sensor. '''
    candidate = Sensor.query.filter(
        Sensor.id == sensor_id,
        Sensor.deleted == None,
    ).first_or_404()

    # Mark deleted.
    candidate.deleted = datetime.datetime.utcnow()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to delete sensor')

    # Confirm deletion with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response
