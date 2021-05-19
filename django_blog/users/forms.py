from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(required=False, help_text='YYYY/MM/DD')
    first_name = forms.CharField(max_length=100, required=False, help_text='F.e: Taras')
    last_name = forms.CharField(max_length=100, required=False, help_text='F.e: Surname')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
