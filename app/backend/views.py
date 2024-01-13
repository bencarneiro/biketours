from django.shortcuts import render

# Create your views here.

def home(request):
    # latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": "hi"}
    return render(request, "home.html", context)