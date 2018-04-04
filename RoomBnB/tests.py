from django.test import TestCase
from django.core.files import File
from RoomBnB.services import *
from RoomBnB.views import *

# Create your tests here.


class TestFlat(TestCase):

    def testRegisterFlatPositive(self):
        flats = Flat.objects.all()
        user = User.objects.get(id=1)
        create_flat(title='Piso en teruel', description='Piso', address='Calle Teruel', owner=user)
        flats2 = Flat.objects.all()
        self.assertEqual(flats, flats2, False)

    def testRegisterFlatNegativeDescription(self):
        exception = False

        user = User.objects.get(id=1)
        try:
            create_flat(title='Piso Betis', description='', address='Calle Teruel', owner=user)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterFlatNegativeTitle(self):
        exception = False

        user = User.objects.get(id=1)
        try:
            create_flat(title='', description='Piso en TerraBIB', address='Calle Teruel', owner=user)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterFlatNegativeAddress(self):
        exception = False

        user = User.objects.get(id=1)
        try:
            create_flat(title='Piso Sevilla', description='Piso en la calle H', address='', owner=user)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testDeleteFlatPositive(self):
        flats = Flat.objects.all()
        f = flats.first()
        self.assertEqual(Room.objects.filter(belong_to=f).exists(), True)
        delete_flat(f.id)
        self.assertEqual(Room.objects.filter(belong_to=f).exists(), False)
        flats2 = Flat.objects.all()
        self.assertEqual(flats, flats2, False)

    def testListFlatsPositive(self):
        flat1 = Flat.objects.all()
        user = User.objects.get(id=1)
        f1 = Flat.objects.create(title='Piso en teruel', description='Pisitoo', address='Calle Teruel', owner=user)
        create_flat(f1.title, f1.description, f1.address, f1.owner)
        flat2 = Flat.objects.all()
        self.assertEqual(flat1, flat2, False)
