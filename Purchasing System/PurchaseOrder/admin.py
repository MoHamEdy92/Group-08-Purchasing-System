from django.contrib import admin

from PurchaseOrder.models import PurchaseOrder,PurchaseOrderItem

admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
