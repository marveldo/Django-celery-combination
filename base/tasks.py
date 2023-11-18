from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from twilio.base.exceptions import TwilioException
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from rest_framework.response import Response
import logging
from .models import Order


@shared_task
def call_after_a_day(order_id):
    try:
       order = Order.objects.get(id=order_id)
       user_number = f'{order.customer_number}'
       client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
       call = client.calls.create(
            twiml='<Response><Say>Hello you have a pending order</Say></Response>',
            to=f'{user_number}',
            from_= '+14692939044'
        )
       return f'Phone call initiated with SID: {call.sid}'
    
    except TwilioException:
        return 'Call coulnt be established'
    except Order.DoesNotExist:
        return  'order doesnt exist'


@shared_task
def add(x,y):
    return x+y

