from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required


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
    context = {

    }
    return render(request, 'trainerInterface/upload.html', context=context)
