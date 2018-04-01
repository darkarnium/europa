''' Implements tests for the Europa UI. '''

import unittest
import coverage

from europa import initialize_all


class EuropaStaticTestCase(unittest.TestCase):
    ''' Defines tests for the Europa UI. '''

    def setUp(self):
        ''' Ensure the application is setup for testing. '''
        self.application = initialize_all()
        self.client = self.application.test_client()

    def test_fetch_index(self):
        ''' Ensures that the root index redirects to the UI. '''
        response = self.client.get('/')
        assert response.status_code == 302

    def test_fetch_ui_index(self):
        ''' Ensures that the UI index can be fetched. '''
        response = self.client.get('/ui/')
        assert response.status_code == 200

    def test_fetch_ui_static_content(self):
        ''' Ensures that static files can be fetched. '''
        response = self.client.get('/ui/static/css/style.css')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
