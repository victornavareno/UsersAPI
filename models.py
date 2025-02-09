from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import ARRAY  # For storing event lists

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """Base user model for authentication."""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  
    role = db.Column(db.String(50), nullable=False)  # "host" or "subscriber"

    def __init__(self, email, role):
        self.email = email
        self.role = role

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Host(db.Model):
    """Hosts manage events (stored in a separate API)."""
    __tablename__ = "hosts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)  # clave foranea con users
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    hosted_events = db.Column(ARRAY(db.Integer), default=[])  # array de events IDs (managed externally)

    user = db.relationship("User", backref=db.backref("host_profile", uselist=False, cascade="all, delete-orphan"))

class Subscriber(db.Model):
    """Subscribers attend events (managed in a separate API)."""
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    subscribed_events = db.Column(ARRAY(db.Integer), default=[])  # Store event IDs (managed externally)

    user = db.relationship("User", backref=db.backref("subscriber_profile", uselist=False, cascade="all, delete-orphan"))


# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# db = SQLAlchemy()
# bcrypt = Bcrypt()

# class User(db.Model):
#     __tablename__ = "users" # si pongo solo "user" me da error porque user es una palabra reservada de SQL maldision
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)  # aqui guarderemos el hash de la contraseña
#     role = db.Column(db.String(50), nullable=False)  # en principio 2 tipos: Asistente a Eventos y Organizador de Eventos

#     def __init__(self, email, role):
#         self.email = email
#         self.role = role
        
#     def set_password(self, password):
#         self.password = bcrypt.generate_password_hash(password).decode("utf-8")

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password, password)


# class Host(db.Model):
#     __tablename__ = "hosts"
#     id = db.Column(db.Integer, primary_key=True)
#     id_host = db.Column(db.String(50), nullable=False)
#     name = db.Column(db.String(255), nullable=False)
#     address = db.Column(db.String(255), nullable=False)

# class Subscriber(db.Model):
#     __tablename__ = "subscribers"
#     id = db.Column(db.Integer, primary_key=True)
#     id_subscriber = db.Column(db.String(50), nullable=False)
#     name = db.Column(db.String(255), nullable=False)
    
