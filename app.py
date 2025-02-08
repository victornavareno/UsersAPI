from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from config import Config
import routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)  # para conectarnos con el frontend

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
