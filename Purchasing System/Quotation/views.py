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
from Quotation.models import Quotation,QuotationItem
from RequestForQuotation.models import RequestForQuotation,RequestForQuotationItem
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http.request import QueryDict
from decimal import Decimal
import random
import datetime 



@login_required
def quotationform(request):
    context = {
            'title':'Quotation Form'
        }
    context['user'] = request.user

    return render(request,'Quotation/quotationform.html',context)


@login_required
def fillingquotation(request):

    context = {}
    re_of_quo_id = request.GET['re_of_quo_id']
    quo_id = random.randint(1000000,9999999)
    user_id  = request.user.id
    staff = Person.objects.get(user_id = user_id)
    try: 
        request_for_quotations = RequestForQuotation.objects.get(request_for_quotation_id = re_of_quo_id)
        item_list = RequestForQuotationItem.objects.filter(request_for_quotation_id = re_of_quo_id)
        context = {
                'title': 'Quotation Form',
                'quotation_id': 'QUO' + str(quo_id),
                'request_for_quotation_id': re_of_quo_id, 
                'staff_id' : staff.person_id,
                'vendor_id': request_for_quotations.vendor_id.vendor_id,
                'rows':item_list
            }
        return render(request,'Quotation/quotationform.html',context)

    except RequestForQuotation.DoesNotExist:

        context = { 'error': 'The request for quotation id is invalid !',
                    'title': 'Quotation Form'
            }
        return render(request,'Quotation/quotationform.html',context)

def quotationconfirmation(request):

    context = {}
    quo_id = request.POST['quotation_id']
    request_for_quotation_id = request.POST['request_for_quotation_id']
    user_id  = request.user.id
    staff = Person.objects.get(user_id = user_id)

    vendor_id = request.POST['vendor_id']
    description = request.POST['description']
    vendor_info = Vendor.objects.get(vendor_id = vendor_id)
    
    responses = request.read()
    print(responses)
   
    q= QueryDict(responses)
    
    items_id = q.getlist('item_id')
    items_name = q.getlist('item_name')
    items_quantity = q.getlist('quantity')
    items_unit_price = q.getlist('unit_price')
    items_total_price = q.getlist('total_price')


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
            'title': 'Quotation Confirmation',
            'request_for_quotation_id' : request_for_quotation_id,
            'quotation_id' : quo_id,
            'staff_id' : staff.person_id,
            'vendor_id' : vendor_id,
            'grand_total': grand_total,
            'rows' : items,
            'staff_info' : staff,
            'vendor_info' : vendor_info,
            'description' : description
        }


    return render(request,'Quotation/quotationconfirmation.html',context)

 
def quotationdetails(request):
    context = {}
    quo_id = request.POST['quotation_id']
    request_for_quotation_id = request.POST['request_for_quotation_id']
    staff_id = request.POST['staff_id']
    vendor_id = request.POST['vendor_id']
    description = request.POST['description']
    request_for_quotation = RequestForQuotation.objects.get(request_for_quotation_id = request_for_quotation_id)
    staff_info = Person.objects.get(person_id = staff_id)
    vendor_info = Vendor.objects.get(vendor_id = vendor_id)

    responses = request.read()
    print(responses)
   
    q= QueryDict(responses)
    
    items_id = q.getlist('item_id')
    items_name = q.getlist('item_name')
    items_quantity = q.getlist('quantity')
    items_unit_price = q.getlist('unit_price')
    items_total_price = q.getlist('total_price')
    items_reference_id = q.getlist('ref_id')


    items = list()

    i = 0
    items_length = len(items_id)
    grand_total = Decimal(0)

    while i < items_length:
        total= Decimal(items_quantity[i]) * Decimal(items_unit_price[i])
        item_table = {
            'item_name': items_name[i],
            'item_id': items_id[i],
            'ref_id' : items_reference_id[i],
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
    quo_info = Quotation(quotation_id = quo_id, 
                            time_created = current_time,
                            total_price = grand_total, 
                            person_id = staff_info,
                            description = description,
                            vendor_id = vendor_info, 
                            request_for_quotation_id = request_for_quotation)
    quo_info.save()

    quotation = Quotation.objects.get(quotation_id = quo_id)
    for item in items:
        item_info = Item.objects.get(item_id = item['item_id'])
        quo_item_info = QuotationItem(quotation_id = quotation, 
                                         item_id = item_info, 
                                         total_price = item['total_price'],
                                         quantity = item['quantity'], 
                                         ref_id = item['ref_id'],
                                         unit_price = item['unit_price'])
        quo_item_info.save()


    # info pass to html
    context = {
            'title': 'Quotation Details',
            'request_for_quotation_id' : request_for_quotation_id,
            'quotation_id' : quo_id,
            'staff_id' : staff_id,
            'vendor_id' : vendor_id,
            'rows' : items,
            'staff_info' : staff_info,
            'vendor_info' : vendor_info,
            'grand_total': grand_total,
            'time_created': current_time,
            'description' : description
        }

    return render(request,'Quotation/quotationdetails.html',context)

def quotationhistorydetails(request):

    print(request.body)
    pk = request.GET['quo_id']
    quotation = Quotation.objects.get(quotation_id = pk)
    items = QuotationItem.objects.filter(quotation_id = pk)

    print(quotation.person_id)
    context = {

            'title': 'Quotation Details',
            'request_for_quotation_id' : quotation.request_for_quotation_id.request_for_quotation_id,
            'quotation_id' : pk,
            'staff_id' : quotation.person_id.person_id,
            'vendor_id' : quotation.vendor_id.vendor_id,
            'rows' : items,
            'staff_info' : quotation.person_id,
            'vendor_info' : quotation.vendor_id,
            'grand_total': quotation.total_price,
            'time_created': quotation.time_created,
            'description' : quotation.description
        }
  
    return render(request,'Quotation/quotationhistorydetails.html',context)

def quotationhistory(request):

    quotations = Quotation.objects.all()

    context = {
            'title':'Quotation History',
            'rows':quotations
        }
    return render(request,'Quotation/quotationhistory.html',context)
