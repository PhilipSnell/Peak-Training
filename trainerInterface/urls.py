
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
    path('dashboard/addPhase/', addPhase, name='add_phase'),
    path('dashboard/addWeek/<int:phaseID>/', addWeek, name='add_week'),
    path('dashboard/addDay/<int:phaseID>/<int:weekID>/', addDay, name='add_day'),
    # path('dashboard/addExercise/<int:phaseID>/<int:weekID>/<int:dayID>/', addEntry, name='add_entry'),
    path('dashboard/addentry/', addEntry, name='add_entry'),

]

