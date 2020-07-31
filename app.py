import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

ITEMS_PER_PAGE = 5

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    all_items = [item.format() for item in selection]
    current_items = all_items[start:end]

    return {
        'current_page': page,
        'total_items': len(all_items),
        'current_items': current_items
    }

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    @requires_auth(permission='get:actors')
    def get_actors(jwt):
        '''Handles GET requests for actors.

        Accepts a request for actors and retrieves all actors
        from the database.

        Returns:
            A JSON response reporting success, a list of actors as 
            JSON objects, total number of actors and current page.

        Raises:
            404 if there are no actors to return.
            422 if the request cannot be processed
        '''
        try:
            actors = Actor.query.order_by(Actor.id).all()
        except:
            abort(422)
        
        current_actors = paginate(request, actors)

        if len(current_actors['current_items']) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors['current_items'],
            'total_actors': current_actors['total_items'],
            'current_page': current_actors['current_page']
        })

    @app.route('/movies')
    @requires_auth(permission='get:movies')
    def get_movies(jwt):
        '''Handles GET requests for movies.

        Accepts a request for movies and retrieves all movies
        from the database.

        Returns:
            A JSON response reporting success, a list of movies as 
            JSON objects, total number of movies and current page.

        Raises:
            404 if there are no movies to return.
            422 if the request cannot be processed
        '''
        try:
            movies = Movie.query.order_by(Movie.id).all()
        except:
            abort(404)

        current_movies = paginate(request, movies)

        if len(current_movies['current_items']) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies['current_items'],
            'total_movies': current_movies['total_items'],
            'current_page': current_movies['current_page']
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:actors')
    def delete_actor(jwt, id):
        '''Handles DELETE requests for actors.

        Accepts a delete request for a specified actor
        and deletes it from the database.

        Returns:
            A JSON response reporting success and the
            ID of the deleted actor.

        Raises:
            404 if the specified actor does not exist.
            422 if the request cannot be processed
        '''
        actor = Actor.query.get(id)

        if not actor:
            abort(404)
        
        try:
            actor.delete()

            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:movies')
    def delete_movie(jwt, id):
        '''Handles DELETE requests for movies.

        Accepts a delete request for a specified movie
        and deletes it from the database.

        Returns:
            A JSON response reporting success and the
            ID of the deleted movie.

        Raises:
            404 if the specified movie does not exist.
            422 if the request cannot be processed
        '''
        movie = Movie.query.get(id)

        if not movie:
            abort(404)
        
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth(permission='post:actors')
    def post_actor(jwt):
        '''Handles POST requests for actors.

        Accepts a POST request for actors and adds the new
        record to the database.

        Returns:
            A JSON response reporting success, a list of all actors
            as JSON objects, total number of actors & current page.

        Raises:
            422 if the request cannot be processed
        '''
        actor_details = request.get_json()
        
        if 'name' not in actor_details or 'age' not in actor_details or 'gender' not in actor_details:
            abort(422)

        actor_name = actor_details['name']
        actor_age = actor_details['age']
        actor_gender = actor_details['gender']

        try:
            new_actor = Actor(
                name=actor_name,
                age=actor_age,
                gender=actor_gender
            )
            new_actor.insert()

            all_actors = Actor.query.all()
            all_actors = [actor.format() for actor in all_actors]
        except:
            abort(422)
        
        return jsonify({
            'success': True,
            'actors': all_actors
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth(permission='post:movies')
    def post_movie(jwt):
        '''Handles POST requests for movies.

        Accepts a POST request for movies and adds the new
        record to the database.

        Returns:
            A JSON response reporting success, a list of all movies
            as JSON objects, total number of movies & current page.

        Raises:
            422 if the request cannot be processed
        '''
        movie_details = request.get_json()
        
        if 'title' not in movie_details or 'release_date' not in movie_details:
            abort(422)

        movie_title = movie_details['title']
        movie_release_date = movie_details['release_date']

        try:
            new_movie = Movie(
                title=movie_title,
                release_date=movie_release_date
            )
            new_movie.insert()

            all_movies = Movie.query.all()
            all_movies = [movie.format() for movie in all_movies]
        except:
            abort(422)
        
        return jsonify({
            'success': True,
            'movies': all_movies
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:actors')
    def patch_actor(jwt, id):
        '''Handles PATCH requests for actors.

        Accepts a PATCH request for a specified actor
        and updates the record in the database.

        Returns:
            A JSON response reporting success and the
            record for the modified record.

        Raises:
            404 if the specified actor does not exist.
            422 if the request cannot be processed
        '''
        edit_actor = Actor.query.get(id)
        if not edit_actor:
            abort(404)

        actor_update = request.get_json()
        if 'name' in actor_update:
            actor_name = actor_update['name']
            edit_actor.name = actor_name
        if 'age' in actor_update:
            actor_age = actor_update['age']
            edit_actor.age = actor_age
        if 'gender' in actor_update:
            actor_gender = actor_update['gender']
            edit_actor.gender = actor_gender
        if 'name' not in actor_update:
            if 'age' not in actor_update:
                if 'gender' not in actor_update:
                    abort(422)

        try:
            edit_actor.update()
            actor = Actor.query.get(id)
            actor = actor.format()

            return jsonify({
                'success': True,
                'actors': actor
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:movies')
    def patch_movie(jwt, id):
        '''Handles PATCH requests for movies.

        Accepts a PATCH request for a specified movie
        and updates the record in the database.

        Returns:
            A JSON response reporting success and the
            record for the modified record.

        Raises:
            404 if the specified movie does not exist.
            422 if the request cannot be processed
        '''
        edit_movie = Movie.query.get(id)
        if not edit_movie:
            abort(404)

        movie_update = request.get_json()
        if 'title' in movie_update:
            movie_title = movie_update['title']
            edit_movie.title = movie_title
        if 'release_date' in movie_update:
            movie_release_date = movie_update['release_date']
            edit_movie.release_date = movie_release_date
        if 'title' not in movie_update:
            if 'release_date' not in movie_update:
                abort(422)

        try:
            edit_movie.update()
            movie = Movie.query.get(id)
            movie = movie.format()

            return jsonify({
                'success': True,
                'movies': movie
            })
        except:
            abort(422)


    # Error handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized'
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden'
        }), 403


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404


    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422


    @app.errorhandler(AuthError)
    def auth_error(exception):
        return jsonify({
            'success': False,
            'error': exception.status_code,
            'message': exception.error
        }), exception.status_code

    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)