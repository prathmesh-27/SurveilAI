from flask import render_template, redirect, url_for, flash, request, session,jsonify,make_response
from werkzeug.security import check_password_hash
from app.auth import auth_bp  # Import the blueprint instance
from app.db_model import Organization,Payment
from app.utils import *
from app.globals import get_otp,set_otp,delete_otp,get_user_details,get_user_details_str,camera_plans

# Login route
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # print(email, password)
        
        user = Organization.get_user_by_email(email)
        user = serialize_user(user)
        
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['user'] = user
            session['_id'] = user['_id']
            current_time = get_current_time()  
            Organization.update_last_login(user['_id'], current_time)  # Update last login in the database         
            flash(f"Welcome !!! { user['name'] }", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


# Logout route
@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


# # Signup route
@auth_bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        
        # user_details_str = get_user_details_str()
        # print(user_details_str)
        user_details = get_user_details()
    
        result =  Organization.save_organization(user_details)
        
        if result['status'] == "error":
            print(result['message'])
        
        
        payment_info = {
            "user_id": result['user_id'],
            "card_details": {
                "card_number":request.form.get('card_number').strip()[-4:],
                "card_holder": request.form.get('name'),
                "expiry_date": request.form.get('expiry'),
                "cvv": "###"
            },
            "transaction_id": generate_transaction_id(),
            "amount_paid":camera_plans()[user_details['camera']],
            "payment_timestamp": get_current_time(),
            "tenure":{ 
            "start_date": get_current_time(),
            "end_date": get_28_days_ahead()
            }
        }
        
        response = Payment.save_payment(payment_info)
        
        
        flash('Signup successful! You can now log in.', 'success')
        
        return redirect(url_for('auth.login'))  # Note the 'auth.login' here
    
    return render_template('registration.html')



@auth_bp.route('/send_otp', methods=['POST'])
def otp_request():
    email = request.json.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    otp = send_otp(email) 
    set_otp(email,otp)
    
    return jsonify({"message": f"An OTP has been sent to {email}. Please check your email."}), 200  

@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    email = request.json.get('email')
    user_otp = request.json.get('otp')
    global_otp = get_otp(email)
    
    # print(user_otp)
    # print(global_otp)

    if global_otp == user_otp:
        delete_otp(email)
        return jsonify({"success": "OTP verified successfully!"}), 200
    else:
        return jsonify({"failed": "Invalid OTP!"}), 400