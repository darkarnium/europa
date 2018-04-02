''' Version 1 Sensor Category endpoints of the Europa project API. '''

import datetime
import sqlalchemy

from flask import g
from flask import jsonify
from flask import request

from europa.models import db
from europa.models import SensorCategory

from europa.api.v1 import decorators
from europa.api.v1 import exceptions

from europa.api.v1 import router


@router.route('/sensor/category', methods=['POST'])
@decorators.validated(fields=['name', 'units'])
def create_sensor_category():
    ''' Attempt to create a sensor category. '''
    document = request.get_json()

    # Create a new sensor category from the provided payload.
    candidate = SensorCategory(
        name=document.get('name'),
        units=document.get('units'),
    )
    db.session.add(candidate)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to create sensor category')

    # Return the newly created sensor category to the user.
    # TODO: Perhaps reference the account in the HTTP 'Location' header, rather
    #       than returning a body on the HTTP 201?
    response = jsonify(candidate.for_json())
    response.status_code = 201
    return response


@router.route('/sensor/categories', methods=['GET'])
def retrieve_sensor_categories():
    ''' Attempt to retrive sensor cagegories the user can access. '''
    candidates = SensorCategory.query.filter(
        SensorCategory.deleted == None,
    ).order_by(SensorCategory.id).all()

    # Construct a JSON friendly response.
    categories = [candidate.for_json() for candidate in candidates]
    return jsonify(categories)


@router.route('/sensor/category/<int:sensor_category_id>', methods=['GET'])
def retrieve_sensor_category(sensor_category_id):
    ''' Attempt to retrieve a given sensor category. '''
    candidate = SensorCategory.query.filter(
        SensorCategory.id == sensor_category_id,
    ).first_or_404()

    # Return the given sensor to the user.
    response = jsonify(candidate.for_json())
    response.status_code = 200
    return response


@router.route('/sensor/category/<int:sensor_category_id>', methods=['PUT'])
@decorators.validated(fields=['name', 'units'], optional=True)
def update_sensor_category(sensor_category_id):
    ''' Attempt to update a given sensor. '''
    candidate = SensorCategory.query.filter(
        SensorCategory.id == sensor_category_id,
    ).first_or_404()

    # Map in all fields that can be modified.
    document = request.get_json()
    if document.get('name'):
        candidate.name = document.get('name')
    if document.get('units'):
        candidate.units = document.get('units')
   
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to update sensor category')

    # Confirm update with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response


@router.route('/sensor/category/<int:sensor_category_id>', methods=['DELETE'])
def delete_sensor_category(sensor_category_id):
    ''' Attempt to delete a given sensor category. '''
    candidate = SensorCategory.query.filter(
        SensorCategory.id == sensor_category_id,
        SensorCategory.deleted == None,
    ).first_or_404()

    # Mark deleted.
    candidate.deleted = datetime.datetime.utcnow()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to delete sensor category')

    # Confirm deletion with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response
