from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from api.models import ExerciseType
from .form import *
import openpyxl
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.generic import BSModalCreateView
from datetime import date
import datetime
from django.utils.dateparse import parse_date

User = get_user_model()
from collections import defaultdict

def processDate(request):
    newdate = parse_date(json.loads(request.POST.get('date', None))["date"])
    request.session["date"] = json.dumps(newdate, indent=4, sort_keys=True, default=str)


def processForm(request):

        # Get the posted form
        ClientSelect = UserForm(request.POST)
        if ClientSelect.is_valid():
            selected_client = ClientSelect.cleaned_data["selected_client"]
            print(selected_client.email)
            request.session["selected_client"] = selected_client.email


def home(request):
    context = {


    }
    return render(request, 'trainerInterface/home.html', context=context)

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dashboard(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
    else:
        form = UserForm()

    return render(request, 'trainerInterface/dashboard.html', {'form': form})

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def trainprog(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
        phases = Phase.objects.filter(user=User.objects.get(email=request.session['selected_client']))
    else:
        form = UserForm()
        phases = None

    day = Day.objects.get(week=1, phase = 5, day =1)
    for entry in day.entrys.all():
        print(str(entry.exercise.name) + " Entry ID: "+str(entry.id)+" Exercise Id: " +str(entry.exercise.id))


    # TrackingGroup.objects.all().delete()
    return render(request, 'trainerInterface/trainProg.html', {'form': form, 'phases': phases})

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def trainplan(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
        phases = Phase.objects.filter(user=User.objects.get(email=request.session['selected_client']))
    else:
        form = UserForm()
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
                  {'form': form, 'phases': phases, 'addform': addform, 'exercises': exercises, 'weekOpen': weekOpen})


@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def deleteExercise(request, id=None):
    object = ExerciseType.objects.get(id=id)
    object.delete()

    return redirect('exercises')


def addPhase(request):
    objects = Phase.objects.filter(user=User.objects.get(email=request.session['selected_client']))
    currPhase = 0
    for phase in objects:
        if  currPhase< phase.phase:
            currPhase = phase.phase

    newPhase = Phase(phase = currPhase+1,
                     user = User.objects.get(email=request.session['selected_client']))
    newPhase.save()

    return redirect('trainplan')


def addWeek(request, phaseID=None):
    phase_selected = Phase.objects.get(id=phaseID)
    user = User.objects.get(email=request.session['selected_client'])
    objects = Week.objects.filter(phase=phase_selected.phase, user=user)
    currWeek= 0
    for week in objects:
        if currWeek < week.week:
            currWeek = week.week

    newWeek = Week(week=currWeek+1,
                   phase=phase_selected.phase,
                   user = user)
    newWeek.save()
    phase_selected.weeks.add(newWeek)
    request.session['weekOpen'] = True
    request.session['selectedPhase'] = phase_selected.phase
    return redirect('trainplan')


def addDay(request, phaseID=None, weekID=None):
    phase_selected = Phase.objects.get(id=phaseID)
    week_selected = Week.objects.get(id=weekID)
    user = User.objects.get(email=request.session['selected_client'])
    objects = Day.objects.filter(phase=phase_selected.phase, week=week_selected.week, user=user)
    currDay= 0
    for day in objects:
        if currDay < day.day:
            currDay = day.day

    newDay = Day(day=currDay+1,
                 phase=phase_selected.phase,
                 week=week_selected.week,
                 user=user)
    newDay.save()
    week_selected.days.add(newDay)

    return redirect('trainplan')



def addEntry(request):
    user = User.objects.get(email=request.session['selected_client'])
    if request.is_ajax():
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        day = request.POST.get('day', None)
        exercise = request.POST.get('exercise', None)
        reps = request.POST.get('reps', None)
        weight = request.POST.get('weight', None)
        sets = request.POST.get('sets', None)
        comment = request.POST.get('comment', None)
        print(exercise)
        try:
            train_entry = TrainingEntry(
                user=user,
                phase = phase,
                week = week,
                day = day,
                exercise = ExerciseType.objects.get(name=exercise),
                reps = reps,
                weight = weight,
                sets = sets,
                comment = comment,
            )
            train_entry.save()
            print("saved")
            response = {
                'msg': 'Your form has been submitted successfully'  # response message
            }
            day = Day.objects.get(phase=phase, week=week, day=day, user=user)
            day.entrys.add(train_entry)

        except:
            print("not saved")
            response = {
                'msg': 'Your form has not been saved'  # response message
            }
    return redirect('trainplan')

def changeOrder(request):
    if request.is_ajax():
        idOrder = json.loads(request.POST.get('idOrder', None))['idOrder']
        order = 1
        for id in idOrder:
            print(id)
            exercise = TrainingEntry.objects.get(id=id)
            exercise.order = order
            exercise.save()
            order += 1

        print(idOrder)

    return redirect('trainplan')

def cloneWeek(request):
    user=User.objects.get(email=request.session['selected_client'])
    if request.is_ajax():
        phaseFromNum = request.POST.get('phaseFrom', None)
        weekFromNum = request.POST.get('weekFrom', None)
        phaseToNum = request.POST.get('phaseTo', None)
        weekToNum = request.POST.get('weekTo', None)
        # try:
        phaseFrom = Phase.objects.get(user=user,
                                      phase=phaseFromNum)
        weekFrom = phaseFrom.weeks.get(week=weekFromNum, user=user)

        phaseTo = Phase.objects.get(user=User.objects.get(email=request.session['selected_client']),
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
                    user = User.objects.get(email=request.session['selected_client']),
                    phase=weekTo.phase,
                    week=weekTo.week,
                    day=day.day,
                    reps = entry.reps,
                    weight = entry.weight,
                    sets = entry.sets,
                    comment = entry.comment,
                    exercise = entry.exercise
                )
                copiedEntry.save()
                copiedEntrys.append(copiedEntry)
            copiedDay = Day(
                phase= weekTo.phase,
                week = weekTo.week,
                day = day.day,
                user = user
            )
            copiedDay.save()
            copiedDay.entrys.add(*copiedEntrys)
            copiedDay.save()
            copiedDays.append(copiedDay)
        weekTo.days.add(*copiedDays)
        weekTo.save()
        # except:

    return redirect('trainplan')

def toggleActiveWeek(request):
    if request.is_ajax():
        phaseNum = request.POST.get('phase', None)
        weekNum = request.POST.get('week', None)
        try:
            allPhases = Phase.objects.filter(user = User.objects.get(email=request.session['selected_client']))
            for phase in allPhases:
                try:
                    activeWeek = phase.weeks.get(isActive=True)
                    activeWeek.isActive = False;
                    activeWeek.save()
                    print("found active week" +activeWeek.week)
                except:
                    print("active week not found")

            phase = Phase.objects.get(user = User.objects.get(email=request.session['selected_client']), phase=phaseNum)
            week = phase.weeks.get(week=weekNum)
            week.isActive = True
            week.save()


        except:
            print("changing active week didnt work")
    return redirect('trainplan')

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
            train_entry.exercise = ExerciseType.objects.get(name = exerciseName)
            train_entry.reps = reps
            train_entry.weight = weight
            train_entry.sets = sets
            train_entry.comment = comment
            train_entry.save()
            print("entry updated")

        except:
            print("entry not edited")
            response = {
                'msg': 'not edited'  # response message
            }
    return redirect('trainplan')

def deleteEntry(request):

    if request.is_ajax():
        id = request.POST.get('id', None)

        try:
            train_entry = TrainingEntry.objects.get(id=id)
            train_entry.delete()


        except:
            print("entry not deleted")
            response = {
                'msg': 'not deleted'  # response message
            }
    return redirect('trainplan')




@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dataTracking(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
        currUserID = request.user.id
        groups = TrackingGroup.objects.filter(trainer__id__in=[1, currUserID])
    else:
        form = UserForm()
        groups = None
    # TrackingGroup.objects.all().delete()
    addGroupForm = GroupAddForm()
    addFieldForm = GroupFieldForm()
    return render(request, 'trainerInterface/dataTracking.html', {'form': form, 'groups': groups, 'addGroupForm':
        addGroupForm, 'addFieldForm': addFieldForm, 'selected_client': request.session['selected_client']})

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dailyTracking(request):
    if request.method == "POST":
        processForm(request)
        if request.is_ajax():
            processDate(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
        currUserID = request.user.id
        groups = TrackingGroup.objects.filter(trainer__id__in=[1, currUserID])
        if 'date' in request.session:
            newdate = date(*map(int, json.loads(request.session['date']).split('-')))

        else:
            newdate = date.today()
        trackingVals = TrackingTextValue.objects.filter(client = User.objects.get(email=request.session['selected_client']), date = newdate)
    else:
        form = UserForm()
        groups = None
        trackingVals = None





    return render(request, 'trainerInterface/dailyTracking.html',
                  {'form': form, 'groups': groups, 'selected_client': request.session['selected_client'],
                   'trackingVals': trackingVals, 'date': newdate})

def editGroup(request):

    if request.is_ajax():
        groupId = request.POST.get('groupId', None)
        name = request.POST.get('name', None)
        fieldIds = json.loads(request.POST.get('fieldIds', None))['fieldIds']
        fieldnames = json.loads(request.POST.get('fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get('classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]

        editGroup = TrackingGroup.objects.get(id=groupId)
        editGroup.name = name
        editGroup.save()

        for id, fieldname, fieldselect, toggle in zip(fieldIds, fieldnames, fieldSelects, toggles):
            print(id)
            if not id:


                if fieldselect == 'text':
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=False,
                    )
                else:
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=True,
                    )

                if toggle == 'True':
                    new_field.save()
                    new_field.clientToggle.add(User.objects.get(email=request.session['selected_client']))

                new_field.save()
                editGroup.textfields.add(new_field)
                editGroup.save()
            elif 'delete' in id :
                TrackingTextField.objects.get(id=id[0]).delete()

            else:
                editField = TrackingTextField.objects.get(id = id)
                editField.name = fieldname
                if toggle == 'True':
                    editField.clientToggle.add(User.objects.get(email=request.session['selected_client']))
                else:
                    editField.clientToggle.remove(User.objects.get(email=request.session['selected_client']))
                if fieldselect == 'text':
                    editField.type = False
                else:
                    editField.type = True
                editField.save()
                editGroup.textfields.add(editField)
                editGroup.save()

    return redirect('trainprog')

def addGroup(request):

    if request.is_ajax():
        name = request.POST.get('name', None)
        fieldnames = json.loads(request.POST.get('fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get('classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]
        print(fieldSelects)
        try:

            new_group = TrackingGroup(
                name=name,
                trainer=request.user,
            )
            new_group.save()
            for fieldSelect, fieldname, toggle in zip(fieldSelects, fieldnames, toggles):
                if fieldSelect == "text":
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=False,
                    )

                    if toggle == 'True':
                        new_field.save()
                        new_field.clientToggle.add(User.objects.get(email=request.session['selected_client']))

                    new_field.save()
                else:

                    new_field = TrackingTextField(
                        name=fieldname,
                        type=True,
                    )

                    if toggle == 'True':
                        new_field.save()
                        new_field.clientToggle.add(User.objects.get(email=request.session['selected_client']))
                    new_field.save()
                new_group.textfields.add(new_field)
                new_group.save()


            print("saved")
            response = {
                'msg': 'Your form has been submitted successfully'  # response message
            }


        except:
            print("not saved")
            response = {
                'msg': 'Your form has not been saved'  # response message
            }
    return redirect('dataTracking')

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def exercises(request):
    exerciseForm = AddExercise()
    exercises = ExerciseType.objects.all().order_by('name')

    if request.method == "POST":
        processForm(request)

        if 'uploadFile' in request.POST:
            excel_file = request.FILES["excel_file"]

            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(excel_file.temporary_file_path())

            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)

            worksheet.delete_rows(0)
            for row in worksheet.iter_rows():
                if not ExerciseType.objects.filter(name=row[0].value).exists():
                    exercise = ExerciseType(
                        name=row[0].value,
                        description=row[1].value,
                        video=row[2].value,
                    )
                    exercise.save()
                    print("exercise " + exercise.name + " saved")
                else:
                    exercise = ExerciseType.objects.get(name=row[0].value)
                    exercise.description = row[1].value
                    exercise.video = row[2].value
                    exercise.save()
                    print("exercise " + row[0].value + " updated")
        if 'addExercise' in request.POST:

            addedExercise = AddExercise(request.POST, request.FILES)
            if addedExercise.is_valid():
                name = addedExercise.cleaned_data.get("name")
                description = addedExercise.cleaned_data.get("description")
                image = addedExercise.cleaned_data.get("image")
                video = addedExercise.cleaned_data.get("video")
                if not ExerciseType.objects.filter(name=name).exists():
                    exercise = ExerciseType(
                        name=name,
                        description=description,
                        image=image,
                        video=video,
                        )
                    exercise.save()
                    print("exercise " + name + " saved")
                else:
                    exercise = ExerciseType.objects.get(name=name)
                    exercise.description = description
                    exercise.image = image
                    exercise.video = video
                    exercise.save()
                    print("exercise " + name + " updated")
    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
    else:
        form = UserForm()
    return render(request, 'trainerInterface/exercises.html', {'form': form, 'exercises': exercises, 'exerciseForm': exerciseForm})



