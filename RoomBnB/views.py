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


User.objects.all().delete()
User(username="damserfer", first_name="Damian", last_name="Serrano Fernandez", last_login=timezone.now(), password="pbkdf2_sha256$100000$7A2Auxc1wT9A$zOrLubd7KlN6cfPH9nZ322S2n8AYHGawSJbYXvuxRJQ=",email="damian@gmail.com").save()
User(username="frasanvel1", first_name="Javier", last_name="Santos Velazquez", last_login=timezone.now(), password="pbkdf2_sha256$100000$oEzewmmGTjyT$xhBw3UmmCBvugvI8Tc1Ax6iL+WA5AvZRFF/oMx36BJI=",email="frasanvel1@gmail.com").save()
User(username="alepolhal", first_name="Alejandro", last_name="Polvillo Hall", last_login=timezone.now(), password="pbkdf2_sha256$100000$4UA2r8wfvzwt$IjMLHNx7Pfmx3d0YoYh4lmvC5eVbzg7Autt/QuhPji0=",email="alepolhall@gmail.com").save()
User(username="tansalalv", first_name="Tania", last_name="Salguero Alvarez", last_login=timezone.now(), password="pbkdf2_sha256$100000$5RrgRCDef2YP$t6T2MjQPJVCrY5IvnGMnkSSIbasZNx8nnx59ao4aAB8=",email="tansalalv@gmail.com").save()
User(username="carloztor", first_name="Carlos", last_name="Lozano", last_login=timezone.now(), password="pbkdf2_sha256$100000$mxAT3eCAVLU2$T3tez+MZzikI8uRwch05GoZib0ZD7BZsPOyzzqFW5sc=",email="carloztor@gmail.com").save()
User(username="mansergue", first_name="Manuel", last_name="Serrano Guerrero", last_login=timezone.now(), password="pbkdf2_sha256$100000$WyBDBlRclzC8$ZpmNuo57IVFeiExf00pxzN7gsTeq8V072b0LG/mZCo4=",email="mansergue@gmail.com").save()
User(username="gonlopher", first_name="Gonzalo", last_name="Lopez hernandez", last_login=timezone.now(), password="pbkdf2_sha256$100000$QWbvh5g6WQPJ$QW80LGiL3S6QSkw7HdbFfjLYQzY4aWH2E4oz2t8VpW4=",email="gonlopher@gmail.com").save()
User(username="raurompal", first_name="Raul", last_name="Romero Palomo", last_login=timezone.now(), password="pbkdf2_sha256$100000$u4UZ1CxnSg8G$SWe+g3gXgo9YnavdWRkVoRuJZ8cAqwdBQnDlaffGwhA=",email="raurompal@gmail.com").save()

Profile.objects.all().delete()
Profile(avatar="avatars/foto-tamaño-carnet.jpg", user_id=1).save()
Profile(avatar="avatars/580109640.jpg", user_id=2).save()
Profile(avatar="avatars/descarga.jpg", user_id=3).save()
Profile(avatar="avatars/chica-sonrisa.jpg", user_id=4).save()
Profile(avatar="avatars/chico.jpg", user_id=5).save()
Profile(avatar="avatars/chico1.jpg", user_id=6).save()
Profile(avatar="avatars/chico2.jpg", user_id=7).save()
Profile(avatar="avatars/images.jpg", user_id=8).save()

UserProperties.objects.all().delete()
UserProperties(profile_id=1,sporty=2,gamer=2,sociable=5, degree=2 ).save()
UserProperties(profile_id=2,smoker=True,pets=True ,sporty=5,gamer=5,sociable=1, degree=2 ).save()
UserProperties(profile_id=3, pets=True ,sporty=1,gamer=5,sociable=3, degree=2 ).save()
UserProperties(profile_id=4,smoker=True ,sporty=5,gamer=5,sociable=1, degree=3 ).save()
UserProperties(profile_id=5,smoker=True,pets=True ,sporty=5,gamer=5,sociable=4, degree=4 ).save()
UserProperties(profile_id=6,smoker=True,pets=True ,sporty=5,gamer=5,sociable=5, degree=5 ).save()
UserProperties(profile_id=7 ,sporty=5,gamer=5,sociable=2, degree=2 ).save()
UserProperties(profile_id=8,smoker=True,pets=True ,sporty=3,gamer=3,sociable=1, degree=2 ).save()


Flat.objects.all().delete()
Flat(title="Piso en Bami", address="Calle castillo de constantina nº3 sevilla", description="Piso amplio y luminoso", picture="flat/piso1.jpg",owner_id=1).save()
Flat(title="Piso en la raza", address="Calle claudio boutelou", description="Piso amplio y luminoso", picture="flat/piso2.jpg",owner_id=2).save()
Flat(title="Piso en las 3000", address="Calle utopia las 3000", description="Piso muy barato y blindado", picture="flat/piso3.jpg",owner_id=3).save()
Flat(title="Piso los remedios", address="Calle virgen de lujan 4", description="Habitaciones grandes con balcones", picture="flat/piso4.jpg",owner_id=4).save()
Flat(title="Piso en Triana", address="Calle manuel arellano n 1 sevilla", description="Piso acogedor y moderno", picture="flat/piso5.jpg",owner_id=5).save()
Flat(title="Piso en Viapol", address="Calle Santo Rey 5", description="Cerca de la universidad", picture="flat/piso6.jpg",owner_id=6).save()
Flat(title="Piso en Torneo", address="Calle torneo", description="Cerca de la estacion plaza de armas", picture="flat/piso7.jpg",owner_id=7).save()
Flat(title="Piso en la cartuja", address="Calle Albert Einstein 4", description="Cerca de la universidad tecnica", picture="flat/piso8.jpg",owner_id=8).save()


FlatProperties.objects.all().delete()
FlatProperties(flat_id=1, elevator=True, washdisher=True).save()
FlatProperties(flat_id=2, washdisher=True).save()
FlatProperties(flat_id=3, elevator=True, ).save()
FlatProperties(flat_id=4 ).save()
FlatProperties(flat_id=5, elevator=True, washdisher=True).save()
FlatProperties(flat_id=6, elevator=True, washdisher=True).save()
FlatProperties(flat_id=7, washdisher=True).save()
FlatProperties(flat_id=8, elevator=True).save()


Room.objects.all().delete()
Room(description="Habitacion amueblada con escritorio", price=280, picture="room/habitacion2.jpg",temporal_owner_id=5,belong_to_id=1).save()
Room(description="Habitacion con dos escritorios", price=280, picture="room/habitacion1.jpg",temporal_owner_id=6,belong_to_id=1).save()

Room(description="Habitacion amplia", price=300, picture="room/habitacion4.jpg",temporal_owner_id=7,belong_to_id=2).save()
Room(description="Habitacion con  armario", price=300, picture="room/habitacion6.jpg",temporal_owner_id=8,belong_to_id=2).save()

Room(description="Habitacion con television", price=290, picture="room/habitacion11.jpg",belong_to_id=3).save()
Room(description="Habitacion bien amueblada", price=290, picture="room/habitacion5.jpg",belong_to_id=3).save()

Room(description="Habitacion pequeña simple", price=250, picture="room/habitacion3.jpg",belong_to_id=4).save()
Room(description="Habitacion rural", price=250, picture="room/habitacion8.jpg",belong_to_id=4).save()

Room(description="Habitacion tematica ", price=270, picture="room/habitacion9.jpg",belong_to_id=5).save()
Room(description="Habitacion con cama de matrimonio", price=275, picture="room/habitacion16.jpg",belong_to_id=5).save()

Room(description="Habitacion con balcon", price=280, picture="room/habitacion10.jpg",belong_to_id=6).save()
Room(description="Habitacion con baño propio", price=300, picture="room/habitacion7.jpg",belong_to_id=6).save()

Room(description="Habitacion simple", price=245, picture="room/habitacion12.jpg",belong_to_id=7).save()
Room(description="Habitacion hogareña", price=245, picture="room/habitacion13.jpg",belong_to_id=7).save()

Room(description="Habitacion con buenas vistas", price=300, picture="room/habitacion14.jpg",belong_to_id=8).save()
Room(description="Habitacion junto a la cocina", price=300, picture="room/habitacion15.jpg",belong_to_id=8).save()



RoomProperties.objects.all().delete()
RoomProperties(room_id=1, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=2, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=3,  window=True, air_conditioner=True ).save()
RoomProperties(room_id=4, window=True, air_conditioner=True).save()
RoomProperties(room_id=5,  air_conditioner=True).save()
RoomProperties(room_id=6, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=7, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=8, air_conditioner=True, bed=2).save()
RoomProperties(room_id=9, balcony=True, window=True, air_conditioner=True, bed=2).save()
RoomProperties(room_id=10, balcony=True, window=True, air_conditioner=True, bed=1).save()
RoomProperties(room_id=11, balcony=True,  air_conditioner=True).save()
RoomProperties(room_id=12,  window=True, air_conditioner=True).save()
RoomProperties(room_id=13, balcony=True,  air_conditioner=True).save()
RoomProperties(room_id=14, balcony=True, air_conditioner=True).save()
RoomProperties(room_id=15, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=16,  window=True, air_conditioner=True).save()

Contract.objects.all().delete()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant_id=5, room_id=1).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant_id=6, room_id=2).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant_id=7, room_id=3).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant_id=8, room_id=4).save()

UserReview.objects.all().delete()
UserReview(user_id=1, title="Buen Casero", description="Casero amable, siempre pendiente de todos los problemas posibles", date="08/08/2017", rating=5).save()
UserReview(user_id=1, title="Amable", description="Permite que le paguemos cuando podamos", date="08/08/2017", rating=5).save()
UserReview(user_id=2, title="Mal casero", description="Siempre poniendo pegas", date="08/08/2017", rating=5).save()
UserReview(user_id=5, title="Inquilino responsable", description="Mantiene la habitacion limpia", date="08/08/2017", rating=5).save()
UserReview(user_id=6, title="Inquilino loco", description="No es limpio, ni respeta a los compañeros", date="08/08/2017", rating=5).save()
UserReview(user_id=7, title="Inquilino normal", description="Responsable y buen compañero", date="08/08/2017", rating=5).save()
UserReview(user_id=8, title="Persona responsable", description="Responsable limpio y ordenado", date="08/08/2017", rating=5).save()





FlatReview.objects.all().delete()
FlatReview(flat_id=1, title="Buen piso", description="Amueblado y con buenas vistas", date="10/03/2018", rating=4).save()
FlatReview(flat_id=1, title="Piso con 3 habitaciones", description="Muy limpio y ordenado", date="08/02/2018", rating=5).save()
FlatReview(flat_id=2, title="Piso bonito", description="Buena decoración", date="05/02/2018", rating=2).save()
FlatReview(flat_id=2, title="Piso con buenas vistas", description="Muy bien iluminado", date="01/08/2018", rating=5).save()


RoomReview.objects.all().delete()
RoomReview(room_id=1, title="Habitación limpia", description="Amueblado", date="10/03/2018", rating=4).save()
RoomReview(room_id=1, title="Habitacion amplia", description="Muy bonita, cuadros espectacules", date="11/01/2017", rating=2).save()
RoomReview(room_id=2, title="Amplia y comoda", description="Tan grande que no te agobias en ella", date="01/11/2017", rating=3).save()
RoomReview(room_id=2, title="Habitación preciosa", description="Muy cómoda", date="01/09/2017", rating=3).save()



FlatImage.objects.all().delete()
FlatImage(flat_id=1, image="flat/piso1.jpg").save()
FlatImage(flat_id=2, image="flat/piso2.jpg").save()
FlatImage(flat_id=3, image="flat/piso3.jpg").save()
FlatImage(flat_id=4, image="flat/piso4.jpg").save()
FlatImage(flat_id=5, image="flat/piso5.jpg").save()
FlatImage(flat_id=6, image="flat/piso6.jpg").save()
FlatImage(flat_id=7, image="flat/piso7.jpg").save()
FlatImage(flat_id=8, image="flat/piso8.jpg").save()


RoomImage.objects.all().delete()
RoomImage(room_id=1,image="room/habitacion2.jpg").save()
RoomImage(room_id=2,image="room/habitacion1.jpg").save()
RoomImage(room_id=3,image="room/habitacion4.jpg").save()
RoomImage(room_id=4,image="room/habitacion6.jpg").save()
RoomImage(room_id=5,image="room/habitacion11.jpg").save()
RoomImage(room_id=6,image="room/habitacion5.jpg").save()
RoomImage(room_id=7,image="room/habitacion3.jpg").save()
RoomImage(room_id=8,image="room/habitacion8.jpg").save()
RoomImage(room_id=9,image="room/habitacion9.jpg").save()
RoomImage(room_id=10,image="room/habitacion16.jpg").save()
RoomImage(room_id=11,image="room/habitacion10.jpg").save()
RoomImage(room_id=12,image="room/habitacion7.jpg").save()
RoomImage(room_id=13,image="room/habitacion12.jpg").save()
RoomImage(room_id=14,image="room/habitacion13.jpg").save()
RoomImage(room_id=15,image="room/habitacion14.jpg").save()
RoomImage(room_id=16,image="room/habitacion15.jpg").save()