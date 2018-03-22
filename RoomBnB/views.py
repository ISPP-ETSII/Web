from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from pip.download import user_agent
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from RoomBnB.forms import FlatForm

from RoomBnB.forms import ProfileForm
from RoomBnB.forms import SignUpForm
from RoomBnB.models import Flat
from RoomBnB.models import Profile
from RoomBnB.models import Room
from RoomBnB.models import CreditCard
from RoomBnB.models import FlatReview
from RoomBnB.models import RoomReview
from RoomBnB.models import UserReview
from RoomBnB.forms import ReviewForm
from RoomBnB.models import User

from RoomBnB.services import create_flat


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            profile = Profile(user=user)
            profile.save()

            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList}
    return render(request, 'flat/list.html', context)


def detail(request, flat_id):
    flat=Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    return render(request, 'flat/detail.html', {'flat': flat,'roomList':rooms})

def flatCreate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            create_flat(form_title=form.cleaned_data.get("title"),
                       form_address=form.cleaned_data.get("address"),
                       form_description=form.cleaned_data.get("description"),
                       user=request.user)

            return HttpResponseRedirect('/flats')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FlatForm()

    return render(request, 'flat/create.html', {'form': form})

def profileCreate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST,request.FILES)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            loggedUser=request.user

            creditcard = CreditCard(owner=form.cleaned_data['owner'],code=form.cleaned_data['code'],cvv=form.cleaned_data['cvv'])
            CreditCard.save(creditcard)
            profile = Profile(user=loggedUser,avatar=form.cleaned_data['avatar'],credit_card=creditcard)
            profile.save()


            return HttpResponseRedirect('/flats')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()

    return render(request, 'profile/create.html', {'form': form})

def flatDelete(request, flat_id):
    flatList = Flat.objects.all()
    context = {'flatList': flatList}
    flat = Flat.objects.get(id=flat_id)
    Flat.delete(flat)

    return render(request, 'flat/list.html', context)

@login_required
def root(request):
    return render(request, template_name='root.html')

def base(request):
    return render(request, template_name='index.html')

def detailRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'room/detail.html', {'room': room})

def roomReview(request, room_id):
    room = Room.objects.get(id=room_id)
    reviews = RoomReview.objects.filter(room = room)
    return render(request, 'room/review.html', {'roomRev': reviews, 'room': room})

def flatReview(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    review = FlatReview.objects.filter(flat = flat)
    return render(request, 'flat/review.html', {'flatRev': review, 'flat': flat})

def userReview(request, user_id):
    user= User.objects.get(id = user_id)
    review = UserReview.objects.filter(user = user)
    return render(request, 'user/review.html', {'userRev': review, 'user': user})

def writeReviewUser(request, user_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = user_id)
            rev = UserReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating = form.cleaned_data.get("rating"), user = user)
            rev.save()
            return HttpResponseRedirect('/userReview/'+ str(user_id))
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'user/writeReview.html', {'form': form, 'userid': user_id})

def writeReviewRoom(request, room_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            room = Room.objects.get(id = room_id)
            rev = RoomReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating = form.cleaned_data.get("rating"), room = room)
            rev.save()
            return HttpResponseRedirect('/roomReview/'+ str(room_id))
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'room/writeReview.html', {'form': form, 'roomid': room_id})

def writeReviewFlat(request, flat_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            flat = Flat.objects.get(id = flat_id)
            rev = FlatReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating= form.cleaned_data.get("rating"), flat = flat)
            rev.save()
            return HttpResponseRedirect('/flatReview/'+ flat_id)
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'flat/writeReview.html', {'form': form, 'flatid': flat_id})
