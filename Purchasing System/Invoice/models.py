from django.db import models

from app.models import Person,Vendor,Item
from PurchaseOrder.models import PurchaseOrder,PurchaseOrderItem
from decimal import Decimal

# Create your models here.
class Invoice(models.Model):
    invoice_id = models.CharField(primary_key= True, max_length=10)
    time_created = models.DateTimeField()
    description = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    invoice_status = models.CharField(max_length=20)
    purchase_order_id =models.OneToOneField(PurchaseOrder,on_delete = models.CASCADE)
    person_id = models.ForeignKey(Person,on_delete= models.CASCADE)
    vendor_id = models.ForeignKey(Vendor,on_delete = models.CASCADE)
def __str__ (self):
        return str(self.invoice_id)

class InvoiceItem(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete= models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete= models.CASCADE )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ref_id = models.CharField(max_length=20,null=True,default=None, blank=True )

    class Meta:
        unique_together = (("invoice_id","item_id"),)
    def __str__(self):
        return str(self.invoice_id)
