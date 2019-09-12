from django.contrib import admin

from RequestForQuotation.models import RequestForQuotation,RequestForQuotationItem

admin.site.register(RequestForQuotation)
admin.site.register(RequestForQuotationItem)