from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from MySite import settings

# Create your views here.


def index(request):
    return HttpResponse('main index')

def sslValidation(request,file_name):
    file = open(os.path.join(settings.BASE_DIR,"data","pki",file_name))
    return HttpResponse(file)
