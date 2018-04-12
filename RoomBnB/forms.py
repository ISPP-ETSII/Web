from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from RoomBnB.models import Room, FlatProperties
from RoomBnB.models import User
from RoomBnB.models import Flat
from django.db import models


class FlatForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100)
    address = forms.CharField(label=_('Address'), max_length=100)
    description = forms.CharField(label=_('Description'), max_length=500)
    picture = forms.ImageField(label=_('Image'))



class FlatPropertiesForm(ModelForm):
    class Meta:
        model = FlatProperties
        fields = ['elevator','washdisher']
        #fields = '__all__'
        #widgets = {'flat': forms.HiddenInput()}

class RoomForm(forms.Form):
    description = forms.CharField(label=_('Description'), max_length=500)
    price = forms.FloatField(label=_('Price'), required=True, max_value=1000, min_value=0)
    picture = forms.ImageField(label=_('Title'))


class ProfileForm(forms.Form):
    avatar = forms.ImageField(label=_('Title'))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    email = forms.EmailField(label=_('Email'), max_length=254)

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

    title = forms.CharField(label=_('Title'), max_length=50)
    description = forms.CharField(label=_('Description'), max_length=500)
    rating = forms.CharField(label=_('Rating'), max_length=1)


class UserReviewForm(ReviewForm):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FlatReviewForm(ReviewForm):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)


class RoomReviewForm(ReviewForm):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class SearchFlatForm(forms.Form):
    keyword = forms.CharField(max_length=100)
    elevator = forms.BooleanField(label=_('Elevator'), required=False, initial=False)
    washdisher = forms.BooleanField(label=_('Dishwasher'), required=False, initial=False)
    balcony = forms.BooleanField(label=_('Balcony'), required=False, initial=False)
    window = forms.BooleanField(label=_('Window'), required=False, initial=False)
    air_conditioner = forms.BooleanField(label=_('Air conditioner'), required=False, initial=False)


class ContractForm(forms.Form):
    agree = forms.BooleanField(label=_('I agree'), required=True, initial=False)


