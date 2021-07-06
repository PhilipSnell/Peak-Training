from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import *


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_trainer')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "description","image","video")
    search_fields = ("name","description")


#admin.site.register(TrackingIntValue)
admin.site.register(TrackingTextValue)
# admin.site.register(DailyTracking)
admin.site.register(TrackingTextField)
#admin.site.register(TrackingIntField)
admin.site.register(TrackingGroup)
admin.site.register(Day)
admin.site.register(Week)
admin.site.register(Phase)
admin.site.register(Trainer)
admin.site.register(Set_Entry)
admin.site.register(Account, AccountAdmin)
admin.site.register(ExerciseType, ExerciseAdmin)
admin.site.register(TrainingEntry)
admin.site.register(Message)
# Register your models here.
