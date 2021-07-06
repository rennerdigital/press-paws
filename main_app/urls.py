from main_app.models import Reservation
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path('', views.home, name='home'),
  path('hotel/<int:pk>/add_feedback/', views.CreateFeedback.as_view(), name="feedback_create"),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index'),
  path('rooms/<int:pk>', views.RoomDetail.as_view(), name = 'room_detail'),
  path('rooms/<int:room_id>/add_room_photo/', views.add_room_photo, name='add_room_photo'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('reservations/', views.ReservationList.as_view(), name = 'reservation_index'),
  path('reservations/create', views.ReservationCreate.as_view(), name = 'reservation_create'),
  path('reservations/<int:room_id>/create/', views.ReservationRoomCreate.as_view(), name = 'room_reservation_create'),
  path('reservations/success/', views.successful_reservation, name="successful_reservation"),
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
  path('contact/', views.ContactPage.as_view(), name='contact'),
]

urlpatterns += staticfiles_urlpatterns()
