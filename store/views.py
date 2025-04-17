from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from .middlewares import auth,guest
from django.template.context_processors import request
from django.core.mail import send_mail

from .models import *           #euta euta garna naparos vanerw ailelai sabai tables import


def front(request):
    
    return render(request,"base/front.html")

def home(request):
    products = Products.objects.all().order_by('-uid')[0:3]
    prod = Products.objects.all().order_by('-uid')[3:5]

    context = {
        'products': products,
        'prod':prod,
    }
    print(context)
    return render(request, "base/home.html", context)

def shop(request):
    products = Products.objects.all().order_by('-uid')
   
    context = {
        'products': products,
        
    }
    print(context)
    return render(request, "base/shop.html", context)


def product_search(request):
    query = request.GET.get('q', '')
    
    if query:
        product = Products.objects.filter(name__icontains=query).first()  
        
        if product:
            return redirect('product_detail', slug=product.slug)
        else:
            return redirect('Shop')
        
def product_detail(request,slug):
    productdetails=Products.objects.get(slug=slug)          #form models.py      #get to bring single row from product model
    data={
        'productdetails':productdetails
    }
    return render(request,"base/product_des.html",data)

def product_category(request, slug):
    category = Category.objects.get(slug=slug)  
    products_by_cat = Products.objects.filter(category=category).order_by('-created_at')  
    data = {
        'category': category,  
        'products_by_cat': products_by_cat,  
    }
    return render(request, 'base/product_cat.html', data)
       #redirect same page


