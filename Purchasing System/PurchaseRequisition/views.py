from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from PurchaseRequisition.models import PurchaseRequisition, PurchaseRequisitionItem
from app.models import Person,Item
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from datetime import datetime
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http.request import QueryDict
from decimal import Decimal
import random
import datetime 


@login_required
def purchaserequisitionform(request):
    
    pr_id = random.randint(10000000,99999999)
    user_id = request.user.id
    person = Person.objects.get(user_id = user_id)

    context = {
            'title':'Purchase Requisition Form',
            'person_id': person.person_id,
            'purchase_requisition_id':'PR' + str(pr_id),
  
        }
    context['user'] = request.user

 
    return render(request,'PurchaseRequisition/purchaserequisitionform.html',context)



def purchaserequisitionconfirmation(request):

    context = {}
    pr_id = request.POST['purchase_requisition_id']
    person_id= request.POST['person_id']

    responses = request.read()
    print(responses)

    q = QueryDict(responses)

    items_id = q.getlist('item_id')
    print(items_id)
    items_name = q.getlist('item_name')
    print(items_name)
    description = q.getlist('description')
    print(items_name)
    quantity = q.getlist('quantity')
    print(quantity)
    unit_price = q.getlist('unit_price')
    print(unit_price)
    total_price = q.getlist('total_price')
    print(total_price)

    items = list()

    i = 0
    items_length = len(items_id)
    grand_total = Decimal(0)

    while i < items_length:
        total= Decimal(quantity[i]) * Decimal(unit_price[i])
        item_table = {
            'item_name': items_name[i],
            'item_id': items_id[i],
            'quantity' : quantity[i],
            'description': description[i],
            'unit_price': unit_price[i],
            'total_price': total
        }
        items.append(item_table)
        i = i + 1
        grand_total = grand_total + total
    print(items)

    context = {
            'title': 'Purchase Requisition Confirmation',
            'purchase_requisition_id' : pr_id,
            'person_id' : person_id,
            'grand_total': grand_total,
            'rows' : items,
  
        }

    return render(request,'PurchaseRequisition/purchaserequisitionconfirmation.html',context)

 

   
def purchaserequisitiondetails(request):
    context = {}
    pr_id = request.POST['purchase_requisition_id']
    staff_id = request.POST['person_id']
    print(staff_id)
    staff= Person.objects.get(person_id = staff_id)
    


    responses = request.read()
    print(responses)
   
    q= QueryDict(responses)
    
    items_id = q.getlist('item_id')
    print(items_id)
    items_name = q.getlist('item_name')
    print(items_name)
    description = q.getlist('description')
    print(items_name)
    quantity = q.getlist('quantity')
    print(quantity)
    unit_price = q.getlist('unit_price')
    print(unit_price)
    total_price = q.getlist('total_price')
    print(total_price)



    items = list()

    i = 0
    items_length = len(items_id)
    grand_total = Decimal(0)

    while i < items_length:
        total= Decimal(quantity[i]) * Decimal(unit_price[i])
        item_table = {
            'item_name': items_name[i],
            'item_id': items_id[i],
            'description': description[i],
            'quantity' : quantity[i],
            'unit_price': unit_price[i],
            'total_price': total
        }
        items.append(item_table)
        i = i + 1
        grand_total = grand_total + total
    print(items)

 

    # push the data to the database 
    current_time = datetime.datetime.now() 
    print(current_time)
    pr_info = PurchaseRequisition(pr_id = pr_id, 
                            person_id = staff,
                            time_created = current_time,
                            total_price = grand_total, 
                            description = description,
   
                        )
    pr_info.save()

    purchase_requisition = PurchaseRequisition.objects.get(pr_id = pr_id)
    for item in items:
        
        itemitem =Item(item_id = item['item_id'], item_name = item['item_name']  )
        itemitem.save()
        pr_item_info = PurchaseRequisitionItem(pr_id = purchase_requisition, 
                                         item_id = itemitem, 
                                         quantity = item['quantity'], 
                                         unit_price = item['unit_price'])
        pr_item_info.save()


    # info pass to html
    context = {
            'title': 'Purchase Requisition Details',
            'purchase_requisition_id' : pr_id,
            'staff' : staff,
            'rows' : items,
            'grand_total': grand_total,
            'time_created': current_time,

        }

    return render(request,'PurchaseRequisition/purchaserequisitiondetails.html',context)

def purchaserequisitionhistorydetails(request):

    print(request.body)
    pk = request.GET['pr_id']
    purchase_requisition = PurchaseRequisition.objects.get(pr_id = pk)
    items = PurchaseRequisitionItem.objects.all().filter(pr_id = pk)

    print(purchase_requisition.person_id)
    
    context = {

            'title': 'Purchase Requisition Details',
            'purchase_requisition_id' : pk,
            'staff_id' : purchase_requisition.person_id.person_id,
            'rows' : items,
            'staff_info' : purchase_requisition.person_id,
            'grand_total': purchase_requisition.total_price,
            'time_created': purchase_requisition.time_created,
            'description' : purchase_requisition.description
        }
  
    return render(request,'PurchaseRequisition/purchaserequisitionhistorydetails.html',context)



def purchaserequisitionhistory(request):

    purchase_requisitions = PurchaseRequisition.objects.all()
    print(purchase_requisitions)

    context = {
            'title':'Purchase Requisition History',
            'rows':purchase_requisitions
        }
    return render(request,'PurchaseRequisition/purchaserequisitionhistory.html',context)

