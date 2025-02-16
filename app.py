from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from config import Config
from routes import auth
import routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)  # para conectarnos con el frontend

# register blueprints
app.register_blueprint(routes.auth, url_prefix='/auth')

with app.app_context():
    db.create_all()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
