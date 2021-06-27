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
  path('rooms/', views.RoomList.as_view(), name = 'rooms_index')
]