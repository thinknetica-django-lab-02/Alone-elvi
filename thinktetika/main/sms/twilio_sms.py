from thinktetika import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_sms(to, number):
    message = client.messages.create(body=f"Your confirmation number is {number}", from_='+14372343159', to=to)
    return message.status
