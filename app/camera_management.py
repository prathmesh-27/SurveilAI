from flask import Flask, Response, jsonify,session,request
import cv2
from app import app
from app.db_model import Camera
from app.utils import start_port_forwarding,stop_port_forwarding
from app.globals import activate_camera,get_camera_status,set_cameras, get_cameras,deactivate_camera,cameras
from app.crime_classification import process_frame_for_prediction,make_prediction

cameras = {}
is_webcam_active = {}


@app.route('/start_camera/<int:section>', methods=['PUT'])
def start_camera_section(section):
    global cameras, is_webcam_active

    print(f"Attempting to start camera for section: {section}")

    # Check if section is 0 (special case: no IP and port required)
    if section == 0:
        if get_camera_status(section):
            return jsonify({"status": "error", "message": "Camera is already active for this section."})

        set_cameras(section,0)
        activate_camera(section)  # Use appropriate logic to activate the default camera
        
        return jsonify({"status": "success", "message": f"Default camera started for section {section}"})

    # Parse IP and port from the request JSON
    request_data = request.get_json()
    ip = request_data.get('ip')
    port = request_data.get('port')

    # Validate the port input
    try:
        port = int(port)  # Ensure the port is an integer
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid or missing port number."})

    # Validate IP and port
    if not ip or not port:
        return jsonify({"status": "error", "message": "IP address and port are required."})

    # Check if the camera is already active
    if get_camera_status(section):
        return jsonify({"status": "error", "message": "Camera is already active for this section."})

    # Construct the camera URL using the provided IP and port
    camera_url = f"{ip}:{port}"
    
    print(f"Camera URL for section {section}: {camera_url}")

    # Assign camera to the section
    set_cameras(section, camera_url, port)

    # Activate the camera for the given section
    activate_camera(section)
    print(f"Camera successfully started for section {section}.")
    
    return jsonify({"status": "success", "message": f"Camera started for section {section}."})


# Route to stop the webcam feed
@app.route('/stop_webcam/<int:section>', methods=['PUT'])
def stop_webcam_section(section):
    # Special handling for section 0
    if section == 0:
        if get_camera_status(section):
            get_cameras(section).release()  # Stop the camera
            deactivate_camera(section)  # Deactivate the camera for section 0
            return jsonify({"status": "success", "message": "Default camera stopped for section 0."})
        return jsonify({"status": "error", "message": "No active default camera for section 0."})

    # Parse IP and port from the request JSON
    request_data = request.get_json()
    port = request_data.get('port')
    
    # Validate the port input
    try:
        port = int(port)  # Ensure the port is an integer
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid or missing port number."})

    # Validate IP and port
    if not port:
        return jsonify({"status": "error", "message": "IP address and port are required."})

    # Check if the camera is active
    if get_camera_status(section):
        get_cameras(section).release()  # Stop the camera
        deactivate_camera(section, port)  # Deactivate with additional details
        return jsonify({"status": "success", "message": f"Camera stopped for section {section}."})

    return jsonify({"status": "error", "message": f"No active camera for section {section}."})


# Function to generate video feed with prediction
def generate_video_feed(section):
    frame_sequence = []
    MAX_SEQ_LENGTH = 32
    last_predicted_class = "Waiting for Prediction..."
    while get_camera_status(section):
        success, frame = get_cameras(section).read()
        if not success:
            break
        frame_sequence.append(frame)

        if len(frame_sequence) == MAX_SEQ_LENGTH:
                processed_frames = [process_frame_for_prediction(f) for f in frame_sequence]
                predicted_label = make_prediction(processed_frames)
                frame_sequence = []
                last_predicted_class = predicted_label

        cv2.putText(frame, f"Prediction: {last_predicted_class}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera once streaming stops
    if section in cameras:
        get_cameras(section).release()

# Route for video feed
@app.route('/video_feed/<int:section>')
def video_feed_section(section):
    return Response(generate_video_feed(section),mimetype='multipart/x-mixed-replace; boundary=frame')