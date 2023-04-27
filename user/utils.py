from django.conf import settings
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_otp(mobile, otp):
    account_sid = 'AC339a49687f5cd04de50032a5dcefea3a'
    auth_token = '5977d5eb8bb314217a3907a3850255d6'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body=f"Your OTP code is: ",
                        # otp = otp,
                        from_='+16073177924',
                        to=mobile
                    )

    # print(message.sid)
    return message