
from django import forms
from .models import Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm, DateInput
from em_website.models import Event

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            ]