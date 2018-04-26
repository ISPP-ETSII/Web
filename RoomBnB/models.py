from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile/', default='profile/generic/default.png')


class UserProperties(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    DEGREES = (
        ('1', _('Nursing')),
        ('2', _('Computer Engineering')),
        ('3', _('Medicine')),
        ('4', _('Biology')),
        ('5', _('Architecture')),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    smoker = models.BooleanField(_('Smoker'), default=False)
    pets = models.BooleanField(_('Pets'), default=False)
    sporty = models.CharField(_('Sporty'), max_length=1, choices=RATINGS)
    gamer = models.CharField(_('Gamer'), max_length=1, choices=RATINGS)
    sociable = models.CharField(_('Sociable'), max_length=1, choices=RATINGS)
    degree = models.CharField(_('Degree'), max_length=1, choices=DEGREES)


class Flat(models.Model):
    title = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    picture = models.ImageField(upload_to='flat/', default='flat/generic/default.jpg')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='flats')


class FlatProperties(models.Model):
    flat = models.OneToOneField(Flat, on_delete=models.CASCADE)
    elevator = models.BooleanField(_('Elevator'), default=False)
    washdisher = models.BooleanField(_('Dishwasher'), default=False)


class Room(models.Model):
    description = models.TextField(max_length=500)
    price = models.FloatField()
    picture = models.ImageField(upload_to='room/', default='room/generic/default.jpg')
    temporal_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    belong_to = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='rooms')


class RoomProperties(models.Model):
    BEDS = (
        ('1', _('Couple')),
        ('2', _('Single')),
        ('3', _('Sofa')),
        ('4', _('None')),
    )

    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    balcony = models.BooleanField(_('Balcony'), default=False)
    window = models.BooleanField(_('Window'), default=False)
    air_conditioner = models.BooleanField(_('Air conditioner'), default=False)
    bed = models.CharField(_('Bed'), max_length=1, choices=BEDS, default=2)


class RentRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_requests')
    creation_date = models.DateField(auto_now_add=True)
    requested = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rent_requests')
    accepted = models.BooleanField(default=False)


class Contract(models.Model):
    text = models.TextField()
    date_signed = models.DateField(auto_now_add=True)
    landlord = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='landlord')
    tenant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tenant', null=True)
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
