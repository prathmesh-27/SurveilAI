# **SurveilAI - Real-Time Crime Detection Web App**  

**Note:** This application is still under development. Some features, like email notifications, are not yet fully integrated, and the app currently has some known bugs. The model's accuracy is approximately **72%**, and we are actively working on improving it.

---

## **Steps to Run the Project**

### 1. **Clone the Repository**  
```bash
   git clone https://github.com/prathmesh-27/SurveilAI
   cd SurveilAI
```

### 2. **Update the MongoDB URI**  
Open config.py
 
Replace the placeholder MongoDB URI with your MongoDB Atlas URI:

```bash    
    MONGO_URI = os.getenv('MONGO_URI', '#your_mongo_URI')
  ```
   Ensure your MongoDB database has the following collections:
   
 * Camera
   
 * Organization
   
 * Payment

### 3. ***Set Email Credentials***
* In the config.py file, configure your email and Google-generated app password for sending notifications:
```
    MAIL_USERNAME = os.getenv('EMAIL_USER', '# Your email address')  
    MAIL_PASSWORD = os.getenv('EMAIL_PASS', '# Your app password generated from Google')   
```
### 4. Install Dependencies
Install the required Python packages listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```
### 5. Activate the Virtual Environment
If you're using a virtual environment, activate it:

On Windows:
```bash
venv\Scripts\activate
```
### 6. Run the Application
Start the Flask application:

```
python run.py
```

### 7. Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```
### 8. Create an Account
* Before using the application, register an account through the registration page.
* Follow the on-screen instructions to complete the process.