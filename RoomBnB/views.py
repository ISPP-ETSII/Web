from django.http import HttpResponse
from django.shortcuts import render

from RoomBnB.models import Flat



def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList} # TODO: Cambiar f.description por el nombre
    return render(request, 'flat/list.html', context)



def detail(request, flat_id):
    return HttpResponse("You're looking at flat %s." % flat_id)