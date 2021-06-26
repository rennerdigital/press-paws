from django.urls import path
from . import views

urlpatterns = [
  # path('', views.home, name='home')
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]