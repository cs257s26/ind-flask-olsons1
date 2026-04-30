'''
A starter file for testing a Flask app
Run with:
python -m unittest flask_tests.py
'''

from ProductionCode.command_line import *
from app import *
import unittest

#todo: i need to fix these fucking error messages and make them less shit because this is fucking awful to read and it pains

class Tests(unittest.TestCase):
    def setUp(self): #runs before each test so I don't need to create a client in each one
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_sightings_path(self):
        response = self.client.get('/sightingslocationsall/2018/American Crow (Corvus brachyrhynchos) /')
        self.assertEqual(response.status_code, 200)
   
        self.assertIn(b'was sighted', response.data)
        self.assertIn(b'18', response.data)

    def test_sightings_zero_count(self):
        response = self.client.get('/sightingslocationsall/2018/Barn Swallow (Hirundo rustica) /')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'was sighted', response.data)
        self.assertIn(b'0', response.data)

    def test_mostpopular_path(self):
        response = self.client.get('/mostpopularstop/2018/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Most popular stop for 2018:', response.data)
        self.assertIn(b'17', response.data)

    def test_sightings_file_not_found(self):
        response = self.client.get('/sightingslocationsall/1900/AHHHHH/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'The file was not found', response.data)

    def test_mostpopular_data_missing(self):
        response = self.client.get('/mostpopularstop/1900/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Data for year not found', response.data)

    def test_sightings_non_year(self):
        response = self.client.get('/sightingslocationsall/notyear/Bird/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Not Found', response.data)

    def test_mostpopular_non_int_year(self):
        response = self.client.get('/mostpopularstop/notyear/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Not Found', response.data)

if __name__ == '__main__':
    unittest.main()