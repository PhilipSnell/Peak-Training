
from django.urls import path, include # new
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/exercises/', exercises, name='exercises'),
    path('dashboard/trainplan/', trainplan, name='trainplan'),
    path('dashboard/trainprog/', trainprog, name='trainprog'),
    path('dashboard/delete/<int:id>/', deleteExercise, name='delete_exercise'),

]

