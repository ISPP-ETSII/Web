from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='pics/profile/', default='pics/profile/default.png')


class UserProperties(models.Model):
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
    smoker = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    sporty = models.CharField(max_length=1, choices=RATINGS)
    gamer = models.CharField(max_length=1, choices=RATINGS)
    sociable = models.CharField(max_length=1, choices=RATINGS)
    degree = models.CharField(max_length=1, choices=DEGREES)


class Flat(models.Model):
    title = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    picture = models.ImageField(upload_to='pics/flat/', default='pics/flat/default.jpg')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='flats')


class FlatProperties(models.Model):
    flat = models.OneToOneField(Flat, on_delete=models.CASCADE)
    elevator = models.BooleanField(default=False)
    washdisher = models.BooleanField(default=False)


class Room(models.Model):
    description = models.TextField(max_length=500)
    price = models.FloatField()
    picture = models.ImageField(upload_to='pics/room/', default='pics/room/default.png')
    temporal_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    belong_to = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='rooms')


class RoomProperties(models.Model):
    BEDS = (
        ('1', 'Couple'),
        ('2', 'Single'),
        ('3', 'Sofa'),
        ('4', 'None'),
    )

    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    balcony = models.BooleanField(default=False)
    window = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=False)
    bed = models.CharField(max_length=1, choices=BEDS, default=2)


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
