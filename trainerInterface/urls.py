
from django.urls import path, include

from trainerInterface.splitViews.graph import graphTracking
from trainerInterface.splitViews.daily_tracking import dailyTracking
from trainerInterface.splitViews.training_progress import *
from trainerInterface.splitViews.training_plan import *
from trainerInterface.splitViews.exercises import *
from .views import *

urlpatterns = [


    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/exercises/', exercises, name='exercises'),
    path('dashboard/trainplan/', trainplan, name='trainplan'),
    path('dashboard/trainprog/', trainprog, name='trainprog'),
    path('dashboard/dataTracking/', dataTracking, name='dataTracking'),
    path('dashboard/dailyTracking/', dailyTracking, name='dailyTracking'),
    path('dashboard/clients/', clients, name='clients'),


    path('dashboard/phaseDropdown/', phaseDropdown, name='phaseDropdown'),
    path('dashboard/weekDropdown/', weekDropdown, name='weekDropdown'),
    path('dashboard/getDays/', getDays, name='get_days'),
    path('dashboard/getDayData/', getDayTableData, name='get_days'),
    path('dashboard/getDayDataProg/',
         getDayTableDataProg, name='get_days_progress'),
    path('dashboard/delete/<int:id>/', deleteExercise, name='delete_exercise'),
    path('dashboard/addPhase/', addPhase, name='add_phase'),
    path('dashboard/addWeek/', addWeek, name='add_week'),
    path('dashboard/addDay/', addDay, name='add_day'),
    # path('dashboard/addExercise/<int:phaseID>/<int:weekID>/<int:dayID>/', addEntry, name='add_entry'),
    path('dashboard/addentry/', addEntry, name='add_entry'),
    path('dashboard/deleteentry/', deleteEntry, name='delete_entry'),
    path('dashboard/editentry/', editEntry, name='edit_entry'),
    path('dashboard/addgroup/', addGroup, name='add_group'),
    path('dashboard/editgroup/', editGroup, name='edit_group'),
    path('dashboard/toggleWeek/', toggleActiveWeek, name='toggle_active_week'),
    path('dashboard/checkActiveWeek/', checkActiveWeek, name='check_active_week'),
    path('dashboard/cloneWeek/', cloneWeek, name='clone_week'),
    path('dashboard/getClonePhases/', getClonePhases, name='get_clone_phases'),
    path('dashboard/changeOrder/', changeOrder, name='change_order'),
    path('dashboard/graph/', graphTracking, name='graph'),
    path('dashboard/editexercise/', editExercise, name='edit_exercise'),
]
