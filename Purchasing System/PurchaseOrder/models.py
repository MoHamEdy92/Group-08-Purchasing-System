from django.db import models

from decimal import Decimal
from django.contrib.auth.models import User
from app.models import Person,Item,Vendor
from Quotation.models import Quotation
 
class PurchaseOrder(models.Model):
    purchase_order_id = models.CharField(primary_key=True, max_length=10)
    shipping_instructions = models.TextField()
    time_created = models.DateTimeField()
    description = models.TextField(null=True,default=None, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    person_id = models.ForeignKey(Person)
    vendor_id = models.ForeignKey(Vendor)
    quotation_id = models.OneToOneField(Quotation)
    def __str__(self):
        return str(self.purchase_order_id)

class PurchaseOrderItem(models.Model):
    purchase_order_id = models.ForeignKey(PurchaseOrder)
    item_id = models.ForeignKey(Item)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ref_id = models.CharField(max_length=20,null=True,default=None, blank=True )

    class Meta:
        unique_together = (("purchase_order_id","item_id"),)
    def __str__(self):
        return str(self.purchase_order_id)