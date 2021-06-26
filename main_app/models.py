from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(max_length=2)
    price = models.FloatField("Price Per Night ($CAD)")
    description = models.TextField(max_length=250)
    is_dog_friendly = models.BooleanField()
    is_cat_friendly = models.BooleanField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'room_id': self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=10)
    address = models.CharField(max_length=100)
    credit_card = models.IntegerField(max_length=16)

    def __str__(self):
        return self.name


# Create your models here.
# test:sam
# test:renner