from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from datetime import datetime

#database
from app.models import Person,Item,Vendor
from Quotation.models import Quotation, QuotationItem
from PurchaseOrder.models import PurchaseOrder,PurchaseOrderItem

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http.request import QueryDict
from decimal import Decimal
import random
import datetime 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@login_required
def purchaseorderform(request):
    context = {
            'title':'Purchase Order Form'
        }

    return render(request,'PurchaseOrder/purchaseorderform.html',context)


@login_required
def fillingpurchaseorder(request):

    context = {}
    quo_id = request.GET['quo_id']
    po_id = 1001

    purchaseorders = PurchaseOrder.objects.all()
    numberpo = len(purchaseorders)
    po_id = int(po_id) + int(numberpo) 

    staff_id = request.user
    staff = Person.objects.get(user_id = staff_id)

    try: 

        purchaseorder = PurchaseOrder.objects.get(quotation_id = quo_id)
        print(purchaseorder)

        context = { 'error': 'The purchase order is already Issued! Purchase Order Number: ' + purchaseorder.purchase_order_id,
                    'title': 'Purchase Order Form'
            }
        return render(request,'PurchaseOrder/purchaseorderform.html',context)

    except PurchaseOrder.DoesNotExist:
        try:

            quotations = Quotation.objects.get(quotation_id = quo_id)
            item_list = QuotationItem.objects.filter(quotation_id = quo_id)
            context = {
                    'title': 'Purchase Order Form',
                    'purchase_order_id': 'PO' + str(po_id),
                    'quotation_id': quo_id, 
                    'staff' : staff,
                    'vendor_id': quotations.vendor_id.vendor_id,
                    'rows':item_list
                }

            responsesItems = render(request,'PurchaseOrder/purchaseorderform.html',context).content
            return render(request,'PurchaseOrder/purchaseorderform.html',context)

        except Quotation.DoesNotExist:

            context = { 'error': 'The quotation id is invalid !',
                        'title': 'Purchase Order Form'
                }
            return render(request,'PurchaseOrder/purchaseorderform.html',context)

def purchaseorderconfirmation(request):

    context = {}
    po_id = request.POST['purchase_order_id']
    quotation_id = request.POST['quotation_id']
    staff_id = request.user.id 
    staff = Person.objects.get(user_id = staff_id)
    vendor_id = request.POST['vendor_id']
    shipping_inst = request.POST['shipping_inst']
    description = request.POST['description']
    vendor_info = Vendor.objects.get(vendor_id = vendor_id)
    
    #extract information from item table
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




    context = {
            'title': 'Purchase Order Confirmation',
            'quotation_id' : quotation_id,
            'purchase_order_id' : po_id,
            'vendor_id' : vendor_id,
            'shipping_inst' : shipping_inst,
            'grand_total': grand_total,
            'rows' : items,
            'staff' : staff,
            'vendor_info' : vendor_info,
            'description' : description
        }


    return render(request,'PurchaseOrder/purchaseorderconfirmation.html',context)

 
def purchaseorderdetails(request):
    context = {}

    po_id = request.POST['purchase_order_id']
    quotation_id = request.POST['quotation_id']
    shipping_inst = request.POST['shipping_inst']

    vendor_id = request.POST['vendor_id']
    description = request.POST['description']

    staff_id = request.user.id 
    staff = Person.objects.get(user_id = staff_id)
    quotation = Quotation.objects.get(quotation_id = quotation_id)
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

 

    # push the Purchase Order data to the database 
    current_time = datetime.datetime.now() 
    print(current_time)
    po_info = PurchaseOrder(purchase_order_id = po_id, 
                            shipping_instructions = shipping_inst, 
                            time_created = current_time,
                            total_price = grand_total, 
                            person_id = staff,
                            description = description,
                            vendor_id = vendor_info, 
                            quotation_id = quotation)
    po_info.save()

    # push the Purchase Order item data to the database
    purchase_order = PurchaseOrder.objects.get(purchase_order_id = po_id)
    for item in items:
        item_info = Item.objects.get(item_id = item['item_id'])
        po_item_info = PurchaseOrderItem(purchase_order_id = purchase_order, 
                                         item_id = item_info, 
                                         quantity = item['quantity'], 
                                         unit_price = item['unit_price'],
                                         total_price = item['total_price'])
        po_item_info.save()


    #sending email to vendor
    x = PrettyTable()

    x.field_names = ["Item ID","Item Name","Quantity","Unit Price","Total Price"]

    for item in items:
        x.add_row([item['item_id'],item['item_name'],item['quantity'],item['unit_price'],item['total_price']])

    subject = 'PURCHASE ORDER INFORMATION: '+ po_id
    message = 'This is the Purchase Order Information: \n'+'Person In Charge: '+staff.person_name+'\n'+'Ship to:'+staff.person_address+ '\n' +'Purchase Order Number: ' + po_id + '\n'+'Quotation ID: ' + quotation.quotation_id + '\n'+'Time Issued: ' + str(current_time) + '\n'+'Vendor ID: ' + vendor_id + '\n'+'Description: ' + description + '\n'+'Shipping Instructions: ' + shipping_inst + '\n'+ str(x) +'\n'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [vendor_info.vendor_email,]
    send_mail( subject, message, email_from, recipient_list )

    # info pass to html
    context = {
            'title': 'Purchase Order Details',
            'quotation_id' : quotation_id,
            'purchase_order_id' : po_id,
            'vendor_id' : vendor_id,
            'shipping_inst' : shipping_inst,
            'rows' : items,
            'staff' : staff,
            'vendor_info' : vendor_info,
            'grand_total': grand_total,
            'time_created': current_time,
            'description' : description
        }

    return render(request,'PurchaseOrder/purchaseorderdetails.html',context)

def purchaseorderhistorydetails(request):

    print(request.body)
    pk = request.GET['po_id']
    purchase_order = PurchaseOrder.objects.get(purchase_order_id = pk)
    items = PurchaseOrderItem.objects.filter(purchase_order_id = pk)
    staff = Person.objects.get(person_id=purchase_order.person_id.person_id)

    context = {

            'title': 'Purchase Order Details',
            'quotation_id' : purchase_order.quotation_id.quotation_id,
            'purchase_order_id' : pk,
            'shipping_inst' : purchase_order.shipping_instructions,
            'rows' : items,
            'staff' : staff,
            'vendor_info' : purchase_order.vendor_id,
            'grand_total': purchase_order.total_price,
            'time_created': purchase_order.time_created,
            'description' : purchase_order.description
        }
  
    return render(request,'PurchaseOrder/purchaseorderhistorydetails.html',context)

def purchaseorderhistory(request):

    purchase_orders = PurchaseOrder.objects.all()

    context = {
            'title':'Purchase Order History',
            'rows':purchase_orders
        }
    return render(request,'PurchaseOrder/purchaseorderhistory.html',context)
