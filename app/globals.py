# globals.py
import json
import cv2
from app.utils import start_port_forwarding,stop_port_forwarding
from flask import jsonify

otp_storage = {}
user_details = {}
cameras = {}
is_webcam_active = {}

def camera_plans():
    global camera_plan
    camera_plan = {
    1: 1245,
    2: 2075,
    3: 2905,
    4: 3735
    }
    return camera_plan 



# function for global otp
def set_otp(email, otp):
    otp_storage[email] = otp

def get_otp(email):
    return otp_storage.get(email)

def delete_otp(email):
    if email in otp_storage:
        del otp_storage[email]

# Function for user details
def set_user_details(user_info):
    global user_details
    user_details = user_info

def get_user_details():
    return user_details

def get_user_details_str():
    # Convert the user details dictionary to a JSON string
    user_details_string = json.dumps(user_details, indent=4)  # Pretty print with indentation
    return user_details_string

def clear_user_details():
    global user_details
    user_details = {}

def set_cameras(section, url, port=None):
    global cameras

    try:
        if section == 0:
            # Use the default webcam
            cameras[section] = cv2.VideoCapture(0)
            if not get_cameras(section).isOpened():
                raise RuntimeError("Failed to open the default webcam.")
        else:
            # Construct the URL for the camera stream
            url = f"http://{url}/video"
            print(f"Attempting to set up camera for section {section} with URL: {url} and port: {port}")

            # Ensure port is valid and start port forwarding
            if port is None:
                raise ValueError("Port must be provided for non-default sections.")
            
            start_port_forwarding(port)

            # Attempt to open the camera stream
            cameras[section] = cv2.VideoCapture(url)
            if not get_cameras(section).isOpened():
                # Stop port forwarding if camera fails to open
                stop_port_forwarding(port)
                raise RuntimeError("Failed to open camera stream. Please check the URL and port.")

    except Exception as e:
        # Log the error and return a failure message
        print(f"Error setting camera for section {section}: {e}")
        return jsonify({"status": "error", "message": str(e)})


def get_cameras(section):
    return cameras.get(section)

def activate_camera(section):
    global is_webcam_active
    is_webcam_active[section] = True
    print(f"Camera activated for section {section}.")

def deactivate_camera(section,port=None):
    global is_webcam_active

    if section != 0 :
        stop_port_forwarding(port)
    else: 
        pass
    
    is_webcam_active[section] = False
    print(f"Camera deactivated for section {section}.")

def get_camera_status(section):
    return is_webcam_active.get(section, False)


