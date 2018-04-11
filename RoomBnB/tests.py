from django.test import TestCase
from django.test import TestCase
from django.core.files import File
from RoomBnB.services import *
from RoomBnB.views import *

# Create your tests here.

class TestHouseFilter(TestCase):

    #Test de filtrado

    def testFilteredHouse(self):

        #user creation for the test
        userTest = User.objects.create_user(username="userTest", email="user@prueba.com")
        userTest.set_password("userTest")
        userTest.save()

        #flat creation for the test
        title, address, description1 = "PisoTest", "Bami", "Piso muy guay"
        create_flat(title, address, description1, '', userTest)
        flatSaved = Flat.objects.get(title=title)
        flatSavedProps = FlatProperties.objects.create(flat=flatSaved, elevator=True, washdisher=True)

        #room creation for the test
        description2, price, belong_to = "buena habitacion", 150, flatSaved
        roomSaved = Room.objects.create(description=description2, price=price, picture='', temporal_owner='', belong_to=belong_to)
        roomSavedProps = RoomProperties.objects.create(room=roomSaved, balcony=True, window=True, air_conditioner=True)

        #get flats with properties
        flats = get_flats_filtered("PisoTest", True, True, True, True, True)

        for flat in flats:

            self.assertEqual(flat, flatSaved)
            self.assertEqual(FlatProperties.objects.get(flat=flat), flatSavedProps)
            roomToCheck = Room.objects.filter(belong_to=flat)
            self.assertEqual(roomToCheck, roomSaved)
            self.assertEqual(RoomProperties.objects.get(room=roomToCheck), roomSavedProps)