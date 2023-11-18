from twilio.rest import Client
import os

user_number = '+2348102980007'
client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
call = client.calls.create(
            twiml='<Response><Say>Hello you have a pending order</Say></Response>',
            to=f'{user_number}',
            from_= '+14692939044'
        )
print(f'Phone call initiated with SID: {call.sid}')
