from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

from task.models import Task
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task",
            "start_time",
            "end_time",
            "content",
            # "tag",
        ]
        widgets = {
            'start_time': forms.DateTimeInput(),
            'end_time': forms.DateTimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].widget.attrs.update({'class': 'task-input-2',
                                                 'placeholder': 'What do you need to do today?',
                                                 })
        self.fields['content'].widget.attrs.update({'class': 'content-input-2',
                                                    'placeholder': 'You can add additional information here',
                                                 })
        # self.helper = FormHelper(self)


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'task-input-2 border-bottom',
            'placeholder': '••••••',
        }))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'task-input-2 border-bottom',
            'placeholder': '••••••',
        }))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'task-input-2 border-bottom',
            'placeholder': '••••••',
        }))

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={
            'class': 'task-input-2 border-bottom',
            'placeholder': '••••••',
        }))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'task-input-2 border-bottom',
            'placeholder': '••••••',
        }))