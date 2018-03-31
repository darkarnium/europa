''' Defines exceptions for use throughout V1 of The Europa project API. '''

from flask import jsonify

from europa.api.v1 import router


class EndpointNotImplemented(Exception):
    ''' Implements an exception for handling not implemented endpoints. '''
    pass

@router.app_errorhandler(EndpointNotImplemented)
def handle_endpoint_not_implemented(_):
    ''' Provides a Flask handler for EndpointNotImplemented exceptions. '''
    response = jsonify({'Error': 'Not yet implemented'})
    response.status_code = 501
    return response


class InternalServerError(Exception):
    ''' Implements an exception for handling internal server errors. '''
    pass

@router.app_errorhandler(InternalServerError)
def handle_internal_server_error(message):
    ''' Provides a Flask handler for InternalServerError exceptions. '''
    response = jsonify({'Error': 'Internal server error: {}'.format(message)})
    response.status_code = 500
    return response


class InvalidClientRequest(Exception):
    ''' Implements an exception for handling Invalid client requests. '''
    pass

@router.app_errorhandler(InvalidClientRequest)
def handle_invalid_client_request(message):
    ''' Provides a Flask handler for InvalidClientRequest exceptions. '''
    response = jsonify({'Error': 'Invalid request: {}'.format(message)})
    response.status_code = 400
    return response
