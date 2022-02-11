from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
import openpyxl


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

    form = getUserform(request)

    return render(request, 'trainerInterface/exercises.html', {'form': form, 'exercises': exercises, 'exerciseForm': exerciseForm})


def deleteExercise(request, id=None):
    object = ExerciseType.objects.get(id=id)
    object.delete()

    return redirect('exercises')
