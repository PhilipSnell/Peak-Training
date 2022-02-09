from urllib import response
from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json


def phaseDropdown(request):
    if request.is_ajax():
        if "selected_client" in request.session:
            phases = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
            html_response = '<select><option value="0" title="add phase">+</option>'

            for phase in phases.order_by('-phase'):
                html_response = html_response + '<option value="' + \
                    str(phase.phase) + '">Phase ' + \
                    str(phase.phase) + '</option>'
            html_response = html_response+'</select>'
        return HttpResponse(html_response)


def weekDropdown(request):
    if request.is_ajax():
        phase = request.GET.get('phase', None)
        if "selected_client" in request.session:
            phase = Phase.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phase)
            weeks = phase.weeks.all()

            html_response = '<select><option value="0" title="add week">+</option>'
            for week in weeks.order_by('-week'):
                html_response = html_response + '<option value="' + \
                    str(week.week) + '">Week ' + \
                    str(week.week) + '</option>'
            html_response = html_response+'</select>'
        return HttpResponse(html_response)


def getDays(request):
    if request.is_ajax():
        phase = request.GET.get('phase', None)
        week = request.GET.get('week', None)
        if "selected_client" in request.session:
            try:
                phase = Phase.objects.get(user=User.objects.get(
                    email=request.session['selected_client']), phase=phase)
                week = phase.weeks.get(week=week)
                days = week.days.all()
            except:
                days = []

            html_response = ''

            for day in days:
                html_response = html_response + \
                    '<div class="day-tile selected-day"><div class="day-tile-word">Day</div><div class="day-tile-num">' + \
                    str(day.day)+'</div></div>'
            html_response = html_response + \
                '<div class="day-tile addDayButton"><div class="day-tile-word">Add Day</div></div>'
        return HttpResponse(html_response)


def trainplan(request):

    if request.is_ajax():
        if "selected_client" in request.session:
            phase = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client'])).order_by('-phase')[0]
            week = Week.objects.filter(user=User.objects.get(
                email=request.session['selected_client']), phase=phase.phase).order_by('-week')[0]
            days = week.days.all()
        else:
            days = None

        addform = AddTrainingEntry()
        exercises = ExerciseType.objects.order_by('name')

        # when the add week button is pressed this results in the page reloading with weeks menu open rather than phase open
        weekOpen = False
        if "weekOpen" in request.session:
            if request.session["weekOpen"] == True:
                request.session["weekOpen"] = False
                weekOpen = True

        return render(request, 'trainerInterface/trainPlan.html',
                      {'days': days, 'addform': addform, 'exercises': exercises, 'weekOpen': weekOpen})


def addEntry(request):
    user = User.objects.get(email=request.session['selected_client'])
    if request.is_ajax():
        phase = request.GET.get('phase', None)
        week = request.GET.get('week', None)
        day = request.GET.get('day', None)
        exercise = request.GET.get('exercise', None)
        reps = request.GET.get('reps', None)
        weight = request.GET.get('weight', None)
        sets = request.GET.get('sets', None)
        comment = request.GET.get('comment', None)
        print(exercise)
        try:
            train_entry = TrainingEntry(
                user=user,
                phase=phase,
                week=week,
                day=day,
                exercise=ExerciseType.objects.get(name=exercise),
                reps=reps,
                weight=weight,
                sets=sets,
                comment=comment,
            )
            train_entry.save()
            print("saved")
            day = Day.objects.get(phase=phase, week=week, day=day, user=user)
            day.entrys.add(train_entry)
            return render(request, 'trainerInterface/segments/addTrainingEntrySegment.html',
                          {'entry': train_entry})

        except:
            print("not saved")
            response = {
                'error': 'Error adding entry'  # response message
            }
    return JsonResponse(response)


def deleteEntry(request):

    if request.is_ajax():
        id = request.POST.get('id', None)

        try:
            train_entry = TrainingEntry.objects.get(id=id)
            train_entry.delete()
            response = {
                'success': 'Entry deleted'  # response message
            }
            return JsonResponse(response)

        except:
            response = {
                'error': 'Entry not deleted'  # response message
            }
            return JsonResponse(response)


def changeOrder(request):
    if request.is_ajax():
        try:
            idOrder = json.loads(request.POST.get('idOrder', None))['idOrder']
            print(idOrder)
            order = 1
            for id in idOrder:
                print(id)
                exercise = TrainingEntry.objects.get(id=id)
                exercise.order = order
                exercise.save()
                order += 1
            response = {
                'success': 'Exercise order updated!'  # response message
            }

        except:
            response = {
                'error': 'order could not be updated'  # response message
            }
        return JsonResponse(response)


def editEntry(request):

    if request.is_ajax():
        id = request.POST.get('id', None)
        exerciseName = request.POST.get('exercise', None)
        reps = request.POST.get('reps', None)
        weight = request.POST.get('weight', None)
        sets = request.POST.get('sets', None)
        comment = request.POST.get('comment', None)

        try:
            train_entry = TrainingEntry.objects.get(id=id)
            train_entry.exercise = ExerciseType.objects.get(name=exerciseName)
            train_entry.reps = reps
            train_entry.weight = weight
            train_entry.sets = sets
            train_entry.comment = comment
            train_entry.save()
            print("entry updated")
            response = {
                'success': 'Exercise updated!'
            }

        except:
            print("entry not edited")
            response = {
                'error': 'failed to update the exercise!'  # response message
            }
        return JsonResponse(response)


def toggleActiveWeek(request):
    if request.is_ajax():
        phaseNum = request.POST.get('phase', None)
        weekNum = request.POST.get('week', None)
        try:
            allPhases = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
            for phase in allPhases:
                try:
                    weeks = phase.weeks.all()
                    activeWeek = weeks.get(isActive=True)
                    activeWeek.isActive = False
                    activeWeek.save()
                    print("found active week" + str(activeWeek.week))
                except:
                    print("active week not found")

            phase = Phase.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phaseNum)
            week = phase.weeks.get(week=weekNum)
            week.isActive = True
            week.save()
            response = {
                'success': 'This week is now active!'
            }

        except:
            print("entry not edited")
            response = {
                'error': 'failed to activate week'  # response message
            }
        return JsonResponse(response)
    return redirect('home')


def addPhase(request):
    if request.is_ajax():
        try:
            objects = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
            currPhase = 0
            for phase in objects:
                if currPhase < phase.phase:
                    currPhase = phase.phase

            newPhase = Phase(phase=currPhase+1,
                             user=User.objects.get(email=request.session['selected_client']))
            newPhase.save()
            response = {
                'success': 'Phase added succesfully!'
            }
        except:
            response = {
                'error': 'Could not add phase!'
            }
        return JsonResponse(response)

    return redirect('home')


def addWeek(request):
    if request.is_ajax():

        try:
            phase = request.POST.get('phase', None)
            user = User.objects.get(email=request.session['selected_client'])
            selected_phase = Phase.objects.get(phase=phase, user=user)
            objects = Week.objects.filter(phase=phase, user=user)
            currWeek = 0
            for week in objects:
                if currWeek < week.week:
                    currWeek = week.week

            newWeek = Week(week=currWeek+1,
                           phase=phase,
                           user=user)
            newWeek.save()
            selected_phase.weeks.add(newWeek)
            # request.session['weekOpen'] = True
            # request.session['selectedPhase'] = phase
            response = {
                'success': 'Week added succesfully!'
            }

        except:
            response = {
                'error': 'Could not add week!'
            }
        return JsonResponse(response)
    return redirect('trainplan')


def addDay(request):
    if request.is_ajax():
        # try:
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        user = User.objects.get(email=request.session['selected_client'])
        week_selected = Week.objects.get(user=user, phase=phase, week=week)
        objects = Day.objects.filter(phase=phase, week=week, user=user)

        currDay = 0
        for day in objects:
            if currDay < day.day:
                currDay = day.day

        newDay = Day(day=currDay+1,
                     phase=phase,
                     week=week,
                     user=user)
        newDay.save()
        week_selected.days.add(newDay)
        response = {
            'success': 'Day added succesfully!'
        }
        # except:
        #     response = {
        #         'error': 'Could not add day!'
        #     }
        return JsonResponse(response)
    return redirect('trainplan')


def getDayTableData(request):

    if request.is_ajax():
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        if "selected_client" in request.session:
            week = Week.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phase, week=week)
            days = week.days.all()
        else:
            days = None
            response = {
                'error': 'Could not load days!'
            }
            return JsonResponse(response)

        return render(request, 'trainerInterface/segments/dayTableData.html', {'days': days})
