from django.db.models.signals import post_save
from .models import Order
from .tasks import call_after_a_day
from datetime import timedelta
from django.utils import timezone





def AfterCreated(sender,instance,created,**kwargs):
    if created :
        order = instance
        
        scheduled_time = timezone.now() + timedelta(days=1)
        call_after_a_day.apply_async(args=[order.id], eta =scheduled_time)

post_save.connect(AfterCreated, sender = Order)
