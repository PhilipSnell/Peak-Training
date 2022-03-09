
from django.urls import path, include

from trainerInterface.splitViews.graph import *
from trainerInterface.splitViews.daily_tracking import dailyTracking
from trainerInterface.splitViews.training_progress import *
from trainerInterface.splitViews.training_plan import *
from trainerInterface.splitViews.exercises import *
from trainerInterface.splitViews.data_tracking import *
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [


    path('', login_required(home), name='home'),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('dashboard/exercises/', login_required(exercises), name='exercises'),
    path('dashboard/trainplan/', login_required(trainplan), name='trainplan'),
    path('dashboard/trainprog/', login_required(trainprog), name='trainprog'),
    path('dashboard/dataTracking/',
         login_required(dataTracking), name='dataTracking'),
    path('dashboard/dailyTracking/',
         login_required(dailyTracking), name='dailyTracking'),
    path('dashboard/clients/', login_required(clients), name='clients'),

    path('dashboard/phaseDropdown/',
         login_required(phaseDropdown), name='phaseDropdown'),
    path('dashboard/weekDropdown/',
         login_required(weekDropdown), name='weekDropdown'),
    path('dashboard/getdata/', login_required(getData), name='getData'),
    path('dashboard/getDays/', login_required(getDays), name='get_days'),
    path('dashboard/getDayData/', login_required(getDayTableData), name='get_days'),
    path('dashboard/getDayDataProg/',
         login_required(getDayTableDataProg), name='get_days_progress'),
    path('dashboard/deleteexercise/',
         login_required(deleteExercise), name='delete_exercise'),
    path('dashboard/addPhase/', login_required(addPhase), name='add_phase'),
    path('dashboard/addWeek/', login_required(addWeek), name='add_week'),
    path('dashboard/addDay/', login_required(addDay), name='add_day'),
    path('dashboard/addExercise/', login_required(addExercise), name='add_exercise'),
    path('dashboard/addentry/', login_required(addEntry), name='add_entry'),
    path('dashboard/deleteentry/', login_required(deleteEntry), name='delete_entry'),
    path('dashboard/editentry/', login_required(editEntry), name='edit_entry'),
    path('dashboard/addgroup/', login_required(addGroup), name='add_group'),
    path('dashboard/editgroup/', login_required(editGroup), name='edit_group'),
    path('dashboard/toggleWeek/', login_required(toggleActiveWeek),
         name='toggle_active_week'),
    path('dashboard/checkActiveWeek/',
         login_required(checkActiveWeek), name='check_active_week'),
    path('dashboard/cloneWeek/', login_required(cloneWeek), name='clone_week'),
    path('dashboard/getClonePhases/',
         login_required(getClonePhases), name='get_clone_phases'),
    path('dashboard/changeOrder/', login_required(changeOrder), name='change_order'),
    path('dashboard/graph/', login_required(graphTracking), name='graph'),
    path('dashboard/getGraphData/',
         login_required(getGraphData), name='graph_data'),
    path('dashboard/editexercise/',
         login_required(editExercise), name='edit_exercise'),
    path('dashboard/linkvalues/', login_required(linkValues), name='link'),
    path('dashboard/togglefield/', login_required(toggleField), name='toggle_field'),
    path('dashboard/togglegroup/', login_required(toggleGroup), name='toggle_group'),
]
