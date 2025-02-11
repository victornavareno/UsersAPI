from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Host, Subscriber  # Import new models

auth = Blueprint("auth", __name__)

# Test default route
@auth.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello World!"})

#  Register a new user
@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "subscriber")  # por defecto es qsubscriber
    
    # opcionales en la pagina register
    address = data.get("address")
    city = data.get("city")

    if role not in ["host", "subscriber"]:
        return jsonify({"error": "Invalid role"}), 400

    if not email or not password or not name:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Create base user
    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Create role-specific profile
    if role == "host":
        # if not address or not city:
        #     return jsonify({"error": "Hosts must provide address and city"}), 400
        host_profile = Host(user_id=user.id, name=name, address=address, city=city)
        db.session.add(host_profile)

    elif role == "subscriber":
        subscriber_profile = Subscriber(user_id=user.id, name=name)
        db.session.add(subscriber_profile)

    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login a user
@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({"token": access_token, "role": user.role}), 200

# Get user profile
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }

    if user.role == "host":
        host_profile = Host.query.filter_by(user_id=user.id).first()
        if host_profile:
            user_data.update({
                "name": host_profile.name,
                "address": host_profile.address,
                "city": host_profile.city,
                "hosted_events": host_profile.hosted_events
            })

    elif user.role == "subscriber":
        subscriber_profile = Subscriber.query.filter_by(user_id=user.id).first()
        if subscriber_profile:
            user_data.update({
                "name": subscriber_profile.name,
                "subscribed_events": subscriber_profile.subscribed_events
            })

    return jsonify(user_data), 200

# Delete user (also deletes host/subscriber profile)
@auth.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role == "host":
        Host.query.filter_by(user_id=user.id).delete()

    elif user.role == "subscriber":
        Subscriber.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


# TODO: add authentication with google using 0Auth2.0