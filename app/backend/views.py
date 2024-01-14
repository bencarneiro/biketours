from django.shortcuts import render, redirect
from django.http import JsonResponse
from app import settings
from django.views.decorators.csrf import csrf_exempt

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
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OYZ6BI5l5pOpCHBjgUUzhfP',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='127.0.0.1:8000/success/',
            cancel_url='127.0.0.1:8000/cancel/',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url)
