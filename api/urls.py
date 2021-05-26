from django.urls import path
from .views import UserRecordView, TrainingData, imageDisplay
from chat.views import message_list


app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('image/<int:id>/', imageDisplay, name='image'),
    path('messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('messages/', message_list, name='message-list'),
]