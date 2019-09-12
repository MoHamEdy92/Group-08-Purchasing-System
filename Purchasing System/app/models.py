"""
Definition of models.
"""

from django.db import models

from decimal import Decimal
from django.contrib.auth.models import User

#sharing entity

class Person(models.Model):
    user_id = models.OneToOneField(User)
    person_id = models.CharField(primary_key=True, max_length=10)
    person_name = models.TextField()
    person_address = models.TextField()
    person_phone_number = models.TextField()
    person_role = models.TextField(default = 'MANAGER')

    def __chr__(self):
        return str(self.person_id)

class Vendor(models.Model):
    vendor_id = models.CharField(primary_key=True, max_length=10)
    vendor_name = models.TextField()
    vendor_phone_number = models.TextField()
    vendor_address = models.TextField()
    vendor_email = models.TextField()
    def __str__(self):
        return str(self.vendor_id)

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)
