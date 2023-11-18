from twilio.rest import Client


user_number = '+2348102980007'
client = Client('ACa4d01384f35491a38b0a05410650b5d9','7972d88b67839e93bc2df42b40aeeccd')
call = client.calls.create(
            twiml='<Response><Say>Hello you have a pending order</Say></Response>',
            to=f'{user_number}',
            from_= '+14692939044'
        )
print(f'Phone call initiated with SID: {call.sid}')
