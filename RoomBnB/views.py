from django.core.serializers import unregister_serializer
from django.http.multipartparser import parse_boundary_stream
from django.shortcuts import render
from django.http import HttpResponse
from pip.download import user_agent
from django.utils import timezone

from RoomBnB.models import *

# Create your views here.
