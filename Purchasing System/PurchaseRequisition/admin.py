from django.contrib import admin

# Register your models here.

from PurchaseRequisition.models import PurchaseRequisition,PurchaseRequisitionItem

admin.site.register(PurchaseRequisition)
admin.site.register(PurchaseRequisitionItem)