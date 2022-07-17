import json
from django.http import JsonResponse
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
import openpyxl
from trainerInterface.views import is_ajax

def exercises(request):
    request.session["href"] = '/dashboard/exercises/'
    exercises = ExerciseType.objects.all().order_by('name')

    if request.method == "POST":
        if request.FILES['excel_file']:
            print(request.FILES['excel_file'])

        # if 'uploadFile' in request.POST:
        #     excel_file = request.FILES["excel_file"]

        #     # you may put validations here to check extension or file size
        #     wb = openpyxl.load_workbook(excel_file.temporary_file_path())

        #     # getting a particular sheet by name out of many sheets
        #     worksheet = wb["Sheet1"]
        #     print(worksheet)

        #     worksheet.delete_rows(0)
        #     for row in worksheet.iter_rows():
        #         if not ExerciseType.objects.filter(name=row[0].value).exists():
        #             exercise = ExerciseType(
        #                 name=row[0].value,
        #                 description=row[1].value,
        #                 video=row[2].value,
        #             )
        #             exercise.save()
        #             print("exercise " + exercise.name + " saved")
        #         else:
        #             exercise = ExerciseType.objects.get(name=row[0].value)
        #             exercise.description = row[1].value
        #             exercise.video = row[2].value
        #             exercise.save()
        #             print("exercise " + row[0].value + " updated")
        # if 'addExercise' in request.POST:

        #     addedExercise = AddExercise(request.POST, request.FILES)
        #     if addedExercise.is_valid():
        #         name = addedExercise.cleaned_data.get("name")
        #         description = addedExercise.cleaned_data.get("description")
        #         image = addedExercise.cleaned_data.get("image")
        #         video = addedExercise.cleaned_data.get("video")
        #         if not ExerciseType.objects.filter(name=name).exists():
        #             exercise = ExerciseType(
        #                 name=name,
        #                 description=description,
        #                 image=image,
        #                 video=video,
        #             )
        #             exercise.save()
        #             print("exercise " + name + " saved")
        #         else:
        #             exercise = ExerciseType.objects.get(name=name)
        #             exercise.description = description
        #             exercise.image = image
        #             exercise.video = video
        #             exercise.save()
        #             print("exercise " + name + " updated")

    return render(request, 'trainerInterface/exercises.html', {'exercises': exercises})


def deleteExercise(request):
    if is_ajax(request):
        try:
            id = request.POST.get('id', None)
            object = ExerciseType.objects.get(id=id)
            object.delete()
            response = {
                'success': 'exercise deleted!'
            }
        except:
            response = {
                'error': 'Could not delete exercise!'
            }

        return JsonResponse(response)


def editExercise(request):

    if is_ajax(request):
        id = request.POST.get('id', None)
        title = request.POST.get('title', None)
        url = request.POST.get('new_url', None)
        description = request.POST.get('description', None)
        try:
            exercise = ExerciseType.objects.get(id=id)
            if title != None:
                exercise.name = title
                response = {
                    'success': 'Exercise title updated!'
                }
            elif url != None:
                exercise.video = url
                response = {
                    'success': 'Exercise url updated!'
                }
            elif description != None:
                exercise.description = description
                response = {
                    'success': 'Exercise description updated!'
                }
            else:
                response = {
                    'error': 'No update received'
                }
            exercise.save()

        except:
            response = {
                'error': 'failed to update the exercise!'  # response message
            }
        return JsonResponse(response)


def addExercise(request):

    if is_ajax(request):
        title = request.POST.get('title', None)
        video = request.POST.get('video', None)
        description = request.POST.get('description', None)
        try:
            exercise = ExerciseType(
                name=title, description=description, video=video, creater=request.user)
            exercise.save()

            response = {
                'id': exercise.id,
                'success': 'New Exercise Created!'  # response message
            }
        except:
            response = {
                'error': 'Failed to create the exercise!'  # response message
            }
        return JsonResponse(response)
