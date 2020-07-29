import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingApiTestCase(unittest.TestCase):
    '''Test case for the Casting Agency API.'''

    def setUp(self):
        '''Set variables and init app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_url = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_url)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        '''Executes after each test'''
        pass

    def test_get_actors_success(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies_success(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_actor_success(self):
        actor_id = 4
        response = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], actor_id)

    def test_delete_actor_not_found(self):
        actor_id = 2000
        response = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie_success(self):
        movie_id = 2
        response = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], movie_id)

    def test_delete_movie_not_found(self):
        movie_id = 20000
        response = self.client().delete(f'/movies/{movie_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    #TODO Add tests for POST actors

    #TODO Add tests for POST movies

    #TODO Add tests for PATCH actors

    #TODO Add tests for PATCH movies

    #TODO Add fail tests for all endpoints

    #TODO Add auth tests


if __name__ == "__main__":
    unittest.main()