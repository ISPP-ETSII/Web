from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CreditCard(models.Model):
    owner = models.CharField(max_length=50)
    code = models.CharField(max_length=16)
    cvv = models.CharField(max_length=3)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    credit_card = models.OneToOneField(CreditCard, on_delete=models.CASCADE)


class Flat(models.Model):
    description = models.TextField(max_length=500)
    pictures = models.ImageField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Room(models.Model):
    description = models.TextField(max_length=500)
    price = models.FloatField()
    pictures = models.ImageField()
    temporal_owner = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    belong_to = models.ForeignKey(Flat, on_delete=models.CASCADE)


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

