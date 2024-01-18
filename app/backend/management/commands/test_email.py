from django.core.management.base import BaseCommand
from django.core.mail import send_mail
# from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        send_mail(
            "Confirmation - Your Bike Tour",
            "Here is the message.",
            "biketours@bencarneiro.com",
            ["bencarneiro@gmail.com"],
            fail_silently=False,
        )
        print("email sent")