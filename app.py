import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()

        if not actors:
            abort(404)
        
        actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()

        if not movies:
            abort(404)
        
        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
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
    def delete_movie(id):
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
    def post_actor():
        actor_details = request.get_json()
        
        if 'name' not in actor_details or 'age' not in actor_details or 'gender' not in actor_details:
            abort(404)

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

    #TODO Add POST movies endpoint
    @app.route('/movies', methods=['POST'])
    def post_movie():
        movie_details = request.get_json()
        
        if 'title' not in movie_details or 'release_date' not in movie_details:
            abort(404)

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

    #TODO Add PATCH endpoints for actors and movies
    @app.route('/actors/<int:id>', methods=['PATCH'])
    def patch_actor(id):
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
        
        if not actor_name and not actor_age and not actor_gender:
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
    def patch_movie(id):
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
        
        if not movie_title and not movie_release_date:
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

    #TODO Add auth functionality


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


    # @app.errorhandler(AuthError)
    # def auth_error(exception):
    #     return jsonify({
    #         'success': False,
    #         'error': exception.status_code,
    #         'message': exception.error
    #     }), exception.status_code

    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)