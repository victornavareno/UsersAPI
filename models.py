from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import ARRAY  # for postgresql arrays

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """base user model for authentication"""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  
    city = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # "host" or "subscriber"

    def __init__(self, name, email, city, role):
        self.name = name
        self.email = email
        self.city = city
        self.role = role

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Host(db.Model):
    """hosts manage events (Events will be stored in a separate API)"""
    __tablename__ = "hosts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)  # clave foranea con users
    address = db.Column(db.String(255), nullable=True) # exact location of where events will be hosted
    hosted_events = db.Column(ARRAY(db.Integer), default=[])  # array of hosted event IDs (TODO: another API for events)

    user = db.relationship("User", backref=db.backref("host_profile", uselist=False, cascade="all, delete-orphan"))

class Subscriber(db.Model):
    """Subscribers attend events (managed in a separate API)."""
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    subscribed_events = db.Column(ARRAY(db.Integer), default=[])  # Store event IDs (managed externally)

    user = db.relationship("User", backref=db.backref("subscriber_profile", uselist=False, cascade="all, delete-orphan"))