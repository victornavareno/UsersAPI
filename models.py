from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users" # si pongo solo "user" me da error porque user es una palabra reservada de SQL
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # aqui guarderemos el hash de la contraseña
    user_type = db.Column(db.String(50), nullable=False)  # en principio 2 tipos: Asistente a Eventos y Organizador de Eventos

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
