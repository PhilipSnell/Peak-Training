from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from api.models import ExerciseType
from .form import *
import openpyxl
from django.contrib.auth import get_user_model
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
    phases = defaultdict(lambda: defaultdict(list))
    for entry in trainingEntries:
        #phases[entry.phase].append(entry.week)
        phases[entry.phase][entry.week].append(entry)
    print(phases)

    return render(request, 'trainerInterface/trainPlan.html', {'form': form, 'phases': phases.items()})


@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def deleteExercise(request, id=None):
    object = ExerciseType.objects.get(id=id)
    object.delete()

    return redirect('exercises')


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



