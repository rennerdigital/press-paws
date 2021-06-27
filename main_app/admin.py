# from main_app.forms import ReservatonForm
from django.contrib import admin
from .models import Hotel, Room, Profile, Reservation

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Profile)
admin.site.register(Reservation)