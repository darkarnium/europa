''' Version 1 Plant endpoints of the Europa project API. '''

import datetime
import sqlalchemy

from flask import g
from flask import jsonify
from flask import request

from europa.models import db
from europa.models import Plant
from europa.models import Vessel

from europa.api.v1 import decorators
from europa.api.v1 import exceptions

from europa.api.v1 import router


@router.route('/plants', methods=['GET'])
def retrieve_plants():
    ''' Attempt to retrive plants the user is authorised to access. '''
    candidates = Plant.query.filter(
        Plant.deleted == None,
    ).all()

    # Construct a JSON friendly response.
    plants = [candidate.for_json() for candidate in candidates]
    return jsonify(plants)

@router.route('/plant', methods=['POST'])
@decorators.validated(fields=['name', 'vessel', 'description'])
def create_plant():
    ''' Attempt to create a plant. '''
    document = request.get_json()

    # Ensure the provided vessel exists, or 404.
    vessel = Vessel.query.filter(
        Vessel.id == document.get('vessel'),
    ).first_or_404()

    # Create a new plant from the provided payload.
    candidate = Plant(
        name=document.get('name'),
        vessel_id=vessel.id,
        description=document.get('description'),
    )
    db.session.add(candidate)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to create plant')

    # Return the newly created vessel to the user.
    # TODO: Perhaps reference the account in the HTTP 'Location' header, rather
    #       than returning a body on the HTTP 201?
    response = jsonify(candidate.for_json())
    response.status_code = 201
    return response


@router.route('/plant/<int:plant_id>', methods=['GET'])
def retrieve_plant(plant_id):
    ''' Attempt to retrieve a given plant. '''
    candidate = Plant.query.filter(
        Plant.id == plant_id,
    ).first_or_404()

    # Return the given plant to the user.
    response = jsonify(candidate.for_json())
    response.status_code = 200
    return response


@router.route('/plant/<int:plant_id>', methods=['PUT'])
@decorators.validated(fields=['name', 'description', 'vessel'], optional=True)
def update_plant(plant_id):
    ''' Attempt to update a given plant. '''
    candidate = Plant.query.filter(
        Plant.id == plant_id,
    ).first_or_404()

    # Map in all fields that can be modified.
    document = request.get_json()
    if document.get('name'):
        candidate.name = document.get('name')
    if document.get('description'):
        candidate.description = document.get('description')
    
    # Ensure the provided vessel exists, or 404.
    if document.get('vessel'):
        _ = Vessel.query.filter(
            Vessel.id == document.get('vessel'),
        ).first_or_404()
        candidate.vessel_id = document.get('vessel')

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to update plant')

    # Confirm update with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response


@router.route('/plant/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    ''' Attempt to delete a given plant. '''
    candidate = Plant.query.filter(
        Plant.id == plant_id,
        Plant.deleted == None,
    ).first_or_404()

    # Mark deleted.
    candidate.deleted = datetime.datetime.utcnow()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to delete plant')

    # Confirm deletion with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response
