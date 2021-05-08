from django.contrib import admin
from .models import CustomUser, Advisor, Booking
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Advisor)
admin.site.register(Booking)