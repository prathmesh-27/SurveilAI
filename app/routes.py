from flask import render_template, redirect, url_for, flash, request, session,jsonify,make_response,Response
from app import app
from app.utils import get_current_time
from app.globals import set_user_details,get_user_details_str
from app.db_model import Camera
# import cv2


# Global variables to manage webcam feeds for multiple sections
cameras = {}
is_webcam_active = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make_payment',methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':
        camera = request.form.get('camera_plan').strip()[0]
        # print(camera)
        
        user_info = {
            'name': request.form.get('name'),    
            'organization_name': request.form.get('organization'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),  # Ensure to hash the password in practice
            'phone_number': request.form.get('phone'),
            'camera':int(camera),
            'created_at': get_current_time(),
            'updated_at': get_current_time(),
            'last_login': None
            }
        
        set_user_details(user_info)
        # print(get_user_details_str())
        
        return render_template('payment.html')    
        
    return render_template('payment.html')

@app.route('/success_payment',methods=['POST'])
def success_payment():
    if request.method == 'POST':
       card_number = request.form.get('card_number')
       expiry_date = request.form.get('expiry')
       cvv = request.form.get('cvv')
       name_on_card = request.form.get('name')
       
       print('Card_number',card_number)
       print('Expiry_date',expiry_date)
       print('Cvv',cvv)
       print('Name_on_card',name_on_card)
       
       return redirect(url_for('login'))
       
     
    print("Payment Not Done")  
    return render_template('login.html')
        

# Admin dashboard route (requires admin to be logged in)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash("You need to log in first.", "danger")
        return redirect(url_for('auth.login'))
    user = session.get('user')
    return render_template('dashboard.html',user=user)


@app.route('/cameras')
def cameras():
    if not session.get('logged_in'):
        flash("You need to log in first.", "danger")
        return redirect(url_for('auth.login'))
    user = session.get('user')
    url = Camera.get_camera_url(user['_id'],"1")
    print(url)
    return render_template('cameras.html',user=user)





@app.route('/alerts')
def alerts():
    if not session.get('logged_in'):
        flash("You need to log in first.", "danger")
        return redirect(url_for('auth.login'))
    user = session.get('user')
    
    
    return render_template('alerts.html',user=user)

@app.route('/add_camera', methods=['GET', 'POST'])
def add_camera():
    if not session.get('logged_in'):
        flash("You need to log in first.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user = session.get('user')
        if not user:
            flash("User not found. Please log in again.", "danger")
            return redirect(url_for('auth.login'))
        
        section = request.form.get('section')
        camera_name = "Camera_" + section
        camera_ip = request.form.get('camera_ip')
        camera_port = request.form.get('camera_port')

        # Generate the URL based on the provided section
        if section == '0':
            url = 0
        else:
            url = f"{camera_ip}:{camera_port}"
        
        print(f"Section: {section}, Camera Name: {camera_name}, URL: {url}")

        # Check if a camera with the same section already exists for the user
        existing_camera = Camera.get_camera_by_section(user['_id'], section)
        if existing_camera:
            flash(f"A camera for section {section} already exists.", "danger")
            return redirect(url_for('cameras'))

        # Prepare the camera data to save
        camera = {
            "user_id": user['_id'],
            "camera_url": url,
            "section": section,
            "status": None,
            "camera_name": camera_name,
            "addition_date": get_current_time(),
            "last_activity": get_current_time()
        }

        # Save the new camera to the database
        result = Camera.save_camera(camera)

        if result['status'] == "error":
            flash(result['message'], 'danger')
        else:
            flash(f'Camera {section} added successfully', 'success')

        return redirect(url_for('cameras'))

    # For GET requests, render the form with the current section
    section = request.args.get('section')
    user = session.get('user')
    
    return render_template('add_camera.html', user=user, section=section)


# # Route for webcam feed
# @app.route('/webcam_feed')
# def webcam_feed():
#     return Response(generate_webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


# # Route to stop the webcam feed
# @app.route('/stop_webcam')
# def stop_webcam(section):
#     is_webcam_active[section] = False  
#     print("webcam Stopped")    
#     return 'Webcam stopped'  


