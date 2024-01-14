from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app import settings
import datetime
from django.views.decorators.csrf import csrf_exempt
from backend.models import CheckoutSession

import stripe

# Create your views here.

def home(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "home.html", context)


def success(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "success.html", context)

def checkout(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "checkout.html", context)

def cancel(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "cancel.html", context)

def stripe_webhook(request):
    print(request)
    return JsonResponse({"hi": "hello"})



# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    try:
        product = "price_1OYZ6BI5l5pOpCHBjgUUzhfP"
        quantity=1
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product,
                    'quantity': quantity,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/?session={CHECKOUT_SESSION_ID}',
            cancel_url=f'http://127.0.0.1:8000/cancel/',
        )
        cs = CheckoutSession(
            id = checkout_session.id,
            created = datetime.datetime.now(),
            paid = False
        )
        cs.save()
    except Exception as e:
        return HttpResponse(e)
    print(checkout_session.url)
    return redirect(checkout_session.url)
