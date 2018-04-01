''' Implements tests for Europa Static Content. '''

import unittest
import coverage

from europa import initialize_all


class EuropaStaticTestCase(unittest.TestCase):
    ''' Defines tests for Europa static content. '''

    def setUp(self):
        ''' Ensure the application is setup for testing. '''
        self.application = initialize_all()
        self.client = self.application.test_client()

    def test_fetch_root(self):
        ''' Ensures that the root can be fetched. '''
        response = self.client.get('/')
        assert response.status_code == 200

    def test_fetch_style_css(self):
        ''' Ensures that 'style.css' can be fetched. '''
        response = self.client.get('/static/style.css')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
