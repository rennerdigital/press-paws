from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
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
    phone = models.IntegerField()
    address = models.CharField(max_length=100)
    credit_card = models.IntegerField()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.id})

class Reservation(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    number_of_guests = models.IntegerField()
    number_of_pets = models.IntegerField()
    number_of_nights = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"reservation from {self.date_from} on {self.date_to}"

    class Meta:
        ordering = ['date_from']

TYPES = (
    ('D', 'Dog'),
    ('C', 'Cat')
)

class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=1,
        choices=TYPES,
        default=TYPES[0][0]
    )
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
