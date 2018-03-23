from RoomBnB.models import Flat
from RoomBnB.models import Profile
from RoomBnB.models import Room
from RoomBnB.models import RentRequest
from django.shortcuts import render, redirect


def create_flat(form_title, form_address, form_description, user):
    profile = Profile.objects.get(user=user)

    f1 = Flat(title=form_title,
              address=form_address,
              description=form_description,
              owner=profile)
    f1.save()


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
