from django import forms
from django.contrib.auth import get_user_model
from api.models import MyAccountManager
from api.models import *
User = get_user_model()
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.forms import UserCreationForm

class AddTrainerForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'username_input'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'fname_input'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'lname_input'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'email_input'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'pword_input'}))

    def create(self):
        user = User.objects.create_traineruser(**self.cleaned_data)
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        extra_kwags= {
            'password': {'write_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    def save(self):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user


class AddClientForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'username_input'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'fname_input'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'lname_input'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'email_input'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'pword_input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

    def create(self):
        user = User.objects.create_user(**self.cleaned_data)
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        extra_kwags= {
            'password': {'write_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    def save(self):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user