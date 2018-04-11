from django.test import TestCase
from django.core.files import File
from django.contrib.auth.models import User
from django.core.management import call_command
from RoomBnB.services import *
from RoomBnB.views import *
from RoomBnB.models import *
from django.utils.timezone import localtime, now


# Create your tests here.

class Test(TestCase):
    def setUp(self):
        #call_command('loaddata', 'deploy/populate.json')
        user1 = User.objects.create_user(username='user1', email='user1@prueba.com')
        user1.set_password('user1')
        user1.save()

        profile1 = Profile(user=user1)
        profile1.save()

        user2 = User.objects.create_user(username='user2', email='user2@prueba.com')
        user2.set_password('user2')
        user2.save()

        profile2 = Profile(user=user2)
        profile2.save()

        user3 = User.objects.create_user(username='user3', email='user3@prueba.com')
        user3.set_password('user3')
        user3.save()

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


    def testCreateFlatPositiveDescription(self):
        user = User.objects.get(username='user1')
        profile = Profile.objects.get(user=user)

        title, address, description = 'Piso', 'Calle betis', ''

        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        self.assertEqual(flat_saved.title, title)
        self.assertEqual(flat_saved.address, address)
        self.assertEqual(flat_saved.description, description)
        self.assertEqual(flat_saved.owner, profile)

    def testCreateFlatNegativeTitle(self):
        exception = False
        user = User.objects.get(username='user1')

        try:
            title, description, address, owner = '', 'Piso de Terra', 'Calle pal pozo', user

            create_flat(title, description, address, owner)
        except:
            exception = True

        self.assertEqual(exception, True)


    def testDeleteFlatPositive(self):
        user = User.objects.get(username='user1')

        title, address, description = 'Piso', 'Calle betis', ''

        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        delete_flat(flat_saved.id)

        flat_alls = Flat.objects.all()

        self.assertTrue(flat_saved not in flat_alls)


    def testShowFlatsPositive(self):
        user = User.objects.get(username='user1')

        title, address, description = 'Piso', 'Calle betis', ''

        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        flats2 = Flat.objects.all()

        self.assertTrue(flat_saved in flats2)


    def testShowRoomsPositive(self):
        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user, flat_saved)
        room_saved = Room.objects.get(description=description)

        rooms2 = Room.objects.all().filter(belong_to=flat_saved)

        self.assertTrue(room_saved in rooms2)


    def testCreateProfilePositive(self):
        user3 = User.objects.get(username='user3')
        create_profile(user3, '')
        profile_saved = Profile.objects.get(user=user3)

        self.assertEqual(profile_saved.user, user3)


    def testCreateProfileExitsNegative(self):
        exception = False
        user = User.objects.get(username='user1')

        try:
            user, avatar = user, '',

            create_profile(user, avatar)
        except:
            exception = True

        self.assertEqual(exception, True)


    def testShowPayments(self):
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        picture = ''
        data = localtime(now()).date()


        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user1)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user1, flat_saved)
        room_saved = Room.objects.get(description=description)

        create_contract(picture, data, user1, user2, room_saved.id)
        contract_saved = Contract.objects.get(room=room_saved)

        amount = 300.0
        data1 = localtime(now()).date()

        create_payment(amount, data1, contract_saved.id)
        payment_saved = Payment.objects.get(contract=contract_saved)

        self.assertEqual(payment_saved.amount, amount)
        self.assertEqual(payment_saved.date, data1)
        self.assertEqual(payment_saved.contract, contract_saved)



    def testRegisterReviewUserPositive(self):
        user = User.objects.get(username='user1')

        title, description, date, rating, user = 'Bien', 'Bien', localtime(now()).date(), '2', user

        create_userreview(title, description, date, rating, user)
        review_saved = UserReview.objects.get(title=title)

        self.assertEqual(review_saved.title, title)
        self.assertEqual(review_saved.description, description)
        self.assertEqual(review_saved.date, date)
        self.assertEqual(review_saved.rating, rating)
        self.assertEqual(review_saved.user, user)


    def testRegisterReviewUserPositiveDescription(self):
        user = User.objects.get(username='user1')

        title, description, date, rating, user = 'Bien', '', localtime(now()).date(), '2', user

        create_userreview(title, description, date, rating, user)
        review_saved = UserReview.objects.get(title=title)

        self.assertEqual(review_saved.title, title)
        self.assertEqual(review_saved.description, description)
        self.assertEqual(review_saved.date, date)
        self.assertEqual(review_saved.rating, rating)
        self.assertEqual(review_saved.user, user)

    def testRegisterReviewUserNegativeTitle(self):

        user = User.objects.get(username='user1')
        title, description, date, rating, user = '', 'Bien', localtime(now()).date(), '3', user

        userReview_saved = create_userreview(title, description, date, rating, user)
        self.assertIsNone(userReview_saved)

    def testRegisterReviewUserNegativeRating(self):
        exception = False
        user = User.objects.get(username='user1')
        try:
            title, description, date, rating, user = 'Titulo', 'Bien', localtime(now()).date(), '-3', user

            create_userreview(title, description, date, rating, user)
        except:
            exception = True

        self.assertEqual(exception, True)


    def testRegisterReviewFlatPositive(self):
        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)


        title, description, date, rating, flat = 'Bien', 'Bien', localtime(now()).date(), '2', flat_saved

        create_flatreview(title, description, date, rating, flat)
        review_saved = FlatReview.objects.get(title=title)

        self.assertEqual(review_saved.title, title)
        self.assertEqual(review_saved.description, description)
        self.assertEqual(review_saved.date, date)
        self.assertEqual(review_saved.rating, rating)
        self.assertEqual(review_saved.flat, flat_saved)

    def testRegisterReviewFlatNegativeTitle(self):
        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        title, description, date, rating, flat = '', 'Bien', localtime(now()).date(), '3', flat_saved
        flatReview_saved = create_flatreview(title, description, date, rating, flat)
        self.assertIsNone(flatReview_saved)


    def testRegisterReviewFlatNegativeRating(self):
        exception = False

        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        try:
            title, description, date, rating, flat = 'Titulo', 'Bien', localtime(now()).date(), '-3', flat_saved

            create_flatreview(title, description, date, rating, flat)
        except:
            exception = True

        self.assertEqual(exception, True)

    def testRegisterReviewFlatNegativeTitleLong(self):
        exception = False

        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        try:
            title, description, date, rating, flat = 'El titulo es demasiado largo porque supera los 50 caracteres maximos', 'Bien', localtime(now()).date(), '3', flat_saved

            create_flatreview(title, description, date, rating, flat)
        except:
            exception = True

        self.assertEqual(exception, True)



    def testRegisterReviewRoomPositive(self):
        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user, flat_saved)
        room_saved = Room.objects.get(description=description)

        title, description, date, rating, room = 'Bien', 'Bien', localtime(now()).date(), '2', room_saved

        create_roomreview(title, description, date, rating, room)
        review_saved = RoomReview.objects.get(description=description)


        self.assertEqual(review_saved.title, title)
        self.assertEqual(review_saved.description, description)
        self.assertEqual(review_saved.date, date)
        self.assertEqual(review_saved.rating, rating)
        self.assertEqual(review_saved.room, room_saved)


    def testRegisterReviewRoomNegativeTitle(self):

        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user, flat_saved)
        room_saved = Room.objects.get(description=description)

        title, description, date, rating, room = '', 'Bien', localtime(now()).date(), '3', room_saved

        roomReview_saved = create_roomreview(title, description, date, rating, room)
        self.assertIsNone(roomReview_saved)



    def testRegisterReviewRoomNegativeRating(self):
        exception = False

        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user, flat_saved)
        room_saved = Room.objects.get(description=description)

        try:
            title, description, date, rating, room = 'Bien', 'Bien', localtime(now()).date(), '-3', room_saved

            create_roomreview(title, description, date, rating, room)

        except:
            exception = True

        self.assertEqual(exception, True)


    def testRegisterReviewRoomNegativeTitleLong(self):
        exception = False

        user = User.objects.get(username='user1')
        title, address, description = 'Piso', 'Bami', 'Piso luminoso'
        create_flat(title, address, description, '', user)
        flat_saved = Flat.objects.get(title=title)

        description, price = 'Bien', '500.5'
        create_room(description, price, '', user, flat_saved)
        room_saved = Room.objects.get(description=description)

        try:
            title, description, date, rating, room = 'El titulo es demasiado largo porque supera los 50 caracteres maximos', 'Bien',localtime(now()).date(), '3', room_saved

            create_roomreview(title, description, date, rating, room)
        except:
            exception = True

        self.assertEqual(exception, True)




