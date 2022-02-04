from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect


def trainplan(request):

    if request.is_ajax():
        if "selected_client" in request.session:
            phases = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
        else:
            phases = None

        addform = AddTrainingEntry()
        exercises = ExerciseType.objects.order_by('name')

        # when the add week button is pressed this results in the page reloading with weeks menu open rather than phase open
        weekOpen = False
        if "weekOpen" in request.session:
            if request.session["weekOpen"] == True:
                request.session["weekOpen"] = False
                weekOpen = True

        return render(request, 'trainerInterface/trainPlan.html',
                      {'phases': phases, 'addform': addform, 'exercises': exercises, 'weekOpen': weekOpen})
