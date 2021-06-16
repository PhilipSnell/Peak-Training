from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from api.models import ExerciseType
from .form import *
import openpyxl
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.generic import BSModalCreateView
User = get_user_model()
from collections import defaultdict

def processForm(request):

        # Get the posted form
        ClientSelect = UserForm(request.POST)
        if ClientSelect.is_valid():
            selected_client = ClientSelect.cleaned_data["selected_client"]
            print(selected_client.email)
            request.session["selected_client"] = selected_client.email
        print("done")

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
def trainplan(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
    else:
        form = UserForm()

    trainingEntries = TrainingEntry.objects.all()
    phases = Phase.objects.filter(user=User.objects.get(email=request.session['selected_client']))
    addform = AddTrainingEntry()
    return render(request, 'trainerInterface/trainPlan.html', {'form': form, 'phases': phases, 'addform': addform})


@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def deleteExercise(request, id=None):
    object = ExerciseType.objects.get(id=id)
    object.delete()

    return redirect('exercises')


def addPhase(request):
    objects = Phase.objects.all()
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
    objects = Week.objects.filter(phase=phase_selected.phase)
    currWeek= 0
    for week in objects:
        if currWeek < week.week:
            currWeek = week.week

    newWeek = Week(week=currWeek+1,
                   phase=phase_selected.phase)
    newWeek.save()
    phase_selected.weeks.add(newWeek)

    return redirect('trainplan')


def addDay(request, phaseID=None, weekID=None):
    phase_selected = Phase.objects.get(id=phaseID)
    week_selected = Week.objects.get(id=weekID)
    objects = Day.objects.filter(phase=phase_selected.phase, week=week_selected.week)
    currDay= 0
    for day in objects:
        if currDay < day.day:
            currDay = day.day

    newDay = Day(day=currDay+1,
                 phase=phase_selected.phase,
                 week=week_selected.week)
    newDay.save()
    week_selected.days.add(newDay)

    return redirect('trainplan')



def addEntry(request):

    if request.is_ajax():
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        day = request.POST.get('day', None)
        exercise = request.POST.get('exercise', None)
        reps = request.POST.get('reps', None)
        weight = request.POST.get('weight', None)
        sets = request.POST.get('sets', None)
        comment = request.POST.get('comment', None)

        print("phase "+phase)
        print("week " + week)
        print("day " + day)
        print("exercise " + exercise)
        print("reps "+ reps)
        print("weight " + weight)
        print("sets " + sets)
        print("comment "+comment)
        try:
            train_entry = TrainingEntry(
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
            day = Day.objects.get(phase=phase,week=week,day=day)
            day.entrys.add(train_entry)

        except:
            print("not saved")
            response = {
                'msg': 'Your form has not been saved'  # response message
            }

    return redirect('trainplan')



@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def trainprog(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(email=request.session['selected_client'])})
        form.fields["selected_client"].empty_label = None
    else:
        form = UserForm()
    return render(request, 'trainerInterface/trainProg.html', {'form': form})


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
            print(request.POST.get("image"))
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



