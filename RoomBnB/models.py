from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Properties(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    DEGREES = (
        ('1', 'Enfermeria'),
        ('2', 'Ing. Informatica'),
        ('3', 'Medicina'),
        ('4', 'Biologia'),
        ('5', 'Arquitectura'),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    smoker = models.CharField(max_length=1, choices=RATINGS)
    neat = models.CharField(max_length=1, choices=RATINGS)
    sporty = models.CharField(max_length=1, choices=RATINGS)
    gamer = models.CharField(max_length=1, choices=RATINGS)
    sociable = models.CharField(max_length=1, choices=RATINGS)
    active = models.CharField(max_length=1, choices=RATINGS)
    degree = models.CharField(max_length=1, choices=DEGREES)


class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=50)
    code = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)


class Flat(models.Model):
    title = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flats')


class Room(models.Model):
    description = models.TextField(max_length=500)
    price = models.FloatField()
    temporal_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    belong_to = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='rooms')


class RentRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_requests')
    creation_date = models.DateField(auto_now_add=True)
    requested = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rent_requests')
    accepted = models.BooleanField(default=False)


class Contract(models.Model):
    picture = models.ImageField()
    date_signed = models.DateField(auto_now_add=True)
    landlord = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='landlord')
    tenant = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='tenant')
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)


class Payment(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.DO_NOTHING)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, default=None)


class Review(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    date = models.DateField(auto_now_add=True)
    rating = models.CharField(max_length=1, choices=RATINGS)


class UserReview(Review):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FlatReview(Review):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)


class RoomReview(Review):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField()


class FlatImage(Image):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)


class RoomImage(Image):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
