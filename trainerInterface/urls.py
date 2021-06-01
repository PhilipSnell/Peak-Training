
from django.urls import path, include # new
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/upload/', upload, name='upload'),

]
