import os
from datetime import timezone

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from RoomBnB.forms import *
from RoomBnB.models import *
from django.contrib.auth.models import User
from RoomBnB.services import create_flat, create_profile, create_rent_request, get_user_details, get_flat_details, get_room_details, get_flats_filtered


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            create_profile(user, '')

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
    pending_contracts = []

    if my_flats:
        for flat in my_flats:
            rooms = flat.rooms.all()
            if rooms:
                for room in rooms:
                    room_requests = room.rent_requests.all()
                    if room_requests:
                        rent_requests_to_me.append(*room_requests)

    rent_requests_by_me = RentRequest.objects.filter(requester=request.user)

    for room in Room.objects.filter(temporal_owner=request.user):
        contracts = Contract.objects.filter(room=room)
        for contract in contracts:
            if contract.tenant is None:
                pending_contracts.append(room)

    for room in Room.objects.filter(belong_to__owner__user=request.user):
        if room.temporal_owner is not None and room not in pending_contracts:
            try:
                Contract.objects.get(room=room)
            except ObjectDoesNotExist:
                pending_contracts.append(room)

    return render(request, 'request/list.html', {'requests_by_me': rent_requests_by_me,
                                                 'requests_to_me': rent_requests_to_me,
                                                 'pending_contracts': pending_contracts})


@login_required
def accept_request(request, request_id):
    rent_request = RentRequest.objects.get(pk=request_id)
    room = rent_request.requested
    room.temporal_owner = rent_request.requester
    room.save()

    rent_request.delete()

    return redirect('/contracts/sign/' + str(room.id))


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
    flats_filtered = get_flats_filtered(keyword, elevator, washdisher, balcony, window, air_conditioner)

    return render(request, 'flat/list.html', {'flatList': flats_filtered})


def detail(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    flat_details = get_flat_details(flat)
    availableRooms = Room.objects.filter(belong_to=flat, temporal_owner=None)
    notAvailableRooms = set(Room.objects.filter(belong_to=flat)) - set(availableRooms)
    direccion= flat.address.split() #Separo la cadena en palabras creando una lista
    direc= '+'.join(direccion) #Uno la lista con +  porque asi lo tiene que recibir la url de google maps

    #separo los numeros de las palabras para no mostrar la direccion exacta, solamente la calle
    di=[]
    nu=[]
    for d in direc:
        try:
            nu.append(float(d))
        except ValueError:
            di.append(d)
    #Este metodo me a separado cada palabra en un caracter
    direcc=''.join(di) # me junta los caracteres por palabras

    mapkey= os.environ.get('MAPKEY')
    print(mapkey)
    print(direcc)

    return render(request, 'flat/detail.html', {'mapkey':mapkey,'direccion':direcc ,'flat': flat, 'flatDetails': flat_details, 'roomAvailableList':availableRooms, 'roomNotAvailableList': notAvailableRooms})


@login_required
def flatCreate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            flat = create_flat(
                form_title=form.cleaned_data.get("title"),
                form_address=form.cleaned_data.get("address"),
                form_description=form.cleaned_data.get("description"),
                form_picture=form.cleaned_data['picture'],
                user=request.user)

            return HttpResponseRedirect('/flats/' + str(flat.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FlatForm()

    return render(request, 'flat/create.html', {'form': form})


@login_required
def editFlatProperties(request,flat_id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatPropertiesForm(request.POST)
        # check whether it's valid:
        print("prueba3")
        if form.is_valid():

            flat = Flat.objects.get(id=flat_id)
            flatProperties = FlatProperties.objects.get(flat=flat)


            flatProperties.washdisher = form.cleaned_data['washdisher']
            flatProperties.elevator = form.cleaned_data['elevator']
            flatProperties.save()



            return HttpResponseRedirect('/flats/'+ str(flat_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        flat = Flat.objects.get(id=flat_id)
        flatProperties = FlatProperties.objects.get(flat=flat)
        form = FlatPropertiesForm(instance=flatProperties)

    return render(request, 'flat/updateProperties.html', {'form': form,'flat_id':flat_id})


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

            return HttpResponseRedirect('/rooms/' + str(room.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomForm()

    return render(request, 'room/create.html', {'form': form, 'flatid': flat_id})


@login_required
def editRoomProperties(request,room_id):
    room = Room.objects.get(id=room_id)
    roomProperties = RoomProperties.objects.get(room=room)

    if request.method == 'POST':
        form = RoomPropertiesForm(request.POST)
        if form.is_valid():
            roomProperties.balcony = form.cleaned_data.get('balcony')
            roomProperties.window = form.cleaned_data.get('window')
            roomProperties.air_conditioner = form.cleaned_data.get('air_conditioner')
            roomProperties.bed = form.cleaned_data.get('bed')
            roomProperties.save()

            return HttpResponseRedirect('/rooms/'+ str(room_id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomPropertiesForm(instance=roomProperties)

    return render(request, 'room/updateProperties.html', {'form': form,'room_id':room_id})


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
def editUserProperties(request):
    profile = Profile.objects.get(user=request.user)
    profileProperties = get_user_details(profile)

    if request.method == 'POST':
        form = UserPropertiesForm(request.POST)
        if form.is_valid():
            profileProperties.smoker = form.cleaned_data.get('smoker')
            profileProperties.pets = form.cleaned_data.get('pets')
            profileProperties.sporty = form.cleaned_data.get('sporty')
            profileProperties.gamer = form.cleaned_data.get('gamer')
            profileProperties.sociable = form.cleaned_data.get('sociable')
            profileProperties.degree = form.cleaned_data.get('degree')
            profileProperties.save()

            return HttpResponseRedirect('/profile/' + str(request.user.id))

    else:
        form = UserPropertiesForm(instance=profileProperties)

    return render(request, 'profile/update.html', {'form': form,'user_id':request.user.id})


@login_required
def showUserProperties(request, user_id):
    profile = Profile.objects.get(user=user_id)
    profileProperties = get_user_details(profile)

    return render(request, 'profile/detail.html', {'userProperties': profileProperties})


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


def terms_and_conditions(request):
    return render(request, 'tyc.html')


def detailRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    user = room.temporal_owner
    profile = Profile.objects.get(user=user)
    profileProperties = get_user_details(profile)
    room_details = get_room_details(room)
    rentRequest = RentRequest.objects.all()
    flat = Flat.objects.get(id=room.belong_to.id)
    rooms = Room.objects.filter(belong_to=flat)


    return render(request, 'room/detail.html',
                  {'room': room, 'rooms': rooms, 'rentRequest': rentRequest, 'roomDetails': room_details, 'userProperties': profileProperties, 'profile':profile})


def roomReview(request, room_id):
    room = Room.objects.get(id=room_id)
    reviews = RoomReview.objects.filter(room=room)
    return render(request, 'room/review.html', {'roomRev': reviews, 'room': room})


def flatReview(request, flat_id):
    flat = Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    user = request.user

    show_review_button = False
    for room in rooms:
        if user == room.temporal_owner:
            show_review_button = True
            break

    review = FlatReview.objects.filter(flat=flat)
    return render(request, 'flat/review.html', {'flatRev': review, 'flat': flat, 'rooms': rooms, 'showReviewButton': show_review_button})


def userReview(request, flat_id, user_id):
    user = User.objects.get(id=user_id)
    flat = Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    review = UserReview.objects.filter(user=user)

    show_review_button = False
    for room in rooms:
        if user == room.temporal_owner or user == flat.owner.user:
            show_review_button = True
            break

    return render(request, 'user/review.html', {'userRev': review, 'flat': flat, 'userToReview': user, 'rooms': rooms, 'showReviewButton': show_review_button})


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


@login_required
def signContract(request, room_id):
    room = Room.objects.get(id = room_id)
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            try:
                # Tenant is signing the contract
                contract = Contract.objects.get(room=room)
                contract.tenant = request.user
                contract.save()
            except ObjectDoesNotExist:
                # A new contract
                contract = Contract.objects.create(room=room,
                                                   text=request.POST.get('text'),
                                                   landlord=request.user)
                contract.save()

            return HttpResponseRedirect('/requests/list')
    else:
        form = ContractForm()
    return render(request, 'contract/create.html', {'form': form, 'room': room})


@login_required
def paymentList(request):
    contracts=Contract.objects.all().filter(tenant=request.user)
    paymentList = Payment.objects.all()
    date=timezone.now().month
    list=[]
    pendientes=[]
    rooms_id=[]


    for n in contracts:
        if len(paymentList)!=0:
            for pay in paymentList:
                if pay.contract == n:
                    list.append(pay)
                else:
                    pendientes.append(n)
                    rooms_id.append(n.room.id)
        else:
            pendientes.append(n)
            rooms_id.append(n.room.id)


    return render(request, 'payment/list.html', {'paymentList': list,'rooms_id': rooms_id, 'pendientes': pendientes ,'date': date})


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
        "notify_url": request.build_absolute_uri('paypal'),
        "return": request.build_absolute_uri(reverse('base')),
        "cancel_return": request.build_absolute_uri(reverse('base')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}

    return render(request, "paypal/payment.html", context)



