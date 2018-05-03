from RoomBnB.models import *
from django.contrib.auth.models import User
from django.utils import timezone

User.objects.all().delete()
User(username="damserfer", first_name="Damian", last_name="Serrano Fernandez", last_login=timezone.now(), password="damserfer123",email="damian@gmail.com").save()
User(username="frasanvel1", first_name="Javier", last_name="Santos Velazquez", last_login=timezone.now(), password="frasanvel1123",email="frasanvel1@gmail.com").save()
User(username="alepolhal", first_name="Alejandro", last_name="Polvillo Hall", last_login=timezone.now(), password="alepolhall123",email="alepolhall@gmail.com").save()
User(username="tansalalv", first_name="Tania", last_name="Salguero Alvarez", last_login=timezone.now(), password="tansalalv123",email="tansalalv@gmail.com").save()
User(username="carloztor", first_name="Carlos", last_name="Lozano", last_login=timezone.now(), password="carloztor123",email="carloztor@gmail.com").save()
User(username="mansergue", first_name="Manuel", last_name="Serrano Guerrero", last_login=timezone.now(), password="mansergue123",email="mansergue@gmail.com").save()
User(username="gonlopher", first_name="Gonzalo", last_name="Lopez hernandez", last_login=timezone.now(), password="gonlopher123",email="gonlopher@gmail.com").save()
User(username="raurompal", first_name="Raul", last_name="Romero Palomo", last_login=timezone.now(), password="raurompal123",email="raurompal@gmail.com").save()

Profile.objects.all().delete()
Profile(avatar="/ISPP/static/avatars/foto-tamaño-carnet.jpg", user_id=1).save()
Profile(avatar="/ISPP/static/avatars/580109640.jpg", user_id=2).save()
Profile(avatar="/ISPP/static/avatars/descarga.jpg", user_id=3).save()
Profile(avatar="/ISPP/static/avatars/chica-sonrisa.jpg", user_id=4).save()
Profile(avatar="/ISPP/static/avatars/chico.jpg", user_id=5).save()
Profile(avatar="/ISPP/static/avatars/chico1.jpg", user_id=6).save()
Profile(avatar="/ISPP/static/avatars/chico2.jpg", user_id=7).save()
Profile(avatar="/ISPP/static/avatars/images.jpg", user_id=8).save()

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
Flat(title="Piso en Bami", address="Calle castillo de constantina nº3 sevilla", description="Piso amplio y luminoso", picture="",owner=1).save()
Flat(title="Piso en la raza", address="Calle claudio boutelou", description="Piso amplio y luminoso", picture="",owner=2).save()
Flat(title="Piso en las 3000", address="Calle utopia las 3000", description="Piso muy barato y blindado", picture="",owner=3).save()
Flat(title="Piso los remedios", address="Calle virgen de lujan 4", description="Habitaciones grandes con balcones", picture="",owner=4).save()
Flat(title="Piso en Triana", address="Calle manuel arellano n 1 sevilla", description="Piso acogedor y moderno", picture="",owner=5).save()
Flat(title="Piso en Viapol", address="Calle Santo Rey 5", description="Cerca de la universidad", picture="",owner=6).save()
Flat(title="Piso en Torneo", address="Calle torneo", description="Cerca de la estacion plaza de armas", picture="",owner=7).save()
Flat(title="Piso en la cartuja", address="Calle Albert Einstein 4", description="Cerca de la universidad tecnica", picture="",owner=8).save()


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
Room(description="Habitacion amueblada con escritorio", price=280, picture="",temporal_owner=5,belong_to_id=1).save()
Room(description="Habitacion con dos escritorios", price=280, picture="",temporal_owner=6,belong_to_id=1).save()

Room(description="Habitacion amplia", price=300, picture="",temporal_owner=7,belong_to_id=2).save()
Room(description="Habitacion con  armario", price=300, picture="",temporal_owner=8,belong_to_id=2).save()

Room(description="Habitacion con television", price=290, picture="",belong_to_id=3).save()
Room(description="Habitacion bien amueblada", price=290, picture="",belong_to_id=3).save()

Room(description="Habitacion pequeña simple", price=250, picture="",belong_to_id=4).save()
Room(description="Habitacion rural", price=250, picture="",belong_to_id=4).save()

Room(description="Habitacion tematica ", price=270, picture="",belong_to_id=5).save()
Room(description="Habitacion con cama de matrimonio", price=275, picture="",belong_to_id=5).save()

Room(description="Habitacion con balcon", price=280, picture="",temporal_owner=6,belong_to_id=6).save()
Room(description="Habitacion con baño propio", price=300, picture="",belong_to_id=6).save()

Room(description="Habitacion simple", price=245, picture="",belong_to_id=7).save()
Room(description="Habitacion hogareña", price=245, picture="",belong_to_id=7).save()

Room(description="Habitacion con buenas vistas", price=300, picture="",belong_to_id=8).save()
Room(description="Habitacion junto a la cocina", price=300, picture="",belong_to_id=8).save()



RoomProperties.objects.all().delete()
RoomProperties(room_id=1, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=2, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=3,  window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=4, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=5,  air_conditioner=True, bed=True).save()
RoomProperties(room_id=6, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=7, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=8, air_conditioner=True, bed=True).save()
RoomProperties(room_id=9, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=10, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=11, balcony=True,  air_conditioner=True, bed=True).save()
RoomProperties(room_id=12,  window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=13, balcony=True,  air_conditioner=True, bed=True).save()
RoomProperties(room_id=14, balcony=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=15, balcony=True, window=True, air_conditioner=True, bed=True).save()
RoomProperties(room_id=16,  window=True, air_conditioner=True, bed=True).save()

Contract.objects.all().delete()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant=5, room_id=1).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=1, tenant=6, room_id=2).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant=7, room_id=3).save()
Contract(text="Contrato de temporada", date_signed="10/02/2017", landlord_id=2, tenant=8, room_id=4).save()

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
FlatImage(flat_id=1, image="/ISPP/static/fotos/piso1.jpg").save()
FlatImage(flat_id=2, image="/ISPP/static/fotos/piso2.jpg").save()
FlatImage(flat_id=3, image="/ISPP/static/fotos/piso3.jpg").save()
FlatImage(flat_id=4, image="/ISPP/static/fotos/piso4.jpg").save()
FlatImage(flat_id=5, image="/ISPP/static/fotos/piso5.jpg").save()
FlatImage(flat_id=6, image="/ISPP/static/fotos/piso6.jpg").save()
FlatImage(flat_id=7, image="/ISPP/static/fotos/piso7.jpg").save()
FlatImage(flat_id=8, image="/ISPP/static/fotos/piso8.jpg").save()


RoomImage.objects.all().delete()
RoomImage(room_id=1,image="/ISPP/static/fotos/habitacion2.jpg").save()
RoomImage(room_id=2,image="/ISPP/static/fotos/habitacion1.jpg").save()
RoomImage(room_id=3,image="/ISPP/static/fotos/habitacion4.jpg").save()
RoomImage(room_id=4,image="/ISPP/static/fotos/habitacion6.jpg").save()
RoomImage(room_id=5,image="/ISPP/static/fotos/habitacion11.jpg").save()
RoomImage(room_id=6,image="/ISPP/static/fotos/habitacion5.jpg").save()
RoomImage(room_id=7,image="/ISPP/static/fotos/habitacion3.jpg").save()
RoomImage(room_id=8,image="/ISPP/static/fotos/habitacion8.jpg").save()
RoomImage(room_id=9,image="/ISPP/static/fotos/habitacion9.jpg").save()
RoomImage(room_id=10,image="/ISPP/static/fotos/habitacion16.jpg").save()
RoomImage(room_id=11,image="/ISPP/static/fotos/habitacion10.jpg").save()
RoomImage(room_id=12,image="/ISPP/static/fotos/habitacion7.jpg").save()
RoomImage(room_id=13,image="/ISPP/static/fotos/habitacion12.jpg").save()
RoomImage(room_id=14,image="/ISPP/static/fotos/habitacion13.jpg").save()
RoomImage(room_id=15,image="/ISPP/static/fotos/habitacion14.jpg").save()
RoomImage(room_id=16,image="/ISPP/static/fotos/habitacion15.jpg").save()



