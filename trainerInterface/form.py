from django import forms
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalModelForm
from api.models import *
User = get_user_model()


class UserForm(forms.Form):
    selected_client = forms.ModelChoiceField(queryset=User.objects.all(), label="", widget=forms.Select(
        attrs={'onchange': 'this.form.submit();', 'class': 'dropdown', 'name': "change_client"}))

    class Meta:
        model = User# Please use CamelCase when defining model class name
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['selected_client'].empty_label = "Select a Client"

class AddExercise(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    image = forms.ImageField()
    video = forms.URLField()

    class Meta:
        model = ExerciseType# Please use CamelCase when defining model class name
        fields = ['name', 'description', 'image', 'video']
    def __init__(self, *args, **kwargs):
        super(AddExercise, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class AddTrainingEntry(BSModalModelForm):
    exercise = forms.ModelChoiceField(queryset=ExerciseType.objects.order_by('name'), widget=forms.Select(attrs={'id': 'exercisefield'}))
    reps = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'repfield'}))
    weight = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'weightfield'}))
    sets = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'setfield'}))
    comment = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'commentfield'}))

    class Meta:
        model = TrainingEntry# Please use CamelCase when defining model class name
        fields = ['reps', 'weight', 'sets', 'comment', 'exercise']


class GroupAddForm(BSModalModelForm):
    name = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'class': 'groupname',
                                                                                  'id': 'groupname',
                                                                                  'placeholder': 'Insert Group Name'}))

    class Meta:
        model = TrackingGroup# Please use CamelCase when defining model class name
        fields = ['name']


class GroupFieldForm(BSModalModelForm):
    fieldname = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'id': 'fieldname', 'placeholder':
        'Item name'}))

    class Meta:
        model = TrackingGroup# Please use CamelCase when defining model class name
        fields = ['fieldname']

