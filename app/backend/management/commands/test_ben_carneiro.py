

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import requests
from backend.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        try:
            test = Test.objects.get(id="test_ben_carneiro.py")
        except:
            test = Test(
                id="test_ben_carneiro.py"
            )
            test.save()
        
        try:
            r = requests.get("https://its.bencarneiro.com")

            if '<title>Ben Carneiro</title>' in r.text:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log="successfully requested homepage at https://its.bencarneiro.com"
                )
            else:
                log = "Unsuccessfully requested homepage at https://its.bencarneiro.com"
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                send_mail(
                    "Test Failure: test_ben_carneiro",
                    f"{log}",
                    "testing@bencarneiro.com",
                    ["bencarneiro@gmail.com"],
                    fail_silently=False,
                )
            new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_ben_carneiro",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )
