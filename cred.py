from flask import Flask, request, render_template, send_from_directory, render_template_string
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import json
load_dotenv() 

firebase_service_account_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

cred = credentials.Certificate(json.loads(firebase_service_account_key))
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/intrestedstyle.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'intrestedstyle.css')

@app.route('/')
def index():
    with open('intrested.html', 'r') as f:
        html_content = f.read()
    return render_template_string(html_content)  

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email_bar']
    subscribers_ref = db.collection('subscribers')

    existing_email = subscribers_ref.where('email', '==', email).get()
    if existing_email:
        return "This email is already registered."
    subscribers_ref.add({
        'email': email
    })
    
    print(f"Registered email: {email}")
    
    return "Registration successful! You will be notified when updates are made."

if __name__ == '__main__':
    app.run(debug=True)
