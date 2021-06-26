from django.urls import path
from . import views

urlpatterns = [
  # path('', views.home, name='home')
  # path('rooms/', views.rooms_index, name = 'rooms_index'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]