from django.test import TestCase
from django.contrib.auth.models import User
from RoomBnB.models import Profile, Flat, Room, Contract, FlatProperties, RoomProperties
from RoomBnB.services import create_flat
from django.core.management import call_command
from RoomBnB.services import sign_contractCreate
from RoomBnB.services import sign_contractCreated


class Test(TestCase):
    def setUp(self):
        #call_command('loaddata', 'deploy/populate.json')
        user1 = User.objects.create_user(username='user1', email='user1@prueba.com')
        user1.set_password('user1')
        user1.save()

        profile1 = Profile(user=user1)
        profile1.save()

    def testCreateFlat(self):
        user = User.objects.get(username='user1')
        profile = Profile.objects.get(user=user)

        title, address, description = 'Piso', 'Bami', 'Piso luminoso'

        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        self.assertEqual(flat_saved.title, title)
        self.assertEqual(flat_saved.address, address)
        self.assertEqual(flat_saved.description, description)
        self.assertEqual(flat_saved.owner, profile)

    def testSignContract(self):
        # user creation for the test
        landlordTest = User.objects.create_user(username="landlordTest", email="landlord@prueba.com")
        landlordTest.set_password("landlordTest")
        landlordTest.save()

        profileLand = Profile(landlordTest)
        profileLand.save()

        tenantTest = User.objects.create_user(username="tenantTest", email="tenant@prueba.com")
        tenantTest.set_password("tenantTest")
        tenantTest.save()

        profileTenant = Profile(user=tenantTest)
        profileTenant.save()

        # flat creation for the test
        title, address, description1 = "PisoTest", "Bami", "Piso muy guay"
        create_flat(title, address, description1, '', landlordTest)
        flatSaved = Flat.objects.get(title=title)
        flatSavedProps = FlatProperties.objects.create(flat=flatSaved, elevator=True, washdisher=True)

        # room creation for the test
        description2, price, belong_to = "buena habitacion", 150, flatSaved
        roomSaved = Room.objects.create(description=description2, price=price, picture='', temporal_owner=None,
                                        belong_to=belong_to)
        roomSavedProps = RoomProperties.objects.create(room=roomSaved, balcony=True, window=True, air_conditioner=True)

        sign_contractCreate(roomSaved, "textTest", landlordTest)

        contractCreated = Contract.objects.get(room=roomSaved)

        self.assertEqual(contractCreated.room, roomSaved)
        self.assertEqual(contractCreated.text, "textTest")
        self.assertEqual(contractCreated.landlord, landlordTest)

        sign_contractCreated(roomSaved, tenantTest)

        self.assertEqual(contractCreated.room, roomSaved)
        self.assertEqual(contractCreated.text, "textTest")
        self.assertEqual(contractCreated.landlord, landlordTest)
        self.assertEqual(contractCreated.tenant, tenantTest)