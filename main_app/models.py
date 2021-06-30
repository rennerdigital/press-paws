from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import datetime

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
    people_capacity = models.IntegerField()
    pets_capacity = models.IntegerField()
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
    date_from = models.DateField(default=datetime.date.today)
    date_to = models.DateField(default=(datetime.date.today() + datetime.timedelta(days=1)))
    number_of_guests = models.IntegerField()
    number_of_pets = models.IntegerField()
    number_of_nights = models.IntegerField(validators=[MinValueValidator(1)])
    total_owed = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"reservation from {self.date_from} on {self.date_to}"

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.id})

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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.url