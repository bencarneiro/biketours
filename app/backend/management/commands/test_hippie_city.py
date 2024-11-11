from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from backend.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        try:
            test = Test.objects.get(id="test_hippie_city.py")
        except:
            test = Test(
                id="test_hippie_city.py"
            )
            test.save()
        
        try:
            r = requests.get("https://hippie.city")

            if '<h1 class="w3-jumbo">Hippie City Bike Tours</h1>' in r.text:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log="successfully requested homepage at https://hippie.city"
                )
            else:
                log = "Unsuccessfully requested homepage at https://hippie.city"
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                send_mail(
                    "Test Failure: test_hippie_city",
                    f"{log}",
                    "testing@bencarneiro.com",
                    ["bencarneiro@gmail.com"],
                    fail_silently=False,
                )
            new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_hippie_city",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )
