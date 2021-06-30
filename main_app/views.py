from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Hotel, Room, Profile, User, Reservation, Pet
from .forms import SignUpForm, ReservationForm, PetForm, ReservationRoomForm
import datetime

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

class ProfileCreate(CreateView):
    model = Profile
    fields = ['phone', 'address', 'credit_card']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/profile/'

def profile(request):
    profile = Profile.objects.get(user=request.user)
    pet_form = PetForm()
    return render(request, 'main_app/profile.html', {
        'profile': profile,
        'pet_form': pet_form
      })

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['phone', 'address', 'credit_card']
    success_url = '/profile/'

def add_pet(request, profile_id):
  form = PetForm(request.POST)
  if form.is_valid():
    new_pet = form.save(commit=False)
    new_pet.profile_id = profile_id
    new_pet.save()
  return redirect('profile')

class PetDelete(DeleteView):
  model = Pet
  success_url = '/profile/'

class PetUpdate(UpdateView):
  model = Pet
  fields = ['name', 'type', 'breed', 'description']
  success_url = '/profile/'

class RoomList(ListView):
    model = Room

class RoomDetail(DetailView):
    model = Room

def create_reservation(request):
  if request.method == 'POST':
    form = ReservationForm (request.POST)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      new_reservation.user_id = request.user.id
      room = Room.objects.get(id=new_reservation.room.id)
      delta = new_reservation.date_to - new_reservation.date_from
      new_reservation.number_of_nights = delta.days
      new_reservation.total_owed = room.price* new_reservation.number_of_nights 
      new_reservation.save()
    return redirect ('reservation_index')

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
  print(days)

  context = {
    'form': form,
    'bookedDays': days
    }
  return render(request, 'main_app/reservation_form.html', context)

class ReservationList(ListView):
    model = Reservation
    def get_queryset(self):
      return Reservation.objects.filter(user=self.request.user.id)

class ReservationDetail(DetailView):
    model = Reservation
    def get_queryset(self):
      return Reservation.objects.filter(user=self.request.user.id)
    success_url = '/reservations/'

def room_create_reservation(request, room_id):
  error_message = ""
  funny_message = ""
  alternate_funny_message = ""
  if request.method == 'POST':
    form = ReservationRoomForm(request.POST)
    room = Room.objects.get(id=room_id)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      if new_reservation.number_of_guests <= room.people_capacity and new_reservation.number_of_pets <= room.pets_capacity:
        new_reservation.user_id = request.user.id
        new_reservation.room_id = room_id
        room = Room.objects.get(id=new_reservation.room.id)
        delta = new_reservation.date_to - new_reservation.date_from
        new_reservation.number_of_nights = delta.days
        new_reservation.total_owed = room.price* new_reservation.number_of_nights 
        new_reservation.save()
        return redirect ('reservation_index')
      elif new_reservation.number_of_guests > room.people_capacity and new_reservation.number_of_pets > room.pets_capacity:
        alternate_funny_message = "Sorry, that's too many people and pets for this room!"
        print(alternate_funny_message)
      elif new_reservation.number_of_pets > room.pets_capacity:
        funny_message = "Sorry, that's too many pets for this room!"
        print(funny_message)
      else:
        error_message = "You have exceeded the maximum capacity for this room. Please check out another room or bring fewer people :-)"
        print(error_message)

  form = ReservationRoomForm()
  room = Room.objects.get(id=room_id)
  return render(request, 'main_app/reservation_form.html', {'form': form, 'room': room, 'error_message': error_message, 'funny_message': funny_message, 'alternate_funny_message': alternate_funny_message})


class ReservationUpdate(UpdateView):
  model = Reservation
  fields = ['date_from', 'date_to', 'number_of_guests', 'number_of_pets', 'number_of_nights']
  # success_url = '/reservations/'
  
class ReservationDelete(DeleteView):
  model = Reservation
  success_url = '/reservations/'




