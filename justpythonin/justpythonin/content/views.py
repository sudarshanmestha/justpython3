import stripe
import json
import stripe.webhook
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stripe._error import SignatureVerificationError 
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from .models import Course
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Course.objects.filter(active=True)

class CourseDetailView(generic.DetailView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()
    context_object_name = "course"
    
    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            # "has_access" : has_access
        })
        return context

class UserProductListView(LoginRequiredMixin, generic.ListView):
    template_name = "content/user_products.html"
    
    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)
    
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs["slug"])
        domain = "https://www.justpython.in"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        customer = None  #initialy we set customer id none for bcs customer id should be same each time
        customer_email=None
        if request.user.is_authenticated:
            if request.user.stripe_customer_id:  
                customer= request.user.stripe_customer_id  #here we assigning stripe customerid
            else:
                # If no, create a new customer in Stripe and update the user's stripe_customer_id
                customer_email = request.user.email
                stripe_customer = stripe.Customer.create(email=customer_email)
                customer = stripe_customer.id
                # Update the user's stripe_customer_id
                request.user.stripe_customer_id = customer
                request.user.save()
    
        session = stripe.checkout.Session.create(
            customer=customer,  #2 created
            # customer_email=customer_email,
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': course.name,
                        },
                        'unit_amount': course.price,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=domain + reverse("success"),
            cancel_url=domain + reverse("content:course-list"),
            metadata={
                "product_id" : course.id
            }
            
            
        )
        return redirect(session.url, code=303)

class SuccessView(generic.TemplateView):
    template_name = "content/success.html"    
    
    
@csrf_exempt
def stripe_webhook(request, *args, **kwargs):
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
    payload = request.body.decode('utf-8')
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    try:
        event = stripe.Event.construct_from(
            json.loads(payload),
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET  
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)   
    except SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=400)
    
    
    if event["type"] == CHECKOUT_SESSION_COMPLETED:
        print(event) 
        session = event["data"]["object"]
        product_id = session["metadata"]["product_id"]
        course = Course.objects.get(id=product_id)
        
        stripe_customer_id = session["customer"]
        try:
            user = User.objects.get(stripe_customer_id=stripe_customer_id)
            user.userlibrary.courses.add(course)
            print("course added")
            # give access to this product
        except User.DoesNotExist:
            # assign the customer_id to the corredsponding user
            stripe_customer_email = session["customer_details"]["email"]
            try:
                user = User.objects.get(email=stripe_customer_email)
                print("The user doesn't have a stripe customer id", user.email)
                user.stripe_customer_id = stripe_customer_id
                user.save()
                user.userlibrary.courses.add(course)
                print("course added")
                
                
            # give access to this product
                       # Give access to this product
            except User.DoesNotExist:
                print("user does not exist")
                pass
        
    
    #listen for successful payments
    
    #who paid for what?
    
    # give access to the user for the product they purchased
    
    return HttpResponse()