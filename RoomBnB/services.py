from RoomBnB.models import Flat
from RoomBnB.models import Profile


def create_flat(form_title, form_address, form_description, user):
    profile = Profile.objects.get(user=user)

    f1 = Flat(title=form_title,
              address=form_address,
              description=form_description,
              owner=profile)
    f1.save()

