from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        self.helper = FormHelper(self)


class EditTask(forms.Form):
    pass


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user