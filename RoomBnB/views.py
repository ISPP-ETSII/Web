from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse
from pip.download import user_agent
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from RoomBnB.models import Flat



def list(request):
    flatList = Flat.objects.all()
    context = {'flatList': flatList} # TODO: Cambiar f.description por el nombre
    return render(request, 'flat/list.html', context)



def detail(request, flat_id):
    return HttpResponse("You're looking at flat %s." % flat_id)


@login_required
def root(request):
    return render(request, template_name='root.html')
