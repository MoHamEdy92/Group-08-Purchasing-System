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
from app.models import Person,Item,Vendor
from PurchaseOrder.models import PurchaseOrder,PurchaseOrderItem
from DeliveryOrder.models import DeliveryOrder,DeliveryOrderItem
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http.request import QueryDict
from decimal import Decimal
import random
import datetime 


@login_required
def deliveryorderform(request):
    context = {
            'title':'Delivery Order Form'
        }
    context['user'] = request.user

    return render(request,'DeliveryOrder/deliveryorderform.html',context)


@login_required
def fillingdeliveryorder(request):

    context = {}
    pur_id = request.GET['pur_id']
    do_id = random.randint(10000000,99999999)
    user_id = request.user.id
    staff = Person.objects.get(user_id = user_id)

    try: 
        po = PurchaseOrder.objects.get(purchase_order_id = pur_id)
        item_list = PurchaseOrderItem.objects.filter(purchase_order_id = pur_id)
        context = {
                'title': 'Delivery Order Form',
                'delivery_order_id': 'PO' + str(do_id),
                'purchase_order_id': pur_id, 
                'staff_id' : staff.person_id,
                'vendor_id': po.vendor_id.vendor_id,
                'rows':item_list
            }

        return render(request,'DeliveryOrder/deliveryorderform.html',context)

    except PurchaseOrder.DoesNotExist:

        context = { 'error': 'The quotation id is invalid !',
                    'title': 'Delivery Order Form'
            }
        return render(request,'DeliveryOrder/deliveryorderform.html',context)

def deliveryorderconfirmation(request):

    context = {}
    do_id = request.POST['delivery_order_id']
    po_id = request.POST['purchase_order_id']

    user_id = request.user.id
    staff = Person.objects.get(user_id=user_id)
    
    vendor_id = request.POST['vendor_id']
    shipping_inst = request.POST['shipping_inst']
    description = request.POST['description']

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




    context = {
            'title': 'Delivery Order Confirmation',
            'purchase_order_id' : po_id,
            'delivery_order_id' : do_id,
            'staff_id' : staff.person_id,
            'vendor_id' : vendor_id,
            'shipping_inst' : shipping_inst,
            'grand_total': grand_total,
            'rows' : items,
            'staff_info' : staff,
            'vendor_info' : vendor_info,
            'description' : description
        }


    return render(request,'DeliveryOrder/deliveryorderconfirmation.html',context)

 
def deliveryorderdetails(request):
    context = {}
    do_id = request.POST['delivery_order_id']
    po_id = request.POST['purchase_order_id']
    shipping_inst = request.POST['shipping_inst']
    staff_id = request.POST['staff_id']
    vendor_id = request.POST['vendor_id']
    description = request.POST['description']
    po = PurchaseOrder.objects.get(purchase_order_id = po_id)
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
    do_info = DeliveryOrder(delivery_order_id = do_id, 
                            shipping_instructions = shipping_inst, 
                            time_created = current_time,
                            total_price = grand_total, 
                            person_id = staff_info,
                            description = description,
                            vendor_id = vendor_info, 
                            purchase_order_id = po)
    do_info.save()

    delivery_order = DeliveryOrder.objects.get(delivery_order_id = do_id)
    for item in items:
        item_info = Item.objects.get(item_id = item['item_id'])
        do_item_info = DeliveryOrderItem(delivery_order_id = delivery_order, 
                                         item_id = item_info, 
                                         quantity = item['quantity'], 
                                         unit_price = item['unit_price'],
                                         total_price = item['total_price'])
        do_item_info.save()


    # info pass to html
    context = {
            'title': 'Delivery Order Details',
            'purchase_order_id' : po_id,
            'delivery_order_id' : do_id,
            'staff_id' : staff_id,
            'vendor_id' : vendor_id,
            'shipping_inst' : shipping_inst,
            'rows' : items,
            'staff_info' : staff_info,
            'vendor_info' : vendor_info,
            'grand_total': grand_total,
            'time_created': current_time,
            'description' : description
        }

    return render(request,'DeliveryOrder/deliveryorderdetails.html',context)

def deliveryorderhistorydetails(request):

    print(request.body)
    pk = request.GET['do_id']
    delivery_order = DeliveryOrder.objects.get(delivery_order_id = pk)
    items = DeliveryOrderItem.objects.filter(delivery_order_id = pk)

    print(delivery_order.person_id)
    context = {

            'title': 'Delivery Order Details',
            'purchase_order_id' : delivery_order.purchase_order_id.purchase_order_id,
            'delivery_order_id' : pk,
            'staff_id' : delivery_order.person_id.person_id,
            'vendor_id' : delivery_order.vendor_id.vendor_id,
            'shipping_inst' : delivery_order.shipping_instructions,
            'rows' : items,
            'staff_info' : delivery_order.person_id,
            'vendor_info' : delivery_order.vendor_id,
            'grand_total': delivery_order.total_price,
            'time_created': delivery_order.time_created,
            'description' : delivery_order.description
        }
  
    return render(request,'DeliveryOrder/deliveryorderhistorydetails.html',context)

def deliveryorderhistory(request):

    delivery_orders = DeliveryOrder.objects.all()

    context = {
            'title':'delivery Order History',
            'rows':delivery_orders
        }
    return render(request,'DeliveryOrder/deliveryorderhistory.html',context)
