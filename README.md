# Casting Agency API - Udacity Fullstack Nanodegree Project

The Casting Agency API provides the Casting Agency Assistants, Directors and Produces to update the database of movies and actors in the pipeline.
A live instance of this API is hosted on Heroku at: https://ndp-casting-agency.herokuapp.com/. See the API reference for a guide to the API endpoints to use with this base URL.

## Style Guide

The Trivia API backend is written with PEP 8 as the style guide. Google's yapf formatter was used to format the code. For consistency, feel free to format using it. It can be installed with `pip install yapf` or view the [GitHub repo](https://github.com/google/yapf). Note: some manual editting may be required.

## Quick Start for Local Development

To jump in right away, follow the sections below. For more detailed instructions, view the readme files for the frontend and backend here:

To set up the backend server:

```bash
# Create the database (Casting Agency API uses postgresql)
createdb <database_name>

# Install requirements in a virtual environment
pip install -r requirements.txt

# Set postgresql database URL as environment variable
# NOTE: Use set on Windows
export DATABASE_URL="postres://<host_name>:<port>/<database_name>

# Run the app
flask run
```
NOTE: This API requires authentication, but does not provide a mechanism to sign up for an account. You will need to update the auth0 details in auth.py to provide your own tokens to the API.

# API Reference

The Casting Agency API application is powered by a Python Flask RESTful API on the backend. This API follows RESTful principles, using standard HTTP verbs (GET, POST, DELETE, etc) and returning response as JSON.

## Getting Started

The base URL for the API backend when using locally is http://localhost:8080/

To use the deployed Heroku app, use https://ndp-casting-agency.herokuapp.com/

## Authentication and Authorization Details
Valid JWTs are included in the setup.sh file in this repo. Tokens have a maximum validity of 24 hours and these tokens in the setup.sh file are as close to that as possible. *NOTE for Udacity Graders: Please use the tokens in the setup.sh file with the sample curl commands in each endpoint reference. Make sure to substitute the necessary parameters in the curl commands for the heroku URL, client_token, etc.*

The endpoints each require authentication and authorization to interact with. There are three roles designed to work with the API
1. Casting Assistant
    1. Can get actors and movies
2. Casting Director
    1. Same as Casting Assistant
    2. Can POST a new actor
    3. Can DELETE an actor
    4. Can PATCH actors or movies
3. Casting Producer
    1. Same as Casting Director
    2. Can POST a new movie
    3. Can DELETE a movie
    
A JWT with the requisite permissions is required to interact with each endpoint in the application.

## Errors

Clients should expect to recieve one of several types of HTTP error response codes if something goes wrong or a request is not correctly submitted. Error response messages are returned as JSON. Response codes include:

+ `400` Bad Request
+ `401` Unauthorized
+ `403` Forbidden
+ `404` Not Found
+ `405` Method Not Allowed
+ `422` Unprocessable

The JSON error response will have the following structure:

```javascript
{
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
}
```

## Endpoint Reference

What follows is the API endpoint reference. The URL pattern would be \[base_url\]/endpoint, for example:
<http://localhost:5000/actors>

### GET /actors

Handles requests for actors. When a request is submitted to this endpoint, all actors in the database will be sent to the user in a JSON response.

Sample request: `curl -H 'Authorization: Bearer <jwt_token>' http://localhost:8080/actors`

The JSON response is an object with keys and values:
+ success: True (boolean)
+ actors: (list)
    + name: actor name (string)
    + age: actor age (int)
    + gender: actor gender (string)
+ total_actors: number of actors (int)
+ current_page: current page (int)

```javascript
{
    'success': True,
    'actors': [
        {
            name: 'John Goodman',
            age: 68,
            gender: 'm'
         },
         {
            name: 'Jessica Biel',
            age: 38,
            gender: 'f'
         }
    ],
    'total_actors': 2,
    'current_page': 1
}
```


### GET /movies

Handles requests for movies. When a request is submitted to this endpoint, all movies in the database will be sent to the user in a JSON response.

Sample request: `curl -H 'Authorization: Bearer <jwt_token>' http://localhost:8080/movies`

The JSON response is an object with keys and values:
+ success: True (boolean)
+ movies: (list)
    + title: movie title (string)
    + release_date: release data (date)
+ total_movies: number of movies (int)
+ current_page: current page (int)

```javascript
{
    'success': True,
    'movies': [
        {
            name: 'Surfs Up',
            release_date: 2007-06-08
         },
         {
            name: 'Surfs Up 2: Wave Mania',
            release_date: 2017-01-17
         }
    ],
    'total_movies': 2,
    'current_page': 1
}
```

### DELETE /actors/[actor_id]

Handles delete requests for a specific actor. When a request is submitted to this endpoint, the actor is looked up in the database and deleted. A JSON response is sent to the user to confirm the delete action. This endpoint takes an integer as the final part of the URL.

Sample request: `curl -H 'Authorization: Bearer <jwt_token>' -X DELETE http://localhost:8080/actors/1`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ deleted: (int)

```javascript
{
    'success': True,
    'delete': 1
}
```

### DELETE /movies/[movie_id]

Handles delete requests for a specific movie. When a request is submitted to this endpoint, the movie is looked up in the database and deleted. A JSON response is sent to the user to confirm the delete action. This endpoint takes an integer as the final part of the URL.

Sample request: `curl -H 'Authorization: Bearer <jwt_token>' -X DELETE http://localhost:8080/movies/1`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ deleted: (int)

```javascript
{
    'success': True,
    'delete': 1
}
```

### POST /actors

Handles post requests for actors. When a request is submitted to this endpoint, a new actor is added to the database. A JSON response is sent to the user to confirm the addition.

Sample request: `curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <jwt_token>' -d '{"name": "Foo", "age": 32, "gender": "m"}' http://localhost:8080/actors`

The JSON response is an object with the keys and value data types:
+ success: True (boolean)
+ actors: (list)
    + name: actor name (string)
    + age: actor age (int)
    + gender: actor gender (string)
+ total_actors: number of actors (int)
+ current_page: current page (int)

```javascript
{
    'success': True,
    'actors': [
        {
            name: 'John Goodman',
            age: 68,
            gender: 'm'
         },
         {
            name: 'Jessica Biel',
            age: 38,
            gender: 'f'
         },
         {
            name: 'Foo',
            age: 32,
            gender: 'm'
         }
    ],
    'total_actors': 3,
    'current_page': 1
}
```

### POST /movies

Handles post requests for movies. When a request is submitted to this endpoint, a new movie is added to the database. A JSON response is sent to the user to confirm the addition.

Sample request: `curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer <jwt_token>' -d '{"title": "Bar", "release_date": "2012-12-12"}' http://localhost:8080/movies`

The JSON response is an object with the keys and value data types:
+ success: True (boolean)
+ movies: (list)
    + title: movie title (string)
    + release_date: release data (date)
+ total_movies: number of movies (int)
+ current_page: current page (int)

```javascript
{
    'success': True,
    'movies': [
        {
            name: 'Surf's Up',
            release_date: 2007-06-08
         },
         {
            name: 'Surf's Up 2: Wave Mania',
            release_date: 2017-01-17
         },
         {
            title: 'Bar',
            release_date: '2012-12-12'
         }
    ],
    'total_movies': 3,
    'current_page': 1
}
```

### PATCH /actors/[actor_id]

Handles patch requests for actors. When a request is submitted to this endpoint, the specified actor is modified in the database. A JSON response is sent to the user to confirm the modification.

Sample request: `curl -X PATCH -H 'Content-Type: application/json' -H 'Authorization: Bearer <jwt_token>' -d '{"name": "Baz"}' http://localhost:8080/actors/3`

The JSON response is an object with the keys and value data types:
+ success: True (boolean)
+ actors: (list)
    + name: actor name (string)
    + age: actor age (int)
    + gender: actor gender (string)

```javascript
{
    'success': True,
    'actors': [
         {
            name: 'Baz',
            age: 32,
            gender: 'm'
         }
    ]
}
```

### PATCH /movies/[movie_id]

Handles patch requests for movies. When a request is submitted to this endpoint, the specified movie is modified in the database. A JSON response is sent to the user to confirm the modification.

Sample request: `curl -X PATCH -H 'Content-Type: application/json' -H 'Authorization: Bearer <jwt_token>' -d '{"title": "Foobar"}' http://localhost:8080/movies/3`

The JSON response is an object with the keys and value data types:
+ success: True (boolean)
+ movies: (list)
    + title: movie title (string)
    + release_date: release data (date)

```javascript
{
    'success': True,
    'movies': [
         {
            title: 'Foobar',
            release_date: '2012-12-12'
         }
    ]
}
```
