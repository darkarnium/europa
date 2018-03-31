''' Implements tests for Europa Models. '''

import uuid
import json
import unittest
import coverage

from europa import initialize_all

from europa.models import db
from europa.models import Vessel
from europa.models import VesselSize
from europa.models import Plant
from europa.models import Sensor
from europa.models import SensorData
from europa.models import SensorUnits
from europa.models import SensorCategory


class EuropaModelTestCase(unittest.TestCase):
    ''' Defines tests for Europa Models. '''

    def setUp(self):
        ''' Ensure the application, and database, is setup for testing. '''
        self.application = initialize_all()
        self.client = self.application.test_client()

        # Create the database and commit all objects.
        with self.application.app_context():
            # Seed the database with a valid vessel.
            vessel = Vessel(
                id=1337,
                name=str(uuid.uuid4()),
                size=VesselSize.POT_TWELVE_CM,
                location='Some Location',
            )
            db.session.add(vessel)

            # Seed the database with a valid plant.
            plant = Plant(
                id=1337,
                name=str(uuid.uuid4()),
                vessel_id=1337,
                description='Some Description',
            )
            db.session.add(plant)

            # Create the test database and save fixtures.
            db.create_all()
            db.session.commit()

    def tearDown(self):
        ''' Ensure the database is torn down between tests. '''
        with self.application.app_context():
            db.drop_all()

    def test_create_vessel(self):
        ''' Ensures that a vessel can be created via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'location': 'Some New Location'
        })
        response = self.client.post(
            '/v1/vessel',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_vessels(self):
        ''' Ensures that vessels can be retrieved via the API. '''
        response = self.client.get(
            '/v1/vessel',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_vessel(self):
        ''' Ensures that a specific vessel can be retrieved via the API. '''
        response = self.client.get(
            '/v1/vessel/1337',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_update_vessel(self):
        ''' Ensures that a specified vessel can be updated via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'location': 'Some Updated Location',
        })
        response = self.client.put(
            '/v1/vessel/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_vessel(self):
        ''' Ensures that a specific vessel can be deleted via the API. '''
        response = self.client.delete(
            '/v1/vessel/1337',
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_create_plant(self):
        ''' Ensures that a plant can be created via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'vessel': 1337,
            'description': 'Some Description'
        })
        response = self.client.post(
            '/v1/plant',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_plants(self):
        ''' Ensures that plants can be retrieved via the API. '''
        response = self.client.get(
            '/v1/plants',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_plant(self):
        ''' Ensures that a specific plant can be retrieved via the API. '''
        response = self.client.get(
            '/v1/plant/1337',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_update_plant(self):
        ''' Ensures that a specified plant can be updated via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'description': 'Some Updated Description',
        })
        response = self.client.put(
            '/v1/plant/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_plant(self):
        ''' Ensures that a specific plant can be deleted via the API. '''
        response = self.client.delete(
            '/v1/plant/1337',
            content_type='application/json',
        )
        assert response.status_code == 204

if __name__ == '__main__':
    unittest.main()
