from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Hotel, Room, Profile, User, Reservation, Pet
from .forms import SignUpForm, ReservatonForm, PetForm, ReservatonRoomForm

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
    form = ReservatonForm (request.POST)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      new_reservation.user_id = request.user.id
      new_reservation.save()
    return redirect ('reservation_index')

  form = ReservatonForm()
  context = {'form': form}
  return render(request, 'main_app/reservation_form.html', context)

class ReservationList(ListView):
    model = Reservation

def room_create_reservation(request, room_id):
  if request.method == 'POST':
    form = ReservatonRoomForm(request.POST)
    if form.is_valid():
      new_reservation = form.save(commit=False)
      new_reservation.user_id = request.user.id
      new_reservation.room_id = room_id
      new_reservation.save()

    return redirect ('reservation_index')

  form = ReservatonRoomForm()
  room = Room.objects.get(id=room_id)
  return render(request, 'main_app/reservation_form.html', {'form': form, 'room': room})
