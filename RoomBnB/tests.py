from django.test import TestCase
from django.core.files import File
from RoomBnB.services import *
from RoomBnB.views import *

# Create your tests here.


class TestFlat(TestCase):

    # Tests de piso

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

    # Tests de opiniones de usuario

    def testRegisterReviewUserPositive(self):
        user = User.objects.get(id=1)
        reviews = UserReview.objects.filter(user=user)

        create_userreview(title='Bien', description='Buen compañero', date='15/02/2017', rating='1', user=user)
        reviews2 = UserReview.objects.filter(user=user)
        self.assertEqual(reviews, reviews2, False)

    def testRegisterReviewUserPositiveDescription(self):
        user = User.objects.get(id=1)
        reviews = UserReview.objects.filter(user=user)

        create_userreview(title='Bien', description='', date='15/02/2017', rating='4', user=user)
        reviews2 = UserReview.objects.filter(user=user)
        self.assertEqual(reviews, reviews2, False)


    def testRegisterReviewUserNegativeTitle(self):
        exception = False

        user = User.objects.get(id=1)
        try:
            create_userreview(title='', description='Bien', date='11/04/2017', rating='2', user=user)
        except:
            exception = True

        self.assertEqual(exception, True)


    def testRegisterReviewUserNegativeRating(self):
        exception = False

        user = User.objects.get(id=1)
        try:
            create_userreview(title='Muy mal ', description='Fumaba en exceso', date='05/01/2018', rating='', user=user)
        except:
            exception = True

        self.assertEqual(exception, True)

    # Test de opiniones al piso

    def testRegisterReviewFlatPositive(self):
        flats = Flat.objects.all()
        f = flats.first()
        reviews = FlatReview.objects.filter(flat=f)

        create_flatreview(title='Excelente', description='Buen piso', date='15/02/2017', rating='5', flat=f)
        reviews2 = FlatReview.objects.filter(flat=f)
        self.assertEqual(reviews, reviews2, False)

    def testRegisterReviewFlatNegativeTitle(self):
        exception = False

        flats = Flat.objects.all()
        f = flats.first()
        try:
            create_flatreview(title='', description='Bien', date='05/11/2017', rating='3', flat=f)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterReviewFlatNegativeRating(self):
        exception = False

        flats = Flat.objects.all()
        f = flats.first()
        try:
            create_flatreview(title='Bien', description='Mejor imposible', date='30/07/2016', rating='-3', flat=f)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterReviewFlatNegativeTitleLong(self):
        exception = False

        flats = Flat.objects.all()
        f = flats.first()
        try:
            create_flatreview(title='El titulo es demasiado largo porque supera los 50 caracteres maximos', description='Bien', date='15/02/2017', rating='3', flat=f)
        except:
            exception = True

        self.assertEqual(exception, True)

    # Test de opiniones a la habitacion

    def testRegisterReviewRoomPositive(self):
        rooms = Room.objects.all()
        r = rooms.first()
        reviews = RoomReview.objects.filter(room=r)

        create_roomreview(title='Bien', description='Buen habitacion', date='09/02/2017', rating='1', room=r)
        reviews2 = RoomReview.objects.filter(room=r)
        self.assertEqual(reviews, reviews2, False)

    def testRegisterReviewRoomNegativeTitle(self):
        exception = False

        rooms = Room.objects.all()
        r = rooms.first()
        try:
            create_roomreview(title='', description='Bien', date='15/02/2017', rating='3', room=r)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterReviewRoomNegativeRating(self):
        exception = False

        rooms = Room.objects.all()
        r = rooms.first()
        try:
            create_roomreview(title='Bien', description='Bien', date='27/05/2017', rating='0', room=r)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterReviewRoomNegativeTitleLong(self):
        exception = False

        rooms = Room.objects.all()
        r = rooms.first()
        try:
            create_roomreview(title='El titulo es demasiado largo porque supera los 50 caracteres maximos asi que...',
                              description='Bien', date='15/02/2017', rating='3', room=r)
        except:
            exception = True

        self.assertEqual(exception, True)



