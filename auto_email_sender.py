import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import json
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

firebase_service_account_key_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
brevo_service_account_key_string = os.getenv('BREVO_KEY')

if not firebase_service_account_key_json:
    print("Error: FIREBASE_SERVICE_ACCOUNT_KEY not found in environment variables.")
    exit()

try:
    firebase_service_account_key = json.loads(firebase_service_account_key_json)
except json.JSONDecodeError as e:
    print(f"Error decoding Firebase credentials: {e}")
    exit()

cred = credentials.Certificate(firebase_service_account_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dwellerportfolio-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('emails/')

def get_all_emails():
    emails_data = ref.get()

    email_list = []
    if emails_data:
        for key, value in emails_data.items():
            if "email" in value:
                email_list.append({"email": value["email"], "name": "User"})  

    return email_list

def send_emails(html_content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = brevo_service_account_key_string
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    email_data = {
        "sender": {"name": "Dweller", "email": "dweller@gmail.com"},
        "to": get_all_emails(),
        "subject": "Newsletter Update",
        "htmlContent": html_content
    }
    try:
        api_instance.send_transac_email(email_data)
        print("Emails sent successfully!")
    except ApiException as e:
        print(f"Error sending email: {e}")

def send_email_welcome(recipient_email):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = brevo_service_account_key_string
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    email_data = {
        "sender": {"name": "Dweller", "email": "dwellerxteam@gmail.com"},
        "to": [{"email": recipient_email, "name": "User"}],  
        "subject": "Newsletter Welcome Email",
        "htmlContent": "<h1>Welcome!</h1><p>This is an automated email. Thanks for subrscribing to my newletter!.</p>"
    }
    try:
        api_instance.send_transac_email(email_data)
        print(f"Email sent successfully to {recipient_email}!")
    except ApiException as e:
        print(f"Error sending email: {e}")
