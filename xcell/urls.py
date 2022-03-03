from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('chat/', include('chat.urls')),
    path('', include('trainerInterface.urls')),
    path('', include('django.contrib.auth.urls')),
    path('signup/', Signup),
    path('signup/<str:trainer>/', SignupClient, name='signup_client'),
    path('clientsuccess/', Success, name='success_client')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
