

import requests
import datetime
from django.core.management.base import BaseCommand
import pytz
import dateparser
from backend.models import *
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **kwargs):


        try:
            test = Test.objects.get(id="test_shrek_bot.py")
        except:
            test = Test(
                id="test_shrek_bot.py"
            )
            test.save()

        try:
            r = requests.get("https://bencarneiro.com/api/v1/accounts/112853697332395541/statuses")

            now = datetime.datetime.today().replace(tzinfo= pytz.timezone('UTC'))
            last_post_dt = dateparser.parse(r.json()[0]["created_at"]).replace(tzinfo=pytz.utc)
            time_since_last_post = now - last_post_dt
            print(last_post_dt)
            print(now)
            print(time_since_last_post)

            log = f"{round(time_since_last_post.seconds / 3600)} hours since last post"
            if time_since_last_post.seconds < 60 * 60 * 48:
                new_log = TestLog(
                    test=test,
                    passed=True,
                    log=log
                )
                new_log.save()
            else:
                new_log = TestLog(
                    test=test,
                    passed=False,
                    log=log
                )
                new_log.save()
        except Exception as e:
            send_mail(
                "Test Failure: test_shrek_bot",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )


