from django import forms
from django.contrib.auth.models import User
from golf_app.models import Golfer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class GolferForm(forms.ModelForm):
    class Meta:
        model = Golfer
        fields = ('name',)