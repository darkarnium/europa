''' Version 1 Vessel endpoints of the Europa project API. '''

import datetime
import sqlalchemy

from flask import g
from flask import jsonify
from flask import request

from europa.models import db
from europa.models import Vessel
from europa.models import VesselSize

from europa.api.v1 import decorators
from europa.api.v1 import exceptions

from europa.api.v1 import router


@router.route('/vessel', methods=['GET'])
def retrieve_vessels():
    ''' Attempt to retrive vessels the user is authorised to access. '''
    candidates = Vessel.query.filter(
        Vessel.deleted == None,
    ).all()

    # Construct a JSON friendly response.
    vessels = [candidate.for_json() for candidate in candidates]
    return jsonify(vessels)

@router.route('/vessel', methods=['POST'])
@decorators.validated(fields=['name', 'location'])
def create_vessel():
    ''' Attempt to create a vessel. '''
    document = request.get_json()

    # Create a new project from the provided payload.
    candidate = Vessel(
        name=document.get('name'),
        size=VesselSize.POT_TWELVE_CM,
        location=document.get('location'),
    )
    db.session.add(candidate)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to create vessel')

    # Return the newly created vessel to the user.
    # TODO: Perhaps reference the account in the HTTP 'Location' header, rather
    #       than returning a body on the HTTP 201?
    response = jsonify(candidate.for_json())
    response.status_code = 201
    return response


@router.route('/vessel/<int:vessel_id>', methods=['GET'])
def retrieve_vessel(vessel_id):
    ''' Attempt to retrieve a given vessel. '''
    candidate = Vessel.query.filter(
        Vessel.id == vessel_id,
    ).first_or_404()

    # Return the given vessel to the user.
    response = jsonify(candidate.for_json())
    response.status_code = 200
    return response


@router.route('/vessel/<int:vessel_id>', methods=['PUT'])
@decorators.validated(fields=['name', 'location'], optional=True)
def update_vessel(vessel_id):
    ''' Attempt to update a given vessel. '''
    candidate = Vessel.query.filter(
        Vessel.id == vessel_id,
    ).first_or_404()

    # Map in all fields that can be modified.
    document = request.get_json()
    if document.get('name'):
        candidate.name = document.get('name')
    if document.get('location'):
        candidate.location = document.get('location')

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to update vessel')

    # Confirm update with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response


@router.route('/vessel/<int:vessel_id>', methods=['DELETE'])
def delete_vessel(vessel_id):
    ''' Attempt to delete a given project. '''
    candidate = Vessel.query.filter(
        Vessel.id == vessel_id,
        Vessel.deleted == None,
    ).first_or_404()

    # Mark deleted.
    candidate.deleted = datetime.datetime.utcnow()

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise exceptions.InternalServerError('Unable to delete vessel')

    # Confirm deletion with an HTTP 204.
    response = jsonify()
    response.status_code = 204
    return response
