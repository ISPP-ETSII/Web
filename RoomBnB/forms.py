from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from RoomBnB.models import Room
from RoomBnB.models import User
from RoomBnB.models import Flat
from django.db import models


class FlatForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
    description = forms.CharField(label='Description', max_length=500)
    picture = forms.ImageField()


class RoomForm(forms.Form):
    description = forms.CharField(label='Description', max_length=500)
    price = forms.FloatField(required=True, max_value=1000, min_value=0)
    picture = forms.ImageField()


class ProfileForm(forms.Form):
    avatar = forms.ImageField()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        help_texts = {
            'username': None,
        }


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


class SearchFlatForm(forms.Form):
    keyword = forms.CharField(max_length=100)
    elevator = forms.BooleanField(required=False, initial=False)
    washdisher = forms.BooleanField(required=False, initial=False)
    balcony = forms.BooleanField(required=False, initial=False)
    window = forms.BooleanField(required=False, initial=False)
    air_conditioner = forms.BooleanField(required=False, initial=False)

