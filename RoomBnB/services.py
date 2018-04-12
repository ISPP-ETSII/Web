from RoomBnB.models import Flat
from RoomBnB.models import FlatProperties
from RoomBnB.models import Profile
from RoomBnB.models import Room
from RoomBnB.models import RoomProperties
from RoomBnB.models import RentRequest
from RoomBnB.models import Review, UserReview, FlatReview, RoomReview, Contract, Payment
from django.shortcuts import render, redirect
from django.db.models import Q


def create_flat(form_title, form_address, form_description, form_picture, user):
    profile = Profile.objects.get(user=user)

    f1 = Flat(title=form_title,
              address=form_address,
              description=form_description,
              picture=form_picture,
              owner=profile)
    return f1.save()


def create_profile(user, form_avatar):

    f1 = Profile(user=user, avatar=form_avatar)
    return f1.save()


def create_contract(form_text, form_data_signed, landlord, tenant, room_id):
    room = Room.objects.get(id=room_id)

    c1= Contract(text=form_text,
                 date_signed=form_data_signed,
                 landlord=landlord,
                 tenant=tenant,
                 room=room)
    return c1.save()

def create_payment(form_amount, form_date, contract_id):
    contract = Contract.objects.get(id=contract_id)

    p1 = Payment(amount=form_amount,
                 date=form_date,
                 contract=contract)
    return p1.save()


def create_room(form_description, form_price, form_picture, user1, flat1):

    f1 = Room(description=form_description,
              price=form_price,
              picture=form_picture,
              temporal_owner=user1,
              belong_to=flat1)
    return f1.save()


def create_userreview(form_title, form_description, form_date, form_rating, user1):

    r1 = UserReview(title=form_title, description=form_description, date=form_date, rating=form_rating, user=user1)
    return r1.save()


def create_flatreview(form_title, form_description, form_date, form_rating, flat1):

    r1 = FlatReview(title=form_title, description=form_description, date=form_date, rating=form_rating, flat=flat1)
    return r1.save()


def create_roomreview(form_title, form_description, form_date, form_rating, room1):

    r1 = RoomReview(title=form_title, description=form_description,
                    date=form_date, rating=form_rating, room=room1)
    return r1.save()


def delete_flat(flat_id):
    flat = Flat.objects.get(id=flat_id)
    return flat.delete()


def get_flat_details(flat):
    try:
        return FlatProperties.objects.get(flat=flat)
    except FlatProperties.DoesNotExist:
        return FlatProperties(flat = flat).save()


def get_room_details(room):
    try:
        return RoomProperties.objects.get(room=room)
    except RoomProperties.DoesNotExist:
        return RoomProperties(room = room).save()


def create_rent_request(user, room_id):
    room = Room.objects.get(pk=room_id)

    if room.belong_to.owner != user and \
            not room.temporal_owner and \
            not RentRequest.objects.filter(requester=user, requested=room, accepted=False):

        rent_request = RentRequest(requester=user, requested=room)
        rent_request.save()
        return redirect('/requests/list')
    else:
        return redirect('/requests/list')

def get_flats_filtered(keyword,elevator,washdisher,balcony,window,air_conditioner):
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

    return res