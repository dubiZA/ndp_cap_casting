import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize DB connection details
database_name = 'casting_dev'
database_path = f'postgresql:///{database_name}'


db = SQLAlchemy()

# Setup the database connection
def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# Define the Models for the databases
class Movie(db.Model):
    __tablename__ = "movies"


class Actor(db.Model):
    __tablename__ = 'actors'