from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import request
from main_app.models import Pet
from django import forms
from django.db.models.enums import Choices
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import Widget
from django.shortcuts import redirect
from django.utils.regex_helper import Choice
from .models import Reservation, Room

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )

class ReservationForm(ModelForm):
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget = forms.Select(attrs={"class": "choice"}),
        )
    class Meta:
        model = Reservation
        fields = ['room', 'date_from', 'date_to', 'number_of_guests', 'number_of_pets']

    def clean(self):
        cleaned_data=super(ReservationForm,self).clean()
        number_of_guests = cleaned_data.get('number_of_guests')
        number_of_pets = cleaned_data.get('number_of_pets')
        room = cleaned_data.get("room")
        date_to = cleaned_data.get("date_to")
        date_from = cleaned_data.get("date_from")
        if number_of_guests < 1 or number_of_pets < 1:
            raise forms.ValidationError("We accept one or more guest and pet")
        if number_of_guests > room.people_capacity and number_of_pets > room.pets_capacity:
            raise forms.ValidationError("This is way too many pets and people for this room!")
        elif number_of_pets > room.pets_capacity:
            raise forms.ValidationError("Sorry! That's too many pets for this room. Try another!")
        elif number_of_guests > room.people_capacity:
            raise forms.ValidationError("That's too many people for this room!")
        else:
            delta = date_to - date_from
            if delta.days < 1:
                raise forms.ValidationError("You have to stay longer!")
            else:
                return cleaned_data

class ReservationRoomForm(ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['date_from', 'date_to', 'number_of_guests', 'number_of_pets']

    def clean(self):
        cleaned_data=super(ReservationRoomForm,self).clean()
        number_of_guests = cleaned_data.get('number_of_guests')
        number_of_pets = cleaned_data.get('number_of_pets')
        room = cleaned_data.get("room")
        date_to = cleaned_data.get("date_to")
        date_from = cleaned_data.get("date_from")
        if number_of_guests < 1 or number_of_pets < 1:
            raise forms.ValidationError("We accept one or more guest and pet")
        if number_of_guests > room.people_capacity and number_of_pets > room.pets_capacity:
            raise forms.ValidationError("This is way too many pets and people for this room!")
        elif number_of_pets > room.pets_capacity:
            raise forms.ValidationError("Sorry! That's too many pets for this room. Try another!")
        elif number_of_guests > room.people_capacity:
            raise forms.ValidationError("That's too many people for this room!")
        else:
            delta = date_to - date_from
            if delta.days < 1:
                raise forms.ValidationError("You have to stay longer!")
            else:
                return cleaned_data


class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'breed', 'description']

class ReservationRoomForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_from', 'date_to', 'number_of_guests', 'number_of_pets']

