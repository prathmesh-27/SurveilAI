# models.py
from flask_pymongo import PyMongo
from app import app, db  # Import app and db from your main file
from werkzeug.security import generate_password_hash  # To hash passwords

# class Admin:
#     @staticmethod
#     def create(admin_name, email, password):
#         # Insert the admin into the Admin collection in MongoDB
#         return db.Admin.insert_one({
#             'admin_name': admin_name,
#             'email': email,
#             'password': generate_password_hash(password),  # Hash the password
#             'last_login': None
#         }).inserted_id
        
#     # def get_by_email(username):
#     #     admin_data = db.Admin.find_one({'email': username})
#     #     return admin_data        

class Organization:
    @staticmethod
    def save_organization(org_info):
        
        # Check if email already exists
        existing_user = db.Organization.find_one({"email": org_info['email']})
        
        if existing_user:
            print("Email already exists. Please use a different email.")
            return {"status": "error", "message": "Email already exists."}
        
        required_fields = ['name', 'organization_name', 'email', 'password', 'phone_number', 'camera', 'created_at', 'updated_at', 'last_login']
        
        for field in required_fields:
            if field not in org_info:
                raise ValueError(f"Missing required field: {field}")
             
        # If email doesn't exist, save the user
        org_info['password'] = generate_password_hash(org_info['password'])
        result = db.Organization.insert_one(org_info)
        
        print("User has been added Successfully")
        
        return {"status": "success", "message": "User added successfully.", "user_id": str(result.inserted_id)}
        
    
    @staticmethod
    def get_user_by_email(email):
        user = db.Organization.find_one({'email': email})
        return user  
    
    @staticmethod
    def update_last_login(user_id, last_login_time):
        # Update the last_login field for the user in the database
        db.Organization.update_one(
            {"_id": user_id},
            {"$set": {"last_login": last_login_time}}
        )    
        
        
class Payment:
    @staticmethod
    def save_payment(payment_info):
        required_fields = ['user_id', 'card_details', 'transaction_id', 'amount_paid', 'payment_timestamp','tenure']
        
        for field in required_fields:
            if field not in payment_info:
                raise ValueError(f"Missing required field: {field}")

        result = db.Payment.insert_one(payment_info)
        print("Payment has been recorded successfully.")
        
        return {"status": "success", "message": "Payment saved.", "payment_id": str(result.inserted_id)}    
    
class Camera:
    @staticmethod
    def save_camera(camera_info):
        required_fields = ['user_id', 'camera_url', 'section', 'status', 'camera_name',  'addition_date', 'last_activity']    
        for field in required_fields:
            if field not in camera_info:
                raise ValueError(f"Missing required field: {field}")
        
        result = db.Camera.insert_one(camera_info)
        print("Camera has been recorded successfully.")
        
        return {"status": "success", "message": "Camera saved.", "camera_id": str(result.inserted_id)}      
    
    @staticmethod
    def get_camera_url(user_id, section):
        camera = db.Camera.find_one({"user_id": user_id, "section": section})
    
        if camera:
            return camera.get("camera_url") 
        else:
            return None
        
    @staticmethod
    def get_number_cameras(user_id):
        return db.Camera.count_documents({"user_id": user_id})
    
    # @staticmethod
    # def get_camera_names(user_id):
    #     if not user_id:
    #         return []  # Return an empty list if user_id is None or empty

    #     try:
    #     # Find all documents for the given user_id and retrieve the camera_name field
    #         camera_names = db.Camera.find({"user_id": user_id}, {"camera_name": 1, "_id": 0})
    #         return [camera["camera_name"] for camera in camera_names]  # Return a list of camera names
    #     except Exception as e:
    #         print(f"Error fetching camera names for user {user_id}: {e}")
    #         return []    
     
    
    @staticmethod
    def delete_camera(user_id, section):

        result = db.Camera.delete_one({"user_id": user_id, "section": section})

        if result.deleted_count > 0:
            return {"status": "success", "message": "Camera deleted successfully."}
        else:
            return {"status": "danger", "message": "Camera not found or already deleted."}   
        
    @staticmethod
    def get_camera_by_section(user_id,section):
        return db.Camera.find({"user_id": user_id, "section": section})
            
            