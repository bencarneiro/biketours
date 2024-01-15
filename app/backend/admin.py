from django.contrib import admin
from .models import Customer, Tour, TourType, TourGroup, TourSpot, TourRoute, GroupMember, CheckoutSession, CustomerWaiver 
# Register your models here.
admin.site.register(Customer)
admin.site.register(Tour)
admin.site.register(TourType)
admin.site.register(TourGroup)
admin.site.register(TourSpot)
admin.site.register(TourRoute)
admin.site.register(GroupMember)
admin.site.register(CheckoutSession)
admin.site.register(CustomerWaiver)