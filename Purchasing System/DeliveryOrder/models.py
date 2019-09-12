from django.db import models

from decimal import Decimal
from app.models import Person,Item,Vendor
from PurchaseOrder.models import PurchaseOrder

class DeliveryOrder(models.Model):
    delivery_order_id = models.CharField(primary_key=True, max_length=10)
    shipping_instructions = models.TextField()
    time_created = models.DateTimeField()
    description = models.TextField(null=True,default=None, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    person_id = models.ForeignKey(Person)
    vendor_id = models.ForeignKey(Vendor)
    purchase_order_id = models.OneToOneField(PurchaseOrder)
    def __str__(self):
        return str(self.delivery_order_id)


class DeliveryOrderItem(models.Model):
    delivery_order_id = models.ForeignKey(DeliveryOrder)
    item_id = models.ForeignKey(Item)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ref_id = models.CharField(max_length=20,null=True,default=None, blank=True )

    class Meta:
        unique_together = (("delivery_order_id","item_id"),)
    def __str__(self):
        return str(self.delivery_order_id)
