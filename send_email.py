import requests
import json
import os
from datetime import datetime

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
EMAIL = os.getenv("EMAIL")

# Step 1: Get token
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
token_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://graph.microsoft.com/.default'
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get('access_token')

# Step 2: Send email
email_data = {
    "message": {
        "subject": "Automated Daily Email from GitHub",
        "body": {
            "contentType": "Text",
            "content": f"Hello! This is your automated email for {datetime.utcnow().isoformat()}."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": EMAIL
                }
            }
        ]
    },
    "saveToSentItems": "true"
}

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

send_url = f"https://graph.microsoft.com/v1.0/users/{EMAIL}/sendMail"
response = requests.post(send_url, headers=headers, json=email_data)

if response.status_code == 202:
    print("✅ Email sent successfully.")
else:
    print(f"❌ Failed to send email: {response.status_code} {response.text}")
