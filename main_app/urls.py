from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index'),
  path('rooms/<int:pk>', views.RoomDetail.as_view(), name = 'room_detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.profile, name='profile'),
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]