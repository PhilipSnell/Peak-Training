from django.urls import path
from .views import UserRecordView, registration_view

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('register/', registration_view, name="register"),
]