from typing import Any
import stripe
from itertools import count
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum, Avg
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.views import generic
from core.models import *
from .forms import *
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = "products/product_list.html"
    queryset = Product.objects.all() # not adding context here
    context_object_name = "products"
    paginate_by = 2
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = "products/product_create.html"
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse("products:product-list")
    
    
class CreateCheckoutSessionView(CreateView):
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    
    def post(self, request, **args):
            checkout_session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                    'currency': 'usd',
                    'unit_amount': 20000,
                    'product_data': {
                        'name': 'produce',
                        #'images': ['https://i.imgur.com/EHyR2nP.png']
                    },  
                  },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
       
            return JsonResponse({
                'id': checkout_session.id
                
            })

class ProductLandingPageView(TemplateView):
    template_name='products/landing_page.html'
    
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name = 'testing product')
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            
        })
        return super().get_context_data(**kwargs)
    
           
def product_home(request):
    return render(request, 'products/first_stripe.html')

def create_checkout_session(request):
	if request.method == "POST":
		YOUR_DOMAIN = 'http://127.0.0.1:8000'
		stripe.api_key = 'sk_test' #replace with your Stripe API key
		data = json.loads(request.body)

		customer = stripe.Customer.create(
			email=request.user.email)
		try:
			checkout_session = stripe.checkout.Session.create(
				payment_method_types=['card'],
				line_items=[
					{
						'price': data["product_id"],
						'quantity': 1,
					}
				],
				mode='subscription',
				success_url=YOUR_DOMAIN + '/success',
				cancel_url=YOUR_DOMAIN + '/cancel',
				customer_email = customer.email,
				)
			return JsonResponse({'id': checkout_session.id})
		except Exception as e:
			return JsonResponse({'error': (e.args[0])}, status =400)
	return JsonResponse({'error':'No GET request allowed.'})

def success_request(request):
	messages.info(request, "You have successfully subscribed.") 
	return redirect("main:dashboard")

def cancel_request(request):
	messages.info(request, "Payment Failed. Please try again.") 
	return redirect("main:pricing")