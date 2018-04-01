''' Implements tests for Europa Models. '''

import uuid
import json
import datetime
import unittest
import coverage

from europa import initialize_all

from europa.models import db
from europa.models import Vessel
from europa.models import VesselSize
from europa.models import Plant
from europa.models import Sensor
from europa.models import SensorData
from europa.models import SensorCategory


class EuropaApiTestCase(unittest.TestCase):
    ''' Defines tests for Europa APi=I. '''

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

            # Seed the database with a valid sensor category.
            sensor_category = SensorCategory(
                id=1337,
                name=str(uuid.uuid4()),
                units='Boolean',
            )
            db.session.add(sensor_category)

            # Seed the database with a valid sensor.
            sensor = Sensor(
                id=1337,
                name=str(uuid.uuid4()),
                vessel_id=1337,
                category_id=1337,
            )
            db.session.add(sensor)

            # Seed the database with valid sensor data.
            sensor_data = SensorData(
                id=1337,
                value=1,
                sensor_id=1337,
            )
            db.session.add(sensor_data)

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
            '/api/v1/vessel',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_vessels(self):
        ''' Ensures that vessels can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/vessel',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_vessel(self):
        ''' Ensures that a specific vessel can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/vessel/1337',
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
            '/api/v1/vessel/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_vessel(self):
        ''' Ensures that a specific vessel can be deleted via the API. '''
        response = self.client.delete(
            '/api/v1/vessel/1337',
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
            '/api/v1/plant',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_plants(self):
        ''' Ensures that plants can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/plants',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_plant(self):
        ''' Ensures that a specific plant can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/plant/1337',
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
            '/api/v1/plant/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_plant(self):
        ''' Ensures that a specific plant can be deleted via the API. '''
        response = self.client.delete(
            '/api/v1/plant/1337',
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_create_sensor(self):
        ''' Ensures that a sensor can be created via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'category': 1337,
            'vessel': 1337,
        })
        response = self.client.post(
            '/api/v1/sensor',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_sensors(self):
        ''' Ensures that sensors can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/sensors',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_sensor(self):
        ''' Ensures that a specific sensor can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/sensor/1337',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_update_sensor(self):
        ''' Ensures that a specified sensor can be updated via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'category': 1337,
        })
        response = self.client.put(
            '/api/v1/sensor/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_sensor(self):
        ''' Ensures that a specific sensor can be deleted via the API. '''
        response = self.client.delete(
            '/api/v1/sensor/1337',
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_create_sensor_category(self):
        ''' Ensures that a sensor category can be created via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'units': 'Degrees',
        })
        response = self.client.post(
            '/api/v1/sensor/category',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_sensor_categories(self):
        ''' Ensures that sensors category can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/sensor/categories',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_retrieve_sensor_category(self):
        ''' Ensures that a specific sensor category can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/sensor/category/1337',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_update_sensor_category(self):
        ''' Ensures that a specified sensor category can be updated via the API. '''
        payload = json.dumps({
            'name': str(uuid.uuid4()),
            'units': 'Boolean',
        })
        response = self.client.put(
            '/api/v1/sensor/category/1337',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_delete_sensor_category(self):
        ''' Ensures that a specific sensor category can be deleted via the API. '''
        response = self.client.delete(
            '/api/v1/sensor/category/1337',
            content_type='application/json',
        )
        assert response.status_code == 204

    def test_create_sensor_data(self):
        ''' Ensures that sensor data can be added via the API. '''
        payload = json.dumps({
            'value': 100.00,
            'created': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        })
        response = self.client.post(
            '/api/v1/sensor/1337/data',
            data=payload,
            content_type='application/json',
        )
        assert response.status_code == 201

    def test_retrieve_sensor_data(self):
        ''' Ensures that sensor data can be retrieved via the API. '''
        response = self.client.get(
            '/api/v1/sensor/1337/data',
            content_type='application/json',
        )
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
