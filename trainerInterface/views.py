from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from api.models import ExerciseType
import openpyxl

def home(request):
    context = {

    }
    return render(request, 'trainerInterface/home.html', context=context)

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dashboard(request):
    context = {

    }
    return render(request, 'trainerInterface/dashboard.html', context=context)

@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def upload(request):
    if "GET" == request.method:
        return render(request, 'trainerInterface/upload.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size
        #wb = xlrd.open_workbook(excel_file.temporary_file_path())
        wb = openpyxl.load_workbook(excel_file.temporary_file_path())

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        worksheet.delete_rows(0)
        for row in worksheet.iter_rows():
            if not ExerciseType.objects.filter(name=row[0].value).exists():
                exercise = ExerciseType(
                    name=row[0].value,
                    description=row[1].value,
                    video=row[2].value,
                )
                exercise.save()
                print("exercise "+ exercise.name + " saved")
            else:
                print("exercise " + row[0].value + " not saved")

            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        return render(request, 'trainerInterface/upload.html', {"excel_data": excel_data})

