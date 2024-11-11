from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from backend.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        try:
            test = Test.objects.get(id="test_roadway_report.py")
        except:
            test = Test(
                id="test_roadway_report.py"
            )
            test.save()
        
        try:
            r = requests.get("https://roadway.report")

            if '<title>Roadway Fatalities 2001-2022</title>' in r.text:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log="successfully requested homepage at https://roadway.report"
                )
            else:
                log = "Unsuccessfully requested homepage at https://roadway.report"
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                send_mail(
                    "Test Failure: test_roadway_report",
                    f"{log}",
                    "testing@bencarneiro.com",
                    ["bencarneiro@gmail.com"],
                    fail_silently=False,
                )
            new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_roadway_report",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )
