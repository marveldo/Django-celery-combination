from django.contrib import admin
from .models import Myuser,Product,Order
# Register your models here.

admin.site.register(Myuser)
admin.site.register(Product)
admin.site.register(Order)