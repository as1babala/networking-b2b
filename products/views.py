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
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class admin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_employee
    
class ProductListView( generic.ListView):
    model = Product
    template_name = "products/product_list.html"
    queryset = Product.objects.all() # not adding context here
    context_object_name = "products"
    paginate_by = 3
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = "products/product_create.html"
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse("products:product-list")

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    
class CreateCheckoutSessionView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product.name,
                            },
                            'unit_amount': int(product.price * 100),
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return str(e)

def create_subscription(request, product_id):
    product = Product.objects.get(id=product_id)
    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/') + '?success=true',
        cancel_url=request.build_absolute_uri('/') + '?cancel=true',
        )
    return redirect(session.url, code=303)


class SuccessView(TemplateView):
    def get(self, request, *args, **kwargs):
        # Handle successful payment, e.g., create a subscription
        return HttpResponse("Success!")

class CancelView(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Cancelled.")

@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Perform some action based on the session data
        handle_successful_payment(session)

    return HttpResponse(status=200)

def handle_successful_payment(session):
    # Logic to handle successful payment
    pass

class ProductUpdateView(admin, generic.UpdateView):
    template_name = "products/product_update.html"
    form_class = ProductForm
    queryset = Product.objects.all()
    
    def get_success_url(self):
        return reverse("products:product-list")
     
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(ProductUpdateView, self).form_valid(form)
    
class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "products/product_delete.html"
    queryset = Product.objects.all()
    
    def get_success_url(self):
        return reverse("products:product-list")

class ServicesView(TemplateView):
    template_name = "products/services.html"