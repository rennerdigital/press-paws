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

class ReservatonForm(ModelForm):
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget = forms.Select(attrs={"class": "choice"}),
        )
    class Meta:
        model = Reservation
        fields = ['room', 'date_from', 'date_to', 'number_of_guests', 'number_of_pets', 'number_of_nights']

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'type', 'breed', 'description']
