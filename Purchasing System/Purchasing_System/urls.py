"""
Definition of urls for Purchasing_System.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
from django.contrib import admin

import app.forms
import app.views

import PurchaseRequisition.views
import RequestForQuotation.views
import Quotation.views
import PurchaseOrder.views
import DeliveryOrder.views
import Invoice.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^menu$', app.views.menu, name='menu'),

    #purchase requisition
    url(r'^purchaserequisitionform$', PurchaseRequisition.views.purchaserequisitionform, name="purchase_requisition_form"),
    url(r'^purchaserequisitionconfirmation', PurchaseRequisition.views.purchaserequisitionconfirmation, name="confirm_purchase_requisition"),
    url(r'^purchaserequisitiondetails', PurchaseRequisition.views.purchaserequisitiondetails, name="purchase_requisition_details"),
    url(r'^purchaserequisitionhistorydetails', PurchaseRequisition.views.purchaserequisitionhistorydetails, name='purchase_requisition_history_details'),
    url(r'^purchaserequisitionhistory', PurchaseRequisition.views.purchaserequisitionhistory, name="purchase_requisition_history"),

    #request for quotation
    url(r'^requestforquotationform$', RequestForQuotation.views.requestforquotationform, name="request_for_quotation_form"),
    url(r'^fillingrequestforquotation', RequestForQuotation.views.fillingrequestforquotation, name="fill_request_for_quotation_form"),
    url(r'^requestforquotationconfirmation', RequestForQuotation.views.requestforquotationconfirmation, name="confirm_request_for_quotation"),
    url(r'^requestforquotationdetails', RequestForQuotation.views.requestforquotationdetails, name="request_for_quotation_details"),
    url(r'^requestforquotationhistorydetails', RequestForQuotation.views.requestforquotationhistorydetails, name='request_for_quotation_history_details'),
    url(r'^requestforquotationhistory', RequestForQuotation.views.requestforquotationhistory, name="request_of_quotation_history"),

    #quotation
    url(r'^quotationform$', Quotation.views.quotationform, name="quotation_form"),
    url(r'^fillingquotation', Quotation.views.fillingquotation, name="fill_quotation_form"),
    url(r'^quotationconfirmation', Quotation.views.quotationconfirmation, name="confirm_quotation"),
    url(r'^quotationdetails', Quotation.views.quotationdetails, name="quotation_details"),
    url(r'^quotationhistorydetails', Quotation.views.quotationhistorydetails, name='quotation_history_details'),
    url(r'^quotationhistory', Quotation.views.quotationhistory, name="quotation_history"),

    #purchase order
    url(r'^purchaseorderform$', PurchaseOrder.views.purchaseorderform, name="purchase_order_form"),
    url(r'^fillingpurchaseorder', PurchaseOrder.views.fillingpurchaseorder, name="fill_purchase_order_form"),
    url(r'^purchaseorderconfirmation', PurchaseOrder.views.purchaseorderconfirmation, name="confirm_purchase_order"),
    url(r'^purchaseorderdetails', PurchaseOrder.views.purchaseorderdetails, name="purchase_order_details"),
    url(r'^purchaseorderhistorydetails', PurchaseOrder.views.purchaseorderhistorydetails, name='purchase_order_history_details'),
    url(r'^purchaseorderhistory', PurchaseOrder.views.purchaseorderhistory, name="purchase_order_history"),

    #delivery order
    url(r'^deliveryorderform$', DeliveryOrder.views.deliveryorderform, name="delivery_order_form"),
    url(r'^fillingdeliveryorder', DeliveryOrder.views.fillingdeliveryorder, name="fill_delivery_order_form"),
    url(r'^deliveryorderconfirmation', DeliveryOrder.views.deliveryorderconfirmation, name="confirm_delivery_order"),
    url(r'^deliveryorderdetails', DeliveryOrder.views.deliveryorderdetails, name="delivery_order_details"),
    url(r'^deliveryorderhistorydetails', DeliveryOrder.views.deliveryorderhistorydetails, name='delivery_order_history_details'),
    url(r'^deliveryorderhistory', DeliveryOrder.views.deliveryorderhistory, name="delivery_order_history"),

    #Invoice
    url(r'^invoiceform$', Invoice.views.invoiceform, name="invoiceform"),
    url(r'^fillinginvoice', Invoice.views.fillinginvoice, name="fill_invoice_form"),
    url(r'^invoiceconfirmation', Invoice.views.invoiceconfirmation, name="confirm_invoice"),
    url(r'^invoicedetails', Invoice.views.invoicedetails, name="invoice_details"),
    url(r'^invoicehistorydetails', Invoice.views.invoicehistorydetails, name='invoice_history_details'),
    url(r'^invoicehistory', Invoice.views.invoicehistory, name="invoice_history"),
]

handler404 = "page_not_found"
