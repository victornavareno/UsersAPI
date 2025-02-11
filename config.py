import os

#añadir claves cuando termine el prototipo
class Config:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost:5433/users"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "clave_secreta_jwt"

