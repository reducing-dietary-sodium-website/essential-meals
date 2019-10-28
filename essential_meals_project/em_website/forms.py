from django import forms
from .models import Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Recipe

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class NewRecipeForm(forms.ModelForm):
     class Meta:
         model = Recipe
         fields = ['title',
                   'ingredients',
                    'preparation',
                    'time_for_preparation',
                    'number_of_portions',
                    'difficulty',
                    ]
     
class EditProfileForm(UserChangeForm):

	class Meta:
		model = User
		fields = [
			'email',
			'first_name',
			'last_name',
			'password',
			]