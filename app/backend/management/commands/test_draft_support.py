

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from backend.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        try:
            test = Test.objects.get(id="test_draft_support.py")
        except:
            test = Test(
                id="test_draft_support.py"
            )
            test.save()
        
        try:
            r = requests.get("https://draft.support")

            if '<h1> PLAYER STATS  2021-2023</h1>' in r.text:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log="successfully requested homepage at https://draft.support"
                )
            else:
                log = "Unsuccessfully requested homepage at https://draft.support"
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                send_mail(
                    "Test Failure: test_draft_support",
                    f"{log}",
                    "testing@bencarneiro.com",
                    ["bencarneiro@gmail.com"],
                    fail_silently=False,
                )
            new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_draft_support",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )
