from django.contrib import admin
from .models import Account, Storage, Delivery, Order, Item

# Register your models here.
admin.site.register(Account)
admin.site.register(Storage)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Item)
