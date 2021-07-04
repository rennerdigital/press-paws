from typing import List
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Feedback, Hotel, Room, Profile, User, Reservation, Pet, Photo, Feedback
from .forms import SignUpForm, ReservationForm, PetForm, ReservationRoomForm, ReservationUpdateForm
import datetime

from main_app import models

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'annacakecollector'


def home(request):
  return render(request, 'home.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)      
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again'
  form = SignUpForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['phone', 'address', 'credit_card']

    def get_form(self, form_class=None):
      if form_class is None:
        form_class = self.get_form_class()

      form = super(ProfileCreate, self).get_form(form_class)
      form.fields['phone'].widget = forms.TextInput(attrs={'placeholder': '###-###-####'})
      form.fields['credit_card'].widget = forms.TextInput(attrs={'placeholder': '####-####-####-####'})
      return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/profile/'

@login_required
def profile(request):
  try:
    Profile.objects.get(user=request.user)
    profile = Profile.objects.get(user=request.user)
    pet_form = PetForm()
    return render(request, 'main_app/profile.html', {
        'profile': profile,
        'pet_form': pet_form
      })
  except Profile.DoesNotExist:
    profile = None
    return render(request, 'main_app/profile.html', {
      'profile': profile,
      })

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['phone', 'address', 'credit_card']
    success_url = '/profile/'

@login_required
def add_pet(request, profile_id):
  form = PetForm(request.POST)
  if form.is_valid():
    new_pet = form.save(commit=False)
    new_pet.profile_id = profile_id
    new_pet.save()
  return redirect('profile')

@login_required
def add_pet_photo(request, pet_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, key=key, pet_id=pet_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('profile')

@login_required
def delete_pet_photo(request, pet_id):
  pet_photo = Photo.objects.get(pet_id=pet_id)
  s3 = boto3.resource('s3')
  s3.Object(BUCKET, pet_photo.key).delete()
  pet_photo.delete()
  return redirect('profile')


class PetDelete(LoginRequiredMixin, DeleteView):
  model = Pet
  success_url = '/profile/'

class PetUpdate(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = ['name', 'type', 'breed', 'description']
  success_url = '/profile/'

class RoomList(ListView):
    model = Room

class RoomDetail(DetailView):
    model = Room


@login_required
def add_room_photo(request, room_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, key=key, room_id=room_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('room_detail', pk=room_id)

@login_required
def create_reservation(request):
  days_error_message = ""
  error_msg = ""
  if request.method == 'POST':
    form = ReservationForm(request.POST)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      room = Room.objects.get(id=new_reservation.room_id)
      new_reservation.room_id = room.id
      if new_reservation.check_room_capacity() != True:
        error_msg = "Sorry! You either have more pets or people than this room can hold."
      else:
        new_reservation.user_id = request.user.id
        if new_reservation.at_least_one_night() == False:
          days_error_message = "You have to stay for more than one night!"
        else:
          new_reservation.save()
          return redirect ('successful_reservation')

  form = ReservationForm()

  def getDays(date_from, date_to):
    days = []
    day = date_from
    while day < date_to:
      days.append([day.year, day.month -1, day.day ])
      day += datetime.timedelta(days=1)
    return days

  reservations = Reservation.objects.all()
  days = list(map(lambda x: getDays(x.date_from, x.date_to), reservations))
  days = [item for sublist in days for item in sublist]

  context = {
    'form': form,
    'bookedDays': [],
    'error_msg': error_msg,
    'days_error_message': days_error_message
    }
  return render(request, 'main_app/reservation_form.html', context)

class ReservationList(LoginRequiredMixin, ListView):
    model = Reservation
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['date'] = datetime.date.today()
      return context
    def get_queryset(self):
      return Reservation.objects.filter(user=self.request.user.id)

class ReservationDetail(LoginRequiredMixin, DetailView):
    model = Reservation
    def get_queryset(self):
      return Reservation.objects.filter(user=self.request.user.id)
    success_url = '/reservations/'

@login_required
def room_create_reservation(request, room_id):
  days_error_message = ""
  error_msg = ""
  if request.method == 'POST':
    form = ReservationRoomForm(request.POST)
    room = Room.objects.get(id=room_id)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      new_reservation.room_id = room_id
      new_reservation.check_room_capacity()
      if new_reservation.check_room_capacity() != True:
        error_msg = "Sorry! You either have more pets or people than this room can hold."
      else:
        new_reservation.user_id = request.user.id
        room = Room.objects.get(id=new_reservation.room.id)
        if new_reservation.at_least_one_night() == False:
          days_error_message = "You have to stay for more than one night!"
        else:
          new_reservation.save()
          return redirect ('successful_reservation')

  def getDays(date_from, date_to):
    days = []
    day = date_from
    while day < date_to:
      days.append([day.year, day.month -1, day.day ])
      day += datetime.timedelta(days=1)
    return days

  form = ReservationRoomForm()
  room = Room.objects.get(id=room_id)
  room_reservations = Reservation.objects.filter(room_id = room_id)
  days = list(map(lambda x: getDays(x.date_from, x.date_to), room_reservations))
  days = [item for sublist in days for item in sublist]

  return render(request, 'main_app/reservation_form.html', {'form': form, 'room': room, "days_error_message": days_error_message, 'error_msg': error_msg, 'bookedDays': days})

@login_required
def successful_reservation(request):
  reservations = Reservation.objects.filter(user=request.user.id)
  latest_reservation = reservations.order_by("-id").first
  date = datetime.date.today()
  return render(request, 'main_app/reservation_list_success.html', {'reservations': reservations, 'date': date, 'latest_res': latest_reservation})

class ReservationUpdate(LoginRequiredMixin, UpdateView):
  model = Reservation
  form_class = ReservationUpdateForm
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['bookedDays'] = []
    return context

class ReservationDelete(LoginRequiredMixin, DeleteView):
  model = Reservation
  success_url = '/reservations/'

class ContactPage(ListView):
  model = Hotel

class CreateFeedback(CreateView):
  model = Feedback
  fields = ['rating', 'message', 'hotel']

  def form_valid(self, form):
    if self.request.user.is_authenticated:
      form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self):
      next_url = self.request.GET.get("next")
      if next_url:
        return next_url
      return reverse('home')
