from RoomBnB.models import Flat
from RoomBnB.models import FlatProperties
from RoomBnB.models import Profile
from RoomBnB.models import Room
from RoomBnB.models import RoomProperties
from RoomBnB.models import RentRequest
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