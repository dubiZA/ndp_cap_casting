import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Movie, Actor

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()

        if not actors:
            abort(404)
        
        actors = [actor.format() for actor in actors]
        print(actors)

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