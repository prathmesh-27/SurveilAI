import random
from flask_mail import Message  
from app import app, mail
from datetime import datetime,timedelta
import string
from bson import ObjectId
import subprocess,time

def serialize_user(user):
    # Check if user is None
    if user is None:
        return None
    
    # Ensure user is a dictionary
    if not isinstance(user, dict):
        try:
            user_copy = dict(user)  # Convert to dictionary if possible
        except TypeError:
            raise ValueError("Cannot serialize user: Expected a dictionary or dictionary-like object")
    else:
        user_copy = user.copy()  # Make a copy of the user data

    # Convert ObjectId to string if found
    for key, value in user_copy.items():
        if isinstance(value, ObjectId):
            user_copy[key] = str(value)  # Convert ObjectId to string
    
    return user_copy

def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    msg = Message("Your OTP Code", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP code is {otp}. Please use this code to complete your registration."
    
    mail.send(msg)  # Send the email 
    
    return otp  

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_28_days_ahead():
    current_time = datetime.now()
    new_time = current_time + timedelta(days=28)
    return new_time.strftime("%Y-%m-%d %H:%M:%S")

def generate_transaction_id():
    # Define the prefix
    prefix = "TXN_"
    
    # Generate a random 16-character alphanumeric string
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Combine the prefix and suffix
    transaction_id = f"{prefix}{suffix}"
    
    return transaction_id

def start_port_forwarding(port):
    subprocess.Popen(['adb', 'forward', f'tcp:{port}', f'tcp:{port}'])
    time.sleep(2)

def stop_port_forwarding(port):
    subprocess.Popen(['adb', 'forward', '--remove', f'tcp:{port}'])

# def generate_webcam_feed(section,url):
#     global cameras, is_webcam_active
    
#     if  section == 0:
#         cameras[section] = cv2.VideoCapture(0)  # Using webcam index 0 for all sections
#         is_webcam_active[section] = True
#     else:
#         cameras[section] = cv2.VideoCapture(url)  # Using URL for other sections
#         is_webcam_active[section] = True
        
        
#     while is_webcam_active[section]:
#         success, frame = cameras[section].read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
