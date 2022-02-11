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
            if request.GET.get('progress', None) == None:
                html_response = html_response + \
                    '<div class="day-tile addDayButton"><div class="day-tile-word">Add Day</div></div>'
        return HttpResponse(html_response)


def trainplan(request):

    if request.is_ajax():
        if "selected_client" in request.session:
            phases = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client']))
            phase = phases.order_by('-phase')[0]
            week = Week.objects.filter(user=User.objects.get(
                email=request.session['selected_client']), phase=phase.phase).order_by('-week')[0]
            days = week.days.all()
        else:
            phases = None
            days = None

        addform = AddTrainingEntry()
        exercises = ExerciseType.objects.order_by('name')
        request.session["href"] = '/dashboard/trainplan/'
        return render(request, 'trainerInterface/trainPlan.html',
                      {'days': days, 'addform': addform, 'exercises': exercises, 'phases': phases,
                       'clients': Trainer.objects.get(trainer=request.user).clients.all()})


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
        client = request.POST.get('client', None)
        if "selected_client" in request.session and client == None:
            week = Week.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phase, week=week)
            days = week.days.all()
        elif client != None:
            client = client.split()
            week = Week.objects.get(user=User.objects.get(
                first_name=client[0], last_name=client[1]), phase=phase, week=week)
            days = week.days.all()
        else:
            days = None
            response = {
                'error': 'Could not load days!'
            }
            return JsonResponse(response)

        return render(request, 'trainerInterface/segments/dayTableData.html', {'days': days})


def getClonePhases(request):
    if request.is_ajax():
        try:
            selected_client = request.POST.get('selected_client', None).split()
            first_name = selected_client[0]
            last_name = selected_client[1]
            selected_client = User.objects.get(
                first_name=first_name, last_name=last_name)
            phases = Phase.objects.filter(user=selected_client)

            return render(request, 'trainerInterface/segments/getClonePhases.html', {'phases': phases})
        except:
            response = {
                'error': 'could not get clients phases'
            }
            return JsonResponse(response)


def cloneWeek(request):
    user = User.objects.get(email=request.session['selected_client'])

    if request.is_ajax():
        client_from = request.POST.get('selected_client', None).split()
        client = User.objects.get(
            first_name=client_from[0], last_name=client_from[1])
        phaseFromNum = request.POST.get('phaseFrom', None)
        weekFromNum = request.POST.get('weekFrom', None)
        phaseToNum = request.POST.get('phaseTo', None)
        weekToNum = request.POST.get('weekTo', None)
        # try:
        phaseFrom = Phase.objects.get(user=client,
                                      phase=phaseFromNum)
        weekFrom = phaseFrom.weeks.get(week=weekFromNum, user=client)

        phaseTo = Phase.objects.get(user=user,
                                    phase=phaseToNum)
        weekTo = phaseTo.weeks.get(week=weekToNum, user=user)

        # Clear all current days
        for day in weekTo.days.all():
            for entry in day.entrys.all():
                entry.delete()
            day.delete()
        copiedDays = []
        for day in weekFrom.days.all():
            copiedEntrys = []
            for entry in day.entrys.all():
                copiedEntry = TrainingEntry(
                    user=user,
                    phase=weekTo.phase,
                    week=weekTo.week,
                    day=day.day,
                    reps=entry.reps,
                    weight=entry.weight,
                    sets=entry.sets,
                    comment=entry.comment,
                    exercise=entry.exercise
                )
                copiedEntry.save()
                copiedEntrys.append(copiedEntry)
            copiedDay = Day(
                phase=weekTo.phase,
                week=weekTo.week,
                day=day.day,
                user=user
            )
            copiedDay.save()
            copiedDay.entrys.add(*copiedEntrys)
            copiedDay.save()
            copiedDays.append(copiedDay)
        weekTo.days.add(*copiedDays)
        weekTo.save()
        # except:

    return render(request, 'trainerInterface/segments/dayTableData.html', {'days': weekTo.days.all()})


def checkActiveWeek(request):
    response = {
        'false': 'false'
    }
    if request.is_ajax():
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)

        week = Week.objects.get(user=User.objects.get(
            email=request.session['selected_client']), week=week, phase=phase)

        if (week.isActive):
            response = {
                'true': 'true'
            }
    return JsonResponse(response)
