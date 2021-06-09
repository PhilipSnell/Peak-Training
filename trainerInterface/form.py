from django import forms
from django.contrib.auth import get_user_model
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

