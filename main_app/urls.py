from main_app.models import Reservation
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index'),
  path('rooms/<int:pk>', views.RoomDetail.as_view(), name = 'room_detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('reservations/', views.ReservationList.as_view(), name = 'reservation_index'),
  path('reservations/create/', views.create_reservation, name="reservation_create"),
  path('reservations/<int:room_id>/create/', views.room_create_reservation, name="room_reservation_create"),
  path('reservations/<int:pk>/', views.ReservationDetail.as_view(), name="reservation_detail"),
  path('reservations/<int:pk>/delete/', views.ReservationDelete.as_view(), name='delete_reservation'),
  path('reservations/<int:pk>/edit/', views.ReservationUpdate.as_view(), name='edit_reservation'),
  path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
  path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
  path('profile/<int:profile_id>/add_pet/', views.add_pet, name='add_pet'),
  path('pets/<int:pet_id>/add_pet_photo/', views.add_pet_photo, name='add_pet_photo'),
  path('pets/<int:pet_id>/delete_pet_photo/', views.delete_pet_photo, name='delete_pet_photo'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='delete_pet'),
  path('pets/<int:pk>/edit/', views.PetUpdate.as_view(), name='edit_pet'),
]