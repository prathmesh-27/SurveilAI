import os
# from flask_pymongo import PyMongo

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # For session management
    # MONGOALCHEMY_DATABASE = 'your_db_name'
    MONGO_URI = os.getenv('MONGO_URI', '#your_mongo_URI')
    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER', '# Your email address')  
    MAIL_PASSWORD = os.getenv('EMAIL_PASS', '# Your app password generated from Google')  # Your app password generated from Google
    
