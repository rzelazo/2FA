from decouple import config
from twilio.rest import Client
from django.conf import settings
import logging

logging.basicConfig(level=logging.DEBUG)


# Create .env file in the project root. Then find your
# Account SID and Auth Token at twilio.com/console
# and set the environment variables in the .env file. See http://twil.io/secure
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
service_phone_number = config('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number: str):
    """
    Create and send SMS message with verification code to user's 'phone_number' via Twilio API.
    :param user_code: verification code to send to the user
    :param phone_number: user's phone number
    """
    message = client.messages.create(
     body=f'Your verification code: {user_code}',
     from_=service_phone_number,
     to=phone_number
    )

    if settings.DEBUG:
        # log the response sid received from Twilio API to the console
        logging.debug(message.sid)

