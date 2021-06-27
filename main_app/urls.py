from django.urls import path
from . import views

urlpatterns = [
  # path('', views.home, name='home')
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('profile_create/', views.ProfileCreate.as_view(), name='profile_create'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]