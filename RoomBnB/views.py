from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from pip.download import user_agent
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from RoomBnB.forms import FlatForm
from RoomBnB.models import Flat


def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList} # TODO: Cambiar f.description por el nombre
    return render(request, 'flat/list.html', context)


def detail(request, flat_id):
    return HttpResponse("You're looking at flat %s." % flat_id)

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FlatForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            f1= Flat(description=form.description)
            f1.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FlatForm()

    return render(request, 'flat/create.html', {'form': form})

@login_required
def root(request):
    return render(request, template_name='root.html')


