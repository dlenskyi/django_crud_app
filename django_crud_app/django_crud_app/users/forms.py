from django import forms
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', ]


class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class AuthForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
