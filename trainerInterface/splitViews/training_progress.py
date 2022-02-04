from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect


def trainprog(request):
    if request.is_ajax():
        if "selected_client" in request.session:
            phases = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
        else:
            phases = None

        return render(request, 'trainerInterface/trainProg.html', {'phases': phases})
