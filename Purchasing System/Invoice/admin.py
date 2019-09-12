from django.contrib import admin

from Invoice.models import Invoice,InvoiceItem

admin.site.register(Invoice)
admin.site.register(InvoiceItem)