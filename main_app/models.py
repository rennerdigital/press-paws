from django.db import models
from django.db.models.base import Model
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
    date_from = models.DateField()
    date_to = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1, message="At least 1 guest")])
    number_of_pets = models.IntegerField(validators=[MinValueValidator(1, message="At least 1 pet")])
    number_of_nights = models.IntegerField(blank=True, null=True)
    total_owed = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"reservation from {self.date_from} on {self.date_to}"

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['date_from']
    
    def upto_capacity(self):
        return self.number_of_guests <= self.room.people_capacity and self.number_of_pets <= self.room.pets_capacity
    
    def over_capacity(self):
        return self.number_of_guests > self.room.people_capacity and self.number_of_pets > self.room.pets_capacity
    
    def pets_over_capacity(self):
        return self.number_of_pets > self.room.pets_capacity

    def people_over_capacity(self):
        return self.number_of_guests > self.room.people_capacity

    def check_room_capacity(self):
        self.room = Room.objects.get(id=self.room_id)
        if self.upto_capacity():
            return True
        else:
            return False
    
    def at_least_one_night(self):
        delta = self.date_to - self.date_from
        if delta.days >= 1:
            return True
        else:
            return False

    def calculate_nights(self):
        self.room = Room.objects.get(id=self.room_id)
        delta = self.date_to - self.date_from
        self.number_of_nights = delta.days
        return self.number_of_nights
    
    def calculate_price(self):
        self.room = Room.objects.get(id=self.room_id)
        delta = self.date_to - self.date_from
        self.number_of_nights = delta.days
        self.total_owed = self.room.price * self.number_of_nights
        return self.total_owed

    def save(self, *args, **kwargs):
        self.calculate_nights()
        self.calculate_price()
        super(Reservation, self).save(*args, **kwargs)


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
    key = models.CharField(max_length=200)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.url

RATINGS= (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)

class Feedback(models.Model):
    rating = models.CharField(
        max_length=1,
        choices=RATINGS,
        default=RATINGS[0][0]
    )
    message = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.created)