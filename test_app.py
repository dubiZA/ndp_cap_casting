import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

unittest.TestLoader.sortTestMethodsUsing = None

class CastingApiTestCase(unittest.TestCase):
    '''Test case for the Casting Agency API.'''

    def setUp(self):
        '''Executes before each test. Set variables and init app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_url = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_url)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
        new_actor = Actor(
            name='Test_Name',
            age=31,
            gender='f'
        )
        new_actor.insert()
        new_actor = Actor.query.filter(Actor.name.ilike('%Test_Name%')).one_or_none()
        global actor_id
        actor_id = new_actor.id
        
        new_movie = Movie(
            title='Test_Title',
            release_date='2012-02-14'
        )
        new_movie.insert()
        new_movie = Movie.query.filter(Movie.title.ilike('%Test_Title%')).one_or_none()
        global movie_id
        movie_id = new_movie.id

    def tearDown(self):
        '''Executes after each test. Cleans up test data'''
        remove_actors = Actor.query.all()
        if remove_actors:
            for actor in remove_actors:
                actor.delete()
        
        remove_movies = Movie.query.all()
        if remove_movies:
            for movie in remove_movies:
                movie.delete()

    # Success behaviour tests
    def test_get_actors_success(self):
        '''Test retrieving all actors'''
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # def test_get_movies_success(self):
    #     '''Test retrieving all movies'''
    #     response = self.client().get('/movies')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['movies'])

    # def test_post_actor_success(self):
    #     '''Test successfully adding new actor'''
    #     payload = {
    #         'name': 'Bozwil',
    #         'age': 43,
    #         'gender': 'f'
    #     }

    #     response = self.client().post('/actors', json=payload)
    #     data = json.loads(response.data)

    #     actor = Actor.query.filter(Actor.name.ilike('%Bozwil%')).one_or_none()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(payload['name'], actor.name)

    # def test_post_movie_success(self):
    #     '''Test successfully adding a new movie'''
    #     payload = {
    #         'title': 'Wilky',
    #         'release_date': '2012-02-13'
    #     }

    #     response = self.client().post('/movies', json=payload)
    #     data = json.loads(response.data)

    #     movie = Movie.query.filter(Movie.title.ilike('%Wilky%')).one_or_none()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(payload['title'], movie.title)

    # def test_patch_actor_success(self):
    #     '''Test successfully modifying record for an actor'''
    #     payload = {
    #         'name': 'Test_Dubz'
    #     }
        
    #     response = self.client().patch(f'/actors/{actor_id}', json=payload)
    #     data = json.loads(response.data)

    #     actor = Actor.query.get(actor_id)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(payload['name'], actor.name)

    # def test_patch_movie_success(self):
    #     '''Test successfully modifying a movie record'''
    #     payload = {
    #         'title': 'Test_Moovz'
    #     }

    #     response = self.client().patch(f'/movies/{movie_id}', json=payload)
    #     data = json.loads(response.data)

    #     movie = Movie.query.get(movie_id)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(payload['title'], movie.title)
    
    # def test_delete_actor_success(self):
    #     '''Test Successfully removing an actor record'''
    #     response = self.client().delete(f'/actors/{actor_id}')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['delete'], actor_id)

    # def test_delete_movie_success(self):
    #     '''Test removing a movie records'''
    #     response = self.client().delete(f'/movies/{movie_id}')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['delete'], movie_id)

    # # Tests for error behaviors
    # def test_get_actors_not_found(self):
    #     '''Test failing getting out of range page for actors'''
    #     response = self.client().get('/actors?page=100000')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_get_movies_not_found(self):
    #     '''Test failing getting out of range page for movies'''
    #     response = self.client().get('/movies?page=100000')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_delete_actor_not_found(self):
    #     '''Test removing an actor that doesn't exists'''
    #     actor_id = 2000
    #     response = self.client().delete(f'/actors/{actor_id}')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_delete_movie_not_found(self):
    #     '''Test removing a movie that doesn't exist'''
    #     movie_id = 20000
    #     response = self.client().delete(f'/movies/{movie_id}')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)

    # def test_post_actor_bad_data(self):
    #     '''Test successfully adding new actor'''
    #     payload = {
    #         'first_name': 'Oops',
    #         'age': 43,
    #         'gender': 'f'
    #     }

    #     response = self.client().post('/actors', json=payload)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)

    # def test_post_movie_bad_data(self):
    #     '''Test successfully adding a new movie'''
    #     payload = {
    #         'title': 'Wilky',
    #         'date': '2012-02-13'
    #     }

    #     response = self.client().post('/movies', json=payload)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)

    # def test_patch_actor_bad_payload(self):
    #     '''Test successfully modifying record for an actor'''
    #     payload = {
    #         'first_name': 'Test_Dubz'
    #     }
        
    #     response = self.client().patch(f'/actors/{actor_id}', json=payload)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)

    # def test_patch_movie_bad_payload(self):
    #     '''Test successfully modifying a movie record'''
    #     payload = {
    #         'name': 'Test_Moovz'
    #     }

    #     response = self.client().patch(f'/movies/{movie_id}', json=payload)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)

    #TODO Add auth tests


if __name__ == "__main__":
    unittest.main()