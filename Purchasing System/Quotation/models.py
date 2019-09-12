from django.db import models

from decimal import Decimal
from django.contrib.auth.models import User
from app.models import Person,Item,Vendor
from RequestForQuotation.models import RequestForQuotation 

# Create your models here.
class Quotation(models.Model):
    quotation_id = models.CharField(primary_key=True, max_length=10)
    time_created = models.DateTimeField()
    description = models.TextField(null=True,default=None, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    vendor_id = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    request_for_quotation_id = models.OneToOneField(RequestForQuotation, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.quotation_id)

class QuotationItem(models.Model):
    quotation_id = models.ForeignKey(Quotation, on_delete = models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ref_id = models.CharField(max_length=20,null=True,default=None, blank=True )

    class Meta:
        unique_together = (("quotation_id","item_id"),)
    def __str__(self):
        return str(self.quotation_id)
