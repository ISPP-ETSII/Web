from RoomBnB.models import *
from django.contrib.auth.models import User
from django.utils import timezone


User.objects.all().delete()
User(username="damserfer", first_name="Damian", last_name="Serrano Fernandez", last_login=timezone.now(), password="pbkdf2_sha256$100000$7A2Auxc1wT9A$zOrLubd7KlN6cfPH9nZ322S2n8AYHGawSJbYXvuxRJQ=",email="damian@gmail.com").save()
User(username="frasanvel1", first_name="Javier", last_name="Santos Velazquez", last_login=timezone.now(), password="pbkdf2_sha256$100000$oEzewmmGTjyT$xhBw3UmmCBvugvI8Tc1Ax6iL+WA5AvZRFF/oMx36BJI=",email="frasanvel1@gmail.com").save()
User(username="alepolhal", first_name="Alejandro", last_name="Polvillo Hall", last_login=timezone.now(), password="pbkdf2_sha256$100000$4UA2r8wfvzwt$IjMLHNx7Pfmx3d0YoYh4lmvC5eVbzg7Autt/QuhPji0=",email="alepolhall@gmail.com").save()
User(username="tansalalv", first_name="Tania", last_name="Salguero Alvarez", last_login=timezone.now(), password="pbkdf2_sha256$100000$5RrgRCDef2YP$t6T2MjQPJVCrY5IvnGMnkSSIbasZNx8nnx59ao4aAB8=",email="tansalalv@gmail.com").save()
User(username="carloztor", first_name="Carlos", last_name="Lozano", last_login=timezone.now(), password="pbkdf2_sha256$100000$mxAT3eCAVLU2$T3tez+MZzikI8uRwch05GoZib0ZD7BZsPOyzzqFW5sc=",email="carloztor@gmail.com").save()
User(username="mansergue", first_name="Manuel", last_name="Serrano Guerrero", last_login=timezone.now(), password="pbkdf2_sha256$100000$WyBDBlRclzC8$ZpmNuo57IVFeiExf00pxzN7gsTeq8V072b0LG/mZCo4=",email="mansergue@gmail.com").save()
User(username="gonlopher", first_name="Gonzalo", last_name="Lopez hernandez", last_login=timezone.now(), password="pbkdf2_sha256$100000$QWbvh5g6WQPJ$QW80LGiL3S6QSkw7HdbFfjLYQzY4aWH2E4oz2t8VpW4=",email="gonlopher@gmail.com").save()
User(username="raurompal", first_name="Raul", last_name="Romero Palomo", last_login=timezone.now(), password="pbkdf2_sha256$100000$u4UZ1CxnSg8G$SWe+g3gXgo9YnavdWRkVoRuJZ8cAqwdBQnDlaffGwhA=",email="raurompal@gmail.com").save()

Profile.objects.all().delete()
Profile(avatar="avatars/foto-tamaño-carnet.jpg", user_id=1).save()
Profile(avatar="avatars/580109640.jpg", user_id=2).save()
Profile(avatar="avatars/descarga.jpg", user_id=3).save()
Profile(avatar="avatars/chica-sonrisa.jpg", user_id=4).save()
Profile(avatar="avatars/chico.jpg", user_id=5).save()
Profile(avatar="avatars/chico1.jpg", user_id=6).save()
Profile(avatar="avatars/chico2.jpg", user_id=7).save()
Profile(avatar="avatars/images.jpg", user_id=8).save()

UserProperties.objects.all().delete()
UserProperties(profile_id=1,sporty=2,gamer=2,sociable=5, degree=2 ).save()
UserProperties(profile_id=2,smoker=True,pets=True ,sporty=5,gamer=5,sociable=1, degree=2 ).save()
UserProperties(profile_id=3, pets=True ,sporty=1,gamer=5,sociable=3, degree=2 ).save()
UserProperties(profile_id=4,smoker=True ,sporty=5,gamer=5,sociable=1, degree=3 ).save()
UserProperties(profile_id=5,smoker=True,pets=True ,sporty=5,gamer=5,sociable=4, degree=4 ).save()
UserProperties(profile_id=6,smoker=True,pets=True ,sporty=5,gamer=5,sociable=5, degree=5 ).save()
UserProperties(profile_id=7 ,sporty=5,gamer=5,sociable=2, degree=2 ).save()
UserProperties(profile_id=8,smoker=True,pets=True ,sporty=3,gamer=3,sociable=1, degree=2 ).save()


Flat.objects.all().delete()
Flat(title="Piso en Bami", address="Calle castillo de constantina nº3 sevilla", description="Piso amplio y luminoso", picture="flat/piso1.jpg",owner_id=1).save()
Flat(title="Piso en la raza", address="Calle claudio boutelou", description="Piso amplio y luminoso", picture="flat/piso2.jpg",owner_id=2).save()
Flat(title="Piso en las 3000", address="Calle utopia las 3000", description="Piso muy barato y blindado", picture="flat/piso3.jpg",owner_id=3).save()
Flat(title="Piso los remedios", address="Calle virgen de lujan 4", description="Habitaciones grandes con balcones", picture="flat/piso4.jpg",owner_id=4).save()
Flat(title="Piso en Triana", address="Calle manuel arellano n 1 sevilla", description="Piso acogedor y moderno", picture="flat/piso5.jpg",owner_id=5).save()
Flat(title="Piso en Viapol", address="Calle Santo Rey 5", description="Cerca de la universidad", picture="flat/piso6.jpg",owner_id=6).save()
Flat(title="Piso en Torneo", address="Calle torneo", description="Cerca de la estacion plaza de armas", picture="flat/piso7.jpg",owner_id=7).save()
Flat(title="Piso en la cartuja", address="Calle Albert Einstein 4", description="Cerca de la universidad tecnica", picture="flat/piso8.jpg",owner_id=8).save()


FlatProperties.objects.all().delete()
FlatProperties(flat_id=1, elevator=True, washdisher=True).save()
FlatProperties(flat_id=2, washdisher=True).save()
FlatProperties(flat_id=3, elevator=True, ).save()
FlatProperties(flat_id=4 ).save()
FlatProperties(flat_id=5, elevator=True, washdisher=True).save()
FlatProperties(flat_id=6, elevator=True, washdisher=True).save()
FlatProperties(flat_id=7, washdisher=True).save()
FlatProperties(flat_id=8, elevator=True).save()


Room.objects.all().delete()
Room(description="Habitacion amueblada con escritorio", price=280, picture="room/habitacion2.jpg",temporal_owner_id=5,belong_to_id=1).save()
Room(description="Habitacion con dos escritorios", price=280, picture="room/habitacion1.jpg",temporal_owner_id=6,belong_to_id=1).save()

Room(description="Habitacion amplia", price=300, picture="room/habitacion4.jpg",temporal_owner_id=7,belong_to_id=2).save()
Room(description="Habitacion con  armario", price=300, picture="room/habitacion6.jpg",temporal_owner_id=8,belong_to_id=2).save()

Room(description="Habitacion con television", price=290, picture="room/habitacion11.jpg",belong_to_id=3).save()
Room(description="Habitacion bien amueblada", price=290, picture="room/habitacion5.jpg",belong_to_id=3).save()

Room(description="Habitacion pequeña simple", price=250, picture="room/habitacion3.jpg",belong_to_id=4).save()
Room(description="Habitacion rural", price=250, picture="room/habitacion8.jpg",belong_to_id=4).save()

Room(description="Habitacion tematica ", price=270, picture="room/habitacion9.jpg",belong_to_id=5).save()
Room(description="Habitacion con cama de matrimonio", price=275, picture="room/habitacion16.jpg",belong_to_id=5).save()

Room(description="Habitacion con balcon", price=280, picture="room/habitacion10.jpg",belong_to_id=6).save()
Room(description="Habitacion con baño propio", price=300, picture="room/habitacion7.jpg",belong_to_id=6).save()

Room(description="Habitacion simple", price=245, picture="room/habitacion12.jpg",belong_to_id=7).save()
Room(description="Habitacion hogareña", price=245, picture="room/habitacion13.jpg",belong_to_id=7).save()

Room(description="Habitacion con buenas vistas", price=300, picture="room/habitacion14.jpg",belong_to_id=8).save()
Room(description="Habitacion junto a la cocina", price=300, picture="room/habitacion15.jpg",belong_to_id=8).save()



RoomProperties.objects.all().delete()
RoomProperties(room_id=1, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=2, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=3,  window=True, air_conditioner=True ).save()
RoomProperties(room_id=4, window=True, air_conditioner=True).save()
RoomProperties(room_id=5,  air_conditioner=True).save()
RoomProperties(room_id=6, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=7, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=8, air_conditioner=True, bed=2).save()
RoomProperties(room_id=9, balcony=True, window=True, air_conditioner=True, bed=2).save()
RoomProperties(room_id=10, balcony=True, window=True, air_conditioner=True, bed=1).save()
RoomProperties(room_id=11, balcony=True,  air_conditioner=True).save()
RoomProperties(room_id=12,  window=True, air_conditioner=True).save()
RoomProperties(room_id=13, balcony=True,  air_conditioner=True).save()
RoomProperties(room_id=14, balcony=True, air_conditioner=True).save()
RoomProperties(room_id=15, balcony=True, window=True, air_conditioner=True).save()
RoomProperties(room_id=16,  window=True, air_conditioner=True).save()

Contract.objects.all().delete()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant_id=5, room_id=1).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant_id=6, room_id=2).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant_id=7, room_id=3).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant_id=8, room_id=4).save()

UserReview.objects.all().delete()
UserReview(user_id=1, title="Buen Casero", description="Casero amable, siempre pendiente de todos los problemas posibles", date="08/08/2017", rating=5).save()
UserReview(user_id=1, title="Amable", description="Permite que le paguemos cuando podamos", date="08/08/2017", rating=5).save()
UserReview(user_id=2, title="Mal casero", description="Siempre poniendo pegas", date="08/08/2017", rating=5).save()
UserReview(user_id=5, title="Inquilino responsable", description="Mantiene la habitacion limpia", date="08/08/2017", rating=5).save()
UserReview(user_id=6, title="Inquilino loco", description="No es limpio, ni respeta a los compañeros", date="08/08/2017", rating=5).save()
UserReview(user_id=7, title="Inquilino normal", description="Responsable y buen compañero", date="08/08/2017", rating=5).save()
UserReview(user_id=8, title="Persona responsable", description="Responsable limpio y ordenado", date="08/08/2017", rating=5).save()





FlatReview.objects.all().delete()
FlatReview(flat_id=1, title="Buen piso", description="Amueblado y con buenas vistas", date="10/03/2018", rating=4).save()
FlatReview(flat_id=1, title="Piso con 3 habitaciones", description="Muy limpio y ordenado", date="08/02/2018", rating=5).save()
FlatReview(flat_id=2, title="Piso bonito", description="Buena decoración", date="05/02/2018", rating=2).save()
FlatReview(flat_id=2, title="Piso con buenas vistas", description="Muy bien iluminado", date="01/08/2018", rating=5).save()


RoomReview.objects.all().delete()
RoomReview(room_id=1, title="Habitación limpia", description="Amueblado", date="10/03/2018", rating=4).save()
RoomReview(room_id=1, title="Habitacion amplia", description="Muy bonita, cuadros espectacules", date="11/01/2017", rating=2).save()
RoomReview(room_id=2, title="Amplia y comoda", description="Tan grande que no te agobias en ella", date="01/11/2017", rating=3).save()
RoomReview(room_id=2, title="Habitación preciosa", description="Muy cómoda", date="01/09/2017", rating=3).save()



FlatImage.objects.all().delete()
FlatImage(flat_id=1, image="flat/piso1.jpg").save()
FlatImage(flat_id=2, image="flat/piso2.jpg").save()
FlatImage(flat_id=3, image="flat/piso3.jpg").save()
FlatImage(flat_id=4, image="flat/piso4.jpg").save()
FlatImage(flat_id=5, image="flat/piso5.jpg").save()
FlatImage(flat_id=6, image="flat/piso6.jpg").save()
FlatImage(flat_id=7, image="flat/piso7.jpg").save()
FlatImage(flat_id=8, image="flat/piso8.jpg").save()


RoomImage.objects.all().delete()
RoomImage(room_id=1,image="room/habitacion2.jpg").save()
RoomImage(room_id=2,image="room/habitacion1.jpg").save()
RoomImage(room_id=3,image="room/habitacion4.jpg").save()
RoomImage(room_id=4,image="room/habitacion6.jpg").save()
RoomImage(room_id=5,image="room/habitacion11.jpg").save()
RoomImage(room_id=6,image="room/habitacion5.jpg").save()
RoomImage(room_id=7,image="room/habitacion3.jpg").save()
RoomImage(room_id=8,image="room/habitacion8.jpg").save()
RoomImage(room_id=9,image="room/habitacion9.jpg").save()
RoomImage(room_id=10,image="room/habitacion16.jpg").save()
RoomImage(room_id=11,image="room/habitacion10.jpg").save()
RoomImage(room_id=12,image="room/habitacion7.jpg").save()
RoomImage(room_id=13,image="room/habitacion12.jpg").save()
RoomImage(room_id=14,image="room/habitacion13.jpg").save()
RoomImage(room_id=15,image="room/habitacion14.jpg").save()
RoomImage(room_id=16,image="room/habitacion15.jpg").save()