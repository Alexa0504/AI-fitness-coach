from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils.auth_decorator import token_required
from backend.utils.security_utils import hash_password, check_password, generate_auth_token
from backend.utils.token_blacklist import add_token_to_blacklist

# Create the Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registers a new user, hashes the password, and issues a token."""

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic validation
    if not all([username, email, password]):
        return jsonify({"message": "Missing required fields (username, email, or password)."}), 400

    # Check if email or username already exists
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({"message": "Username or email already registered."}), 409

    try:
        # 1. Hash the password (for secure storage)
        hashed_pw = hash_password(password)

        # 2. Create and save the new user
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()

        # 3. Generate token (for immediate login)
        token = generate_auth_token(str(new_user.id))

        # 4. Respond to the frontend (using to_dict() to exclude the hash!)
        return jsonify({
            "message": "Registration successful.",
            "user": new_user.to_dict(),
            "token": token
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Registration Error: {e}")
        return jsonify({"message": "An internal error occurred during registration."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticates the user by username or email and password then returns a JWT token."""

    data = request.get_json()
    identifier = data.get('email') or data.get('username') or data.get('identifier')
    password = data.get('password')

    if not all([identifier, password]):
        return jsonify({"message": "Missing username/email or password."}), 400

    user = User.query.filter(
        (User.email == identifier) | (User.username == identifier)
    ).first()

    # In case of invalid username/email or password.:
    if not user or not check_password(password, user.password_hash):
        return jsonify({"message": "Invalid username/email or password."}), 401

    # Successful login
    token = generate_auth_token(str(user.id))
    return jsonify({
        "message": "Login successful.",
        "user": user.to_dict(),
        "token": token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logs out the user by blacklisting the current token."""
    token = request.headers['Authorization'].split(" ")[1]
    if add_token_to_blacklist(token):
        return jsonify({"message": "Logout successful."}), 200
    else:
        return jsonify({"message": "Failed to blacklist token."}), 500
