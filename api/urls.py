from django.urls import path
from .views import *
from chat.views import message_list, load_messages
from rest_framework.authtoken import views

app_name = 'api'
urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('image/<int:id>/', imageDisplay, name='image'),
    path('messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('messages/', message_list, name='message-list'),
    path('loadmessages/', load_messages.as_view(), name='load_message'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('register/', Registration.as_view(), name="register"),
    path('data/', TrainingData.as_view(), name='training data'),
    path('exercise/', ExerciseData.as_view(), name='exercise data'),
    path('sets/', SetEntry.as_view(), name='set data'),
    path('groups/', TrackingData.as_view(), name='group_data'),

]