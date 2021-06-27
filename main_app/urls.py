from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index'),
  path('rooms/<int:pk>', views.RoomDetail.as_view(), name = 'room_detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
  path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
  path('profile/<int:profile_id>/add_pet/', views.add_pet, name='add_pet'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='delete_pet'),
  path('pets/<int:pk>/edit/', views.PetUpdate.as_view(), name='edit_pet'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]