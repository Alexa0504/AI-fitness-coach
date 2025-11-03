from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils.security_utils import hash_password, check_password, generate_auth_token

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

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email address already registered."}), 409

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
    """Authenticates the user based on email and password and returns a JWT token."""

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Missing email or password."}), 400

    # 1. Find user by email
    user = User.query.filter_by(email=email).first()

    if user:
        # 2. Check password against the stored hash
        if check_password(password, user.password_hash):

            # 3. Successful login, generate token
            token = generate_auth_token(str(user.id))

            return jsonify({
                "message": "Login successful.",
                "user": user.to_dict(),
                "token": token
            }), 200
        else:
            # 4. Incorrect password
            return jsonify({"message": "Invalid credentials."}), 401
    else:
        # 5. User not found
        return jsonify({"message": "Invalid credentials."}), 401
