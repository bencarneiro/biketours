from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from backend.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        try:
            test = Test.objects.get(id="test_census_maps.py")
        except:
            test = Test(
                id="test_census_maps.py"
            )
            test.save()
        
        try:
            r = requests.get("https://censusmaps.org")

            if '<a href="search">MAKE BEAUTIFUL MAPS</a>' in r.text:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log="successfully requested homepage at https://censusmaps.org"
                )
            else:
                log = "Unsuccessfully requested homepage at https://censusmaps.org"
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                send_mail(
                    "Test Failure: test_census_maps",
                    f"{log}",
                    "testing@bencarneiro.com",
                    ["bencarneiro@gmail.com"],
                    fail_silently=False,
                )
            new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_census_maps",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )
