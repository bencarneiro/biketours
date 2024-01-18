from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# abstraction of the auth_user django table
class Customer(AbstractUser):

    class Meta:
        managed = True
        db_table = "customer"


class TourType(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=1024)
    description = models.TextField(null=True, blank=True)
    stripe_price = models.CharField(max_length=256, null=True, blank=True)
    price_in_cents = models.BigIntegerField(null=False, default=0)
    url = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        managed = True
        db_table = "tour_type"


class Tour(models.Model):

    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(TourType, on_delete=models.DO_NOTHING)
    day = models.DateTimeField(null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False)

    @property
    def open_spots(self):
        open_spots = 0
        spots = TourSpot.objects.filter(tour__id=self.id)
        for spot in spots:
            if spot.is_open:
                open_spots += 1
        return open_spots
            
    class Meta:
        managed = True
        db_table = "tour"

class TourRoute(models.Model):

    tour = models.ForeignKey(TourType, on_delete=models.DO_NOTHING)
    geojson = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "tour_route"


class TourSpot(models.Model):

    id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.DO_NOTHING)
    spot_number = models.IntegerField(null=False, blank=False)
    is_open = models.BooleanField(default=True)
    # customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = "tour_spot"


class TourGroup(models.Model):

    id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=512, null=True, blank=True)
    group_size = models.IntegerField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = "tour_group"


class GroupMember(models.Model):

    tour_group = models.ForeignKey(TourGroup, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "group_member"



class CustomerWaiver(models.Model): 

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    filepath = models.CharField(max_length=512, null=False, blank=False)

    class Meta:
        managed = True
        db_table = "customer_waiver"


# class Reservation(models.Model):

#     id = models.AutoField(primary_key=True)
#     tour = models.ForeignKey(Tour, on_delete = models.DO_NOTHING)
#     reservation_data = models.TextField(null=True, blank=True)
#     stripe_invoice_id = models.CharField(max_length=64, null=True, blank=True)
#     stripe_invoice = models.JSONField(null=True, blank=True)
    
#     class Meta:
#         managed = True
#         db_table = "reservation"

class CheckoutSession(models.Model):

    id = models.CharField(max_length=512, primary_key=True)
    created = models.DateTimeField(null=False)
    paid = models.BooleanField(default=False)
    total = models.BigIntegerField(null=True, blank=True)
    tour_data = models.JSONField(null=True, blank=True)
    stripe_data = models.JSONField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "checkout_session"