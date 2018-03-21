from django import forms
from RoomBnB.models import Room
from RoomBnB.models import User
from RoomBnB.models import Flat
from django.db import models


class FlatForm(forms.Form):
    address = forms.CharField(label='Address', max_length=100)
    description = forms.CharField(label='Description', max_length=500)

class ReviewForm(forms.Form):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    title = forms.CharField(label='title', max_length=50)
    description = forms.CharField(label='description', max_length=500)
    rating = forms.CharField(label='rating', max_length=1)

class UserReviewForm(ReviewForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FlatReviewForm(ReviewForm):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)

class RoomReviewForm(ReviewForm):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)



    #class Meta:
     #   models = Flat
     #  fields = ['description','pictures','owner']