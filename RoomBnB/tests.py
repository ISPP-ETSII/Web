from django.test import TestCase
from django.test import TestCase
from django.core.files import File
from RoomBnB.services import *
from RoomBnB.views import *

# Create your tests here.

class TestHouseFilter(TestCase):

    #Test de filtrado

    def testFilteredHouse(self, keyword,elevator,washdisher,balcony,window,air_conditioner):

        flats = get_flats_filtered(keyword, elevator, washdisher, balcony, window, air_conditioner)

        for flat in flats:

            #check keyword
            if keyword not in flat.title: print("Error in title")
            if keyword not in flat.description: print("Error in description")
            if keyword not in flat.address: print("Error in address")

            #check flat properties
            flatProps = FlatProperties.objects.get(flat=flat)
            if flatProps.elevator != elevator: print("Error in elevator")
            if flatProps.washdisher != washdisher: print("Error in washdisher")

            #check room properties
            roomList = Room.objects.filter(belong_to=flat)
            for room in roomList:
                roomProps = RoomProperties.objects.get(room=room)
                if roomProps.balcony != balcony: print("Error in balcony")
                if roomProps.window != balcony: print("Error in window")
                if roomProps.air_conditioner != balcony: print("Error in air conditioner")
