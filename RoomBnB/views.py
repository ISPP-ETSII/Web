from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse
from pip.download import user_agent
from django.utils import timezone

from RoomBnB.models import *

# Create your views here.

def loaddata(request):

    #User.objects.all().delete()
    User(username="damserfer", first_name="Damian", last_name="Fernandez", last_login=timezone.now(), password="damserfer",
         email="damian@gmail.com").save()

    User(username="carfergon", first_name="Carlos", last_name="Fernandez", last_login=timezone.now(), password="carfergon",
         email="carlos@gmail.com").save()

    User(username="tansalalv", first_name="Tania", last_name="Salguero", last_login=timezone.now(), password="tansalalv",
         email="tania@gmail.com").save()

    User(username="alevazrod", first_name="Alejandro", last_name="Vazquez", last_login=timezone.now(), password="alevazrod",
         email="alejandro@gmail.com").save()

    User(username="javferfer", first_name="Javier", last_name="Fernandez", last_login=timezone.now(), password="javferfer",
         email="javier@gmail.com").save()

    User(username="pedserlun", first_name="Pedro", last_name="Serrano", last_login=timezone.now(),password="pedserlun",
         email="pedro@gmail.com").save()

    #CreditCard.objects.all().delete()
    CreditCard(owner=1, code=12345677, cvv=123).save()
    CreditCard(owner=2, code=12345678, cvv=124).save()
    CreditCard(owner=3, code=12345679, cvv=125).save()
    CreditCard(owner=4, code=12345680, cvv=126).save()
    CreditCard(owner=5, code=12345680, cvv=126).save()
    CreditCard(owner=6, code=12345680, cvv=126).save()

    #Profile.objects.all().delete()
    Profile(avatar="imagen", credit_card_id=1, user_id=1).save() #Casero 1
    Profile(avatar="imagen", credit_card_id=2, user_id=2).save() #Casero 2
    Profile(avatar="imagen", credit_card_id=3, user_id=3).save()  # inquilino
    Profile(avatar="imagen", credit_card_id=4, user_id=4).save()  # Inquilino
    Profile(avatar="imagen", credit_card_id=5, user_id=5).save()  # Inquilino
    Profile(avatar="imagen", credit_card_id=6, user_id=6).save()  # Inquilino


    #Flat.objects.all().delete()
    Flat(description="Piso en Bami", pictures="img", owner_id=1).save() #Casero id 1
    Flat(description="Piso en Bermejales", pictures="img", owner_id=2).save() #Casero id 2



    #Room.objects.all().delete()
    Room(description="Habitacion luminosa", price=200, pictures="img", belong_to_id=1, temporal_owner_id=3).save() #piso 1
    Room(description="Habitacion con balcon", price=200, pictures="img", belong_to_id=1, temporal_owner_id=4).save() #piso 1
    Room(description="Habitacion grande", price=200, pictures="img", belong_to_id=2, temporal_owner_id=5).save() #piso 2
    Room(description="Habitacion pequeña", price=200, pictures="img", belong_to_id=2, temporal_owner_id=6).save() #piso 2

    #Contract.objects.all().delete()
    Contract(picture="img", date_signed=timezone.now() , landlord_id=1, room_id=1, tenant_id=3).save()
    Contract(picture="img", date_signed=timezone.now(), landlord_id=1, room_id=2, tenant_id=4).save()

    Contract(picture="img", date_signed=timezone.now(), landlord_id=2, room_id=3, tenant_id=5).save()
    Contract(picture="img", date_signed=timezone.now(), landlord_id=2, room_id=4, tenant_id=6).save()

    #Payment.objects.all().delete()
    Payment(amount=200, date=timezone.now(), credit_card_id=3, contract_id=1).save()
    Payment(amount=200, date=timezone.now(), credit_card_id=4, contract_id=2).save()
    Payment(amount=200, date=timezone.now(), credit_card_id=5, contract_id=3).save()
    Payment(amount=200, date=timezone.now(), credit_card_id=6, contract_id=4).save()

    #Review.objects.all().delete()
    Review(title="Review", description="Review general", date=2017 / 1 / 10, rating=1).save()
    Review(title="Review", description="Review general", date=2017 / 1 / 10, rating=2).save()

    #UserReview.objects.all().delete()
    UserReview(user_id=3).save()
    UserReview(user_id=4).save()
    UserReview(user_id=5).save()
    UserReview(user_id=6).save()

    #FlatReview.objects.all().delete()
    FlatReview(flat_id=1).save()
    FlatReview(flat_id=2).save()


    #RoomReview.objects.all().delete()
    RoomReview(room_id=1).save()
    RoomReview(room_id=2).save()
    RoomReview(room_id=3).save()
    RoomReview(room_id=4).save()


    return HttpResponse('hola')
