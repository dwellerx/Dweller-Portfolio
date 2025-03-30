from flask import Flask, request, render_template_string, send_from_directory
import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import json
import base64

# Load environment variables
load_dotenv()

# Decode the Firebase service account key from Base64
firebase_service_account_key_base64 = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

if not firebase_service_account_key_base64:
    print("Error: FIREBASE_SERVICE_ACCOUNT_KEY not found in environment variables.")
    exit()

try:
    firebase_service_account_key_json = base64.b64decode(firebase_service_account_key_base64).decode('utf-8')
    firebase_service_account_key = json.loads(firebase_service_account_key_json)
except Exception as e:
    print(f"Error decoding Firebase credentials: {e}")
    exit()

# Initialize Firebase Realtime Database
cred = credentials.Certificate(firebase_service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dwellerportfolio-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('emails/')

app = Flask(__name__)

@app.route('/intrestedstyle.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'intrestedstyle.css')

@app.route('/')
def index():
    try:
        with open('intrested.html', 'r') as f:
            html_content = f.read()
        return render_template_string(html_content)
    except Exception as e:
        print(f"Error loading HTML file: {e}")
        return "Error loading the page.", 500

@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form['email_bar']

        # Check if email already exists in the database
        existing_email = ref.order_by_child('email').equal_to(email).get()

        if existing_email:
            return "This email is already registered."

        # Store email in Realtime Database
        ref.push({'email': email})

        print(f"Registered email: {email}")
        return "Registration successful! You will be notified when updates are made."

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred.", 500

if __name__ == '__main__':
    app.run(debug=True)
