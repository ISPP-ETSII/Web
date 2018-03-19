from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from pip.download import user_agent
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from RoomBnB.forms import FlatForm
from RoomBnB.models import Flat
from RoomBnB.models import Profile
from RoomBnB.models import Room


def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList} # TODO: Cambiar f.description por el nombre
    return render(request, 'flat/list.html', context)


def detail(request, flat_id):
    flat=Flat.objects.get(id=flat_id)
    rooms = Room.objects.filter(belong_to=flat)
    return render(request, 'flat/detail.html', {'flat': flat,'roomList':rooms})

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            loggedUser=request.user

            profile = Profile.objects.get(user=loggedUser)
            f1= Flat(description=form.cleaned_data.get("description"), owner=profile)
            f1.save()


            return HttpResponseRedirect('/flats')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FlatForm()

    return render(request, 'flat/create.html', {'form': form})


def flatDelete(request, flat_id):
    flatList = Flat.objects.all()
    context = {'flatList': flatList}
    flat = Flat.objects.get(id=flat_id)
    Flat.delete(flat)

    return render(request, 'flat/list.html', context)

@login_required
def root(request):
    return render(request, template_name='root.html')

def base(request):
    return render(request, template_name='static/index.html')


