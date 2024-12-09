from flask import Blueprint

# Initialize the blueprint for auth
auth_bp = Blueprint('auth', __name__)

# Import the routes from auth.py to associate them with this blueprint
from app.auth import auth