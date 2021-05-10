from django.urls import path
from .views import UserRecordView, UserCreate

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('register', UserCreate.as_view()),
]