from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Host, Subscriber

auth = Blueprint("auth", __name__)

#  Default Route - testing api
@auth.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello World!"})

# Register a new user (Host or Subscriber)
@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "subscriber")  # Default: subscriber
    city = data.get("city")

    # verify required fields
    if not all([name, email, password, city]):
        return jsonify({"error": "Missing required fields"}), 400

    if role not in ["host", "subscriber"]:
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # Create base user
    user = User(name=name, email=email, city=city, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Create role-specific profile (address added later for hosts - reducing required friction for normal users in fronted
    if role == "host":
        host_profile = Host(user_id=user.id)
        db.session.add(host_profile)
    else:
        subscriber_profile = Subscriber(user_id=user.id)
        db.session.add(subscriber_profile)

    db.session.commit()
    return jsonify({"message": f"User {role} registered successfully!", "user_id": user.id}), 201

# Add Address for Hosts (Separate Step)
@auth.route("/host/address", methods=["POST"])
@jwt_required()
def add_host_address():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user or user.role != "host":
        return jsonify({"error": "Only hosts can set an address"}), 403

    data = request.json
    address = data.get("address")

    if not address:
        return jsonify({"error": "Address is required"}), 400

    host_profile = Host.query.filter_by(user_id=user.id).first()
    if not host_profile:
        return jsonify({"error": "Host profile not found"}), 404

    host_profile.address = address
    db.session.commit()

    return jsonify({"message": "Address added successfully!"}), 200

#  Login Route
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

# Get User Profile
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "city": user.city
    }

    if user.role == "host":
        host_profile = Host.query.filter_by(user_id=user.id).first()
        if host_profile:
            user_data["address"] = host_profile.address
            user_data["hosted_events"] = host_profile.hosted_events
    elif user.role == "subscriber":
        subscriber_profile = Subscriber.query.filter_by(user_id=user.id).first()
        if subscriber_profile:
            user_data["subscribed_events"] = subscriber_profile.subscribed_events

    return jsonify(user_data), 200

#  Delete User
@auth.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Delete associated profiles
    if user.role == "host":
        Host.query.filter_by(user_id=user.id).delete()
    elif user.role == "subscriber":
        Subscriber.query.filter_by(user_id=user.id).delete()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
