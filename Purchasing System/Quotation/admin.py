from django.contrib import admin

from Quotation.models import Quotation,QuotationItem

admin.site.register(Quotation)
admin.site.register(QuotationItem)