# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv('secrets.env')

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

my_phone_number = os.getenv('MY_PHONE_NUMBER')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

call = client.calls.create(
    url='https://incubous-caitlyn-herby.ngrok-free.dev/skipper.xml',
    to=my_phone_number,
    from_=twilio_phone_number,
)

print(call.sid)