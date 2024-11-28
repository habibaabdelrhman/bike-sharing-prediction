import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bike_store.db'  # Path to SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Secret key for Flask sessions
