from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Tu ne devrais pas être là, go away !")
