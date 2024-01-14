from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app import settings
import datetime
from django.views.decorators.csrf import csrf_exempt
from backend.models import CheckoutSession
import json
import stripe

def process_checkout(session_id):

    session = stripe.checkout.Session.retrieve(
        session_id,
    )
    print(session)
    if session.payment_status == "paid": 
        cs = CheckoutSession.objects.get(id=session.id)
        cs.paid = True
        cs.total = session.amount_total
        cs.save()
    pi = session.payment_intent
    payment_intent = stripe.PaymentIntent.retrieve(pi)
    print("\n\n\n\n\n\n\n")
    print(payment_intent)
    return session.customer
# Create your views here.

def home(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "home.html", context)


def success(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    stripe_checkout_session_id = request.GET['session']
    print(stripe_checkout_session_id)
    customer = process_checkout(stripe_checkout_session_id)
    context = {"latest_question_list": customer}
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
        print(request.POST['tour_id'])
        if "tour_id" in request.POST and request.POST['tour_id']:
            tour_id = request.POST['tour_id']
        else:
            tour_id = ""

        if "tour_price" in request.POST and request.POST['tour_price']:
            tour_price = request.POST['tour_price']
        else:
            tour_price = "price_1OYZ6BI5l5pOpCHBjgUUzhfP"

        if "quantity" in request.POST and request.POST['quantity']:
            quantity = request.POST['quantity']
        else:
            quantity = 1

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': tour_price,
                    'quantity': quantity,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/?session={CHECKOUT_SESSION_ID}',
            cancel_url=f'http://127.0.0.1:8000/cancel/',
        )
        tour_data = {
            "tour_id": tour_id,
            "tour_price": tour_price,
            "quantity": quantity
        }
        cs = CheckoutSession(
            id = checkout_session.id,
            created = datetime.datetime.now(),
            paid = False,
            tour_data = tour_data
        )
        cs.save()
    except Exception as e:
        return HttpResponse(e)
    print(checkout_session.url)

    return redirect(checkout_session.url)
