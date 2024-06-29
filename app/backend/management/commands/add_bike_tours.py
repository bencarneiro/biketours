from django.core.management.base import BaseCommand
import datetime
from backend.models import Tour, TourSpot, TourType

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        
        counter = 0
        # calendar_object = {}
        day = datetime.date.today()
        while counter < 60:
            # date_str = day.strftime("%Y-%m-%d")
            start = datetime.datetime.combine(day, datetime.time.min)
            # print tmp # 2016-02-03 23:59:59.999999
            end = start + datetime.timedelta(days=1)
            existing_tours = Tour.objects.filter(day__gt=start, day__lt=end)
            print(f"{len(existing_tours)} tours found")
            if len(existing_tours) > 0:
                print(f"TOUR FOUND, skipping {start}")

                day = day + datetime.timedelta(days=1)
                counter += 1
                continue
            # if start.weekday() != 0:
            if True:
                tour_type = TourType.objects.get(id=1)
                tour = Tour(
                    type=tour_type,
                    day= start + datetime.timedelta(hours=9),
                    capacity=6
                )
                tour.save()
                for x in range(6):
                    ts = TourSpot(
                        tour=tour,
                        spot_number=x,
                        is_open=True
                    )
                    ts.save()
            day = day + datetime.timedelta(days=1)
            counter +=1