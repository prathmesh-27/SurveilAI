from flask import Flask
from config import Config
from flask_mail import Mail
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config.from_object(Config)
db = PyMongo(app).db
mail = Mail(app)  

# Import and register blueprints
from app.auth import auth_bp  # Import the auth blueprint

app.register_blueprint(auth_bp, url_prefix='/auth') 

print("SuccessFully Connect")

from app import routes
from app import camera_management
from app import crime_classification


