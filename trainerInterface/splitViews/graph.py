from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect


def graphTracking(request):
    if request.method == "POST":
        processForm(request)

    form = getUserform(request)

    return render(request, 'trainerInterface/graph.html', {'form': form})
