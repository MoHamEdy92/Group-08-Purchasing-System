from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from datetime import datetime
from app.models import Person,Item,Vendor
from PurchaseOrder.models import PurchaseOrder,PurchaseOrderItem
from Invoice.models import Invoice,InvoiceItem
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http.request import QueryDict
from decimal import Decimal
import random
import datetime 


@login_required
def invoiceform(request):
    context = {
            'title':'INVOICE AND PAYMENT FORM'
        }
    context['user'] = request.user

    return render(request,'Invoice/invoiceform.html',context)


@login_required
def fillinginvoice(request):

    global responsesItems
    context = {}
    pur_id = request.GET['pur_id']
    inv_id = random.randint(1000000,9999999)
    try: 
        purchase_orders = PurchaseOrder.objects.get(purchase_order_id = pur_id)
        item_list = PurchaseOrderItem.objects.filter(purchase_order_id = pur_id)
        context = {
                'title': 'Invoice Form',
                'invoice_id': 'INV' + str(inv_id),
                'purchase_order_id': inv_id, 
                'staff_id' : purchase_orders.person_id.person_id,
                'vendor_id': purchase_orders.vendor_id.vendor_id,
                'rows':item_list
            }

        responsesItems = render(request,'Invoice/invoiceform.html',context).content
        return render(request,'Invoice/invoiceform.html',context)

    except Invoice.DoesNotExist:

        context = { 'error': 'The invoice id is invalid !',
                    'title': 'Invoice Form'
            }
        return render(request,'Invoice/invoiceform.html',context)

def invoiceconfirmation(request):

    context = {}
    inv_id = request.POST['invoice_id']
    pur_id = request.POST['purchase_order_id']
    staff_id = request.POST['staff_id']
    vendor_id = request.POST['vendor_id']
    description = request.POST['description']
    inv_stat = request.POST.get('invoice_status',False)
    staff_info = Person.objects.get(person_id = staff_id)
    vendor_info = Vendor.objects.get(vendor_id= vendor_id)
    responses = request.read()
    print(responses)
   
    q= QueryDict(responses)
    
    items_id = q.getlist('item_id')
    print(items_id)
    items_name = q.getlist('item_name')
    print(items_name)
    items_quantity = q.getlist('quantity')
    print(items_quantity)
    items_unit_price = q.getlist('unit_price')
    print(items_unit_price)
    items_total_price = q.getlist('total_price')
    print(items_total_price)


    items = list()

    i = 0
    items_length = len(items_id)
    grand_total = Decimal(0)

    while i < items_length:
        total = Decimal(items_quantity[i]) * Decimal(items_unit_price[i])
        item_table = {
            'item_name': items_name[i],
            'item_id': items_id[i],
            'quantity' : items_quantity[i],
            'unit_price': items_unit_price[i],
            'total_price': total
        }
        items.append(item_table)
        i = i + 1
        grand_total = grand_total + total
    print(items)




    context = {
            'title': 'Invoice Confirmation',
            'purchase_order_id' :pur_id,
            'invoice_id' : inv_id,
            'staff_id' : staff_id,
            'vendor_id' : vendor_id,
            'grand_total': grand_total,
            'rows' : items,
            'staff_info' : staff_info,
            'vendor_info' : vendor_info,
            'description' : description
        }


    return render(request,'Invoice/invoiceconfirmation.html',context)

 
def invoicedetails(request):
    context = {}
    inv_id = request.POST['invoice_id']
    purchase_order_id = request.POST['purchase_order_id']
    staff_id = request.POST['staff_id']
    vendor_id = request.POST['vendor_id']
    description = request.POST['description']
    purchaseorder = get_object_or_404(PurchaseOrder)
    staff_info = Person.objects.get(person_id = staff_id)
    vendor_info = Vendor.objects.get(vendor_id = vendor_id)

    responses = request.read()
    print(responses)
   
    q= QueryDict(responses)
    
    items_id = q.getlist('item_id')
    print(items_id)
    items_name = q.getlist('item_name')
    print(items_name)
    items_quantity = q.getlist('quantity')
    print(items_quantity)
    items_unit_price = q.getlist('unit_price')
    print(items_unit_price)
    items_total_price = q.getlist('total_price')
    print(items_total_price)


    items = list()

    i = 0
    items_length = len(items_id)
    grand_total = Decimal(0)

    while i < items_length:
        total= Decimal(items_quantity[i]) * Decimal(items_unit_price[i])
        item_table = {
            'item_name': items_name[i],
            'item_id': items_id[i],
            'quantity' : items_quantity[i],
            'unit_price': items_unit_price[i],
            'total_price': total
        }
        items.append(item_table)
        i = i + 1
        grand_total = grand_total + total
    print(items)

 

    # push the data to the database 
    current_time = datetime.datetime.now() 
    print(current_time)
    inv_info = Invoice(invoice_id = inv_id, 
                            time_created = current_time,
                            total_price = grand_total, 
                            person_id = staff_info,
                            description = description,
                            vendor_id = vendor_info, 
                            purchase_order_id = purchaseorder,
                            )
    inv_info.save()

    invoice = Invoice.objects.get(invoice_id = inv_id)
    for item in items:
        item_info = Item.objects.get(item_id = item['item_id'])
        inv_item_info = InvoiceItem(invoice_id = invoice, 
                                         item_id = item_info, 
                                         quantity = item['quantity'], 
                                         unit_price = item['unit_price'],
                                         total_price = item['total_price'])
        inv_item_info.save()


    # info pass to html
    context = {
            'title': 'Invoice Details',
           'purchase_order_id' : purchase_order_id,
           'invoice_id' : inv_id,
            'staff_id' : staff_id,
            'vendor_id' : vendor_id,
            'rows' : items,
            'staff_info' : staff_info,
            'vendor_info' : vendor_info,
            'grand_total': grand_total,
            'time_created': current_time,
            'description' : description
        }

    return render(request,'Invoice/invoicedetails.html',context)

def invoicehistorydetails(request):

    print(request.body)
    pk = request.GET['inv_id']
    invoice = Invoice.objects.get(invoice_id = pk)
    items = InvoiceItem.objects.filter(invoice_id = pk)

    print(invoice.person_id)
    context = {

            'title': 'Invoice Details',
            'purchase_order_id' : invoice.purchase_order_id.purchase_order_id,
            'invoice_id' : pk,
            'staff_id' : invoice.person_id.person_id,
            'vendor_id' : invoice.vendor_id.vendor_id,
            'rows' : items,
            'staff_info' : invoice.person_id,
            'vendor_info' : invoice.vendor_id,
            'grand_total': invoice.total_price,
            'time_created': invoice.time_created,
            'description' : invoice.description
        }
  
    return render(request,'Invoice/invoicehistorydetails.html',context)

def invoicehistory(request):

    invoice = Invoice.objects.all()

    context = {
            'title':'Invoice History',
            'rows':invoice
        }
    return render(request,'Invoice/invoicehistory.html',context)
