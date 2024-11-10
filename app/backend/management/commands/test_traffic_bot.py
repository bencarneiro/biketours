import requests
import datetime
from django.core.management.base import BaseCommand
import pytz
import dateparser
from backend.models import *
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # Test.objects.all().delete()

        try:
            test = Test.objects.get(id="test_traffic_bot.py")
        except:
            test = Test(
                id="test_traffic_bot.py"
            )
            test.save()

        try:
            r = requests.get("https://mastodon.social/api/v1/accounts/110194222525068835/statuses")

            now = datetime.datetime.today().replace(tzinfo= pytz.timezone('UTC'))
            last_post_dt = dateparser.parse(r.json()[0]["created_at"]).replace(tzinfo=pytz.utc)
            time_since_last_post = now - last_post_dt
            print(last_post_dt)
            print(now)
            print(time_since_last_post)

            log = f"{round(time_since_last_post.seconds / 60)} minutes since last post"
            if time_since_last_post.seconds < 60 * 60 * 6:
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
                "Test Failure: test_traffic_bot",
                f"{e}",
                "testing@bencarneiro.com",
                ["bencarneiro@gmail.com"],
                fail_silently=False,
            )





# from django.db import models

# # Create your models here.


# class Test(models.Model):
#     id = models.AutoField(primary_key=True)
#     path = models.CharField(max_length=256)

# class TestLog(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
#     created = models.DateTimeField(auto_now=True)
#     passed = models.BooleanField(default=)
#     log = models.TextField(null=True)