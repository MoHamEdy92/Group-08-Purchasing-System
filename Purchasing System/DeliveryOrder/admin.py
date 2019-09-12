from django.contrib import admin

from DeliveryOrder.models import DeliveryOrder,DeliveryOrderItem

admin.site.register(DeliveryOrder)
admin.site.register(DeliveryOrderItem)