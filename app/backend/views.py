from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app import settings
import datetime
from django.views.decorators.csrf import csrf_exempt
from backend.models import CheckoutSession, Tour, TourSpot
import json
import stripe
from django.views.generic.base import RedirectView

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

    qty_to_reserve = int(cs.tour_data['quantity'])
    tour_spots = TourSpot.objects.filter(tour__id=int(cs.tour_data['tour_id']))
    for spot in tour_spots:
        if spot.is_open and qty_to_reserve > 0:
            spot.is_open = False
            spot.save()
            qty_to_reserve -= 1

    return session.customer

# Create your views here.

def home(request):
    counter = 0
    calendar_object = {}
    day = datetime.date.today()
    while counter < 31:
        date_str = day.strftime("%Y-%m-%d")
        print(date_str)
        start = datetime.datetime.combine(day, datetime.time.min)
        # print tmp # 2016-02-03 23:59:59.999999
        end = start + datetime.timedelta(days=1)
        this_days_tours = Tour.objects.filter(day__gt=start, day__lt=end).order_by('day')
        calendar_object[start] = this_days_tours
        counter += 1
        day = day + datetime.timedelta(days=1)
    # next_month = datetime.date.today() + datetime.timedelta(days=31)
    # test = Tour.objects.filter(day__lt=next_month)
    context = {"calendar": calendar_object}
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # context = {"latest_question_list": "hi"}
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

def barton(request):
    context = {}
    return render(request, "barton.html", context)

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


def calendar(request):
    counter = 0
    calendar_object = {}
    day = datetime.date.today()
    while counter < 31:
        date_str = day.strftime("%Y-%m-%d")
        print(date_str)
        start = datetime.datetime.combine(day, datetime.time.min)
        # print tmp # 2016-02-03 23:59:59.999999
        end = start + datetime.timedelta(days=1)
        this_days_tours = Tour.objects.filter(day__gt=start, day__lt=end).order_by('day')
        calendar_object[start] = this_days_tours
        counter += 1
        day = day + datetime.timedelta(days=1)
    # next_month = datetime.date.today() + datetime.timedelta(days=31)
    # test = Tour.objects.filter(day__lt=next_month)
    context = {"calendar": calendar_object}
    return render(request, "calendar.html", context)


favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)