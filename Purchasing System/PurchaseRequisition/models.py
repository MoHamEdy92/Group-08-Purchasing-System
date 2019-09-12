from django.db import models

from decimal import Decimal
from django.contrib.auth.models import User
from app.models import Person,Item

# Create your models here.
class PurchaseRequisition(models.Model):
    pr_id= models.CharField(max_length=10, primary_key=True) #takes character
    description= models.TextField(null=True,default=None, blank=True)
    time_created= models.DateTimeField()
    total_price= models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status= models.TextField(max_length=10, default="Pending")
    person_id = models.ForeignKey(Person)

    def __str__(self):
        return str(self.pr_id)


class PurchaseRequisitionItem(models.Model):
    #attribute will represent column in the database
    pr_id= models.ForeignKey(PurchaseRequisition)#takes character
    item_id= models.ForeignKey(Item)#takes character
    unit_price= models.DecimalField(max_digits= 10, decimal_places=2)
    quantity= models.IntegerField()
    ref_id = models.CharField(max_length=20,null=True,default=None, blank=True )


    class Meta:
        unique_together = (("pr_id", "item_id"))

    def __str__(self):
        return str(self.pr_id)