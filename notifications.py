from datetime import datetime
from json import dumps

from whatsapp_api_client_python import API

import requests


def sendMessage(messaggio):
    url = "https://7103.api.greenapi.com/waInstance7103110799/sendMessage/2b7fcf0f09c14c02911828a57930e68278d5f11b7d3b4e5784"

    # Payload with the necessary parameters
    payload = {
        "chatId": "3420499966@c.us",  # Replace with the recipient's WhatsApp number in the correct format
        "message": f"{messaggio}"
    }

    # Set headers if needed (for example, authorization tokens)
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request with payload
    response = requests.post(url, json=payload, headers=headers)

    # Print the response to see the result
    print(response.text)
