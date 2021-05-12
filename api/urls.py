from django.urls import path
from .views import UserRecordView, TrainingData, imageDisplay


app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('image/<int:id>/', imageDisplay, name='image'),
]