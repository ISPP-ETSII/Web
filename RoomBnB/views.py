from django.views.decorators.csrf import csrf_exempt

from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from pip.download import user_agent
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from requests import request

from RoomBnB.forms import FlatForm
from RoomBnB.forms import ProfileForm
from RoomBnB.forms import SignUpForm
from RoomBnB.forms import RoomForm
from RoomBnB.models import Flat
from RoomBnB.models import Profile
from RoomBnB.models import Room
from RoomBnB.models import RoomProperties
from RoomBnB.models import FlatReview
from RoomBnB.models import RoomReview
from RoomBnB.models import UserReview
from RoomBnB.models import FlatProperties
from RoomBnB.models import Contract
from RoomBnB.models import Payment
from RoomBnB.forms import ReviewForm
from RoomBnB.models import User
from RoomBnB.forms import SearchFlatForm
from RoomBnB.models import RentRequest
from django.contrib.auth.models import User
from RoomBnB.services import create_flat, create_rent_request, get_flat_details, get_room_details
from django.urls import reverse
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful


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


@login_required
def request_rent_room(request, room_id):
    response = create_rent_request(request.user, room_id)
    return response


@login_required
def requests_list(request):
    my_flats = request.user.profile.flats.all()
    rent_requests_to_me = []

    if my_flats:
        for flat in my_flats:
            rooms = flat.rooms.all()
            if rooms:
                for room in rooms:
                    room_requests = room.rent_requests.all()
                    if room_requests:
                        rent_requests_to_me.append(*room_requests)

    rent_requests_by_me = RentRequest.objects.filter(requester=request.user)

    return render(request, 'request/list.html', {'requests_by_me': rent_requests_by_me,
                                                 'requests_to_me': rent_requests_to_me})


@login_required
def accept_request(request, request_id):
    rent_request = RentRequest.objects.get(pk=request_id)
    room = rent_request.requested
    room.temporal_owner = rent_request.requester
    room.save()

    rent_request.delete()

    return redirect('/requests/list')


@login_required
def deny_request(request, request_id):
    rent_request = RentRequest.objects.get(pk=request_id)

    rent_request.delete()

    return redirect('/requests/list')


def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList}
    return render(request, 'flat/list.html', context)


def listWithKeyword(request, keyword):
    query = Q(title__icontains=keyword)
    query.add(Q(description__icontains=keyword), Q.OR)
    query.add(Q(address__icontains=keyword), Q.OR)
    flatList = Flat.objects.all().filter(query)

    return render(request, 'flat/list.html', {'flatList': flatList})


def listWithProperties(request, keyword, elevator, washdisher, balcony, window, air_conditioner):
    list = []
    res = []
    query = Q(title__icontains=keyword)
    query.add(Q(description__icontains=keyword), Q.OR)
    query.add(Q(address__icontains=keyword), Q.OR)
    flatList = Flat.objects.all().filter(query)
    flatList2 = FlatProperties.objects.all()
    for flat in flatList:
        query2 = Q(elevator=elevator)
        query2.add(Q(washdisher=washdisher), Q.AND)
        query2.add(Q(flat=flat), Q.AND)
        flatList2 = flatList2.filter(query2)
        if flatList2.exists():
            list.append(flat)
    roomList2 = RoomProperties.objects.all()
    query3 = Q(balcony=balcony)
    query3.add(Q(window=window), Q.AND)
    query3.add(Q(air_conditioner=air_conditioner), Q.AND)

    for flat in list:
        roomList = Room.objects.filter(belong_to=flat)
        for room in roomList:
            query3 = Q(balcony=balcony)
            query3.add(Q(window=window), Q.AND)
            query3.add(Q(air_conditioner=air_conditioner), Q.AND)
            query3.add(Q(room=room), Q.AND)
            roomList2 = roomList2.filter(query3)
            if roomList2.exists():
                res.append(flat)

    return render(request, 'flat/list.html', {'flatList': res})


def detail(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    flat_details = get_flat_details(flat)
    rooms = Room.objects.filter(belong_to=flat)
    return render(request, 'flat/detail.html', {'flat': flat, 'flatDetails': flat_details, 'roomList': rooms})


@login_required
def flatCreate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            create_flat(
                form_title=form.cleaned_data.get("title"),
                form_address=form.cleaned_data.get("address"),
                form_description=form.cleaned_data.get("description"),
                form_picture=form.cleaned_data['picture'],
                user=request.user)

            return HttpResponseRedirect('/flats')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FlatForm()

    return render(request, 'flat/create.html', {'form': form})


@login_required
def roomCreate(request, flat_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RoomForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            flat = Flat.objects.get(id=flat_id)
            room = Room(price=form.cleaned_data.get("price"),
                        description=form.cleaned_data.get("description"),
                        picture=form.cleaned_data['picture'],
                        belong_to=flat)
            room.save()

            return HttpResponseRedirect('/flats/' + str(flat_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomForm()

    return render(request, 'room/create.html', {'form': form, 'flatid': flat_id})


@login_required
def profileCreate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            loggedUser = request.user

            profile = Profile(user=loggedUser,
                              avatar=form.cleaned_data['avatar'])
            profile.save()

            return HttpResponseRedirect('/flats')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()

    return render(request, 'profile/create.html', {'form': form})


@login_required
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
    if request.method == 'POST':
        form = SearchFlatForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            elevator = form.cleaned_data.get('elevator')
            washdisher = form.cleaned_data.get('washdisher')
            balcony = form.cleaned_data.get('balcony')
            window = form.cleaned_data.get('window')
            air_conditioner = form.cleaned_data.get('air_conditioner')
            return HttpResponseRedirect(
                '/flats/keyword=' + keyword + '/elevator=' + str(elevator) + '/washdisher=' + str(washdisher)
                + '/balcony=' + str(balcony) + '/window=' + str(window) + '/air_conditioner=' + str(air_conditioner))
    else:
        form = SearchFlatForm()

    """ if request.method == 'POST':
        if request.payment_was_succesful:
            return HttpResponseRedirect( "EL pago se a realizado")
    """
    return render(request, 'index.html', {'form': form})


def detailRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    rentRequest = RentRequest.objects.all()
    flat = Flat.objects.get(id=room.belong_to.id)
    rooms = rooms = Room.objects.filter(belong_to=flat)
    room_details = get_room_details(room)

    return render(request, 'room/detail.html',
                  {'room': room, 'rooms': rooms, 'user': user, 'rentRequest': rentRequest, 'roomDetails': room_details})


def roomReview(request, room_id):
    room = Room.objects.get(id=room_id)
    reviews = RoomReview.objects.filter(room=room)
    return render(request, 'room/review.html', {'roomRev': reviews, 'room': room})


def flatReview(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    review = FlatReview.objects.filter(flat=flat)
    return render(request, 'flat/review.html', {'flatRev': review, 'flat': flat, 'rooms': rooms})


def userReview(request, flat_id, user_id):
    user = User.objects.get(id=user_id)
    flat = Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    review = UserReview.objects.filter(user=user)
    return render(request, 'user/review.html', {'userRev': review, 'flat': flat, 'rooms': rooms})


@login_required
def writeReviewUser(request, user_id, flat_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            rev = UserReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating=form.cleaned_data.get("rating"), user=user)
            rev.save()
            return HttpResponseRedirect('/userReview/' + str(flat_id) + '/' + str(user_id))
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'user/writeReview.html', {'form': form, 'flatid': flat_id, 'userid': user_id})


@login_required
def writeReviewRoom(request, room_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            room = Room.objects.get(id=room_id)
            rev = RoomReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating=form.cleaned_data.get("rating"), room=room)
            rev.save()
            return HttpResponseRedirect('/roomReview/' + str(room_id))
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'room/writeReview.html', {'form': form, 'roomid': room_id})


@login_required
def writeReviewFlat(request, flat_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            flat = Flat.objects.get(id=flat_id)
            rev = FlatReview(title=form.cleaned_data.get("title"), description=form.cleaned_data.get("description"),
                             rating=form.cleaned_data.get("rating"), flat=flat)
            rev.save()
            return HttpResponseRedirect('/flatReview/' + str(flat_id))
    else:
        form = ReviewForm()
    print(form.errors)
    return render(request, 'flat/writeReview.html', {'form': form, 'flatid': flat_id})


def retur(request):
    return render(request, 'index.html')

@csrf_exempt
def paypal_response(request, room_id):
    if request.POST.get('payment_status') == 'Completed':
        print('Entra pago')
        amount = request.POST.get('mc_gross')
        room = Room.objects.get(id=room_id)
        contract = Contract.objects.filter(room=room)[0]
        pay = Payment(amount=amount, contract=contract)
        pay.save()

    return HttpResponse('')


def view_that_asks_for_money(request, room_id):
    room = Room.objects.get(id=room_id)

    # What you want the button to do.
    import random
    paypal_dict = {
        "business": "roombnbispp-facilitator@gmail.com",
        "currency_code": "EUR",
        "amount": room.price,
        "item_name": Room.description,
        "invoice": random.randint(0, 9999999999999),
        "notify_url": 'http://217.216.240.169:8000/paymentroom/1/paypal',
        "return": request.build_absolute_uri(reverse('base')),
        "cancel_return": request.build_absolute_uri(reverse('base')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    # context = {"form": form}

    date_signed = timezone.now()
    flat = Flat.objects.get(id=room.belong_to.id)
    owner = flat.owner
    user = room.temporal_owner
    tenant = Profile.objects.get(user=request.user)
    contract = Contract(date_signed=date_signed, landlord=owner, tenant=tenant, room=room)
    contract.save()

    return render(request, "paypal/payment.html", {'contract': contract, 'form': form})
