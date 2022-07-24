from trainerInterface.views import is_ajax
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from datetime import date


def dailyTracking(request):
    if is_ajax(request):
        newdate = date.today()
        return render(request, 'trainerInterface/dailyTracking.html', {'date': newdate})
