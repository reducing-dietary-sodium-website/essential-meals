from django import forms
from .models import Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Recipe, SavedRecipe
from django.forms import ModelForm, DateInput, ModelChoiceField
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

class NewRecipeForm(forms.ModelForm):
     class Meta:
         model = Recipe
         fields = ['title',
                   'ingredients',
                    'preparation',
                    'time_for_preparation',
                    'number_of_portions',
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

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = [
      'recipe',
      'start_time',
      ]

  def __init__(self, user, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    recipes = [([recipe[0], recipe[1]], recipe[1]) for recipe in SavedRecipe.objects.filter(user=user).values_list('slug', 'name').distinct()]
    self.fields['recipe'] = forms.ChoiceField(choices=recipes)
    # input_formats to parse HTML5 datetime-local input to datetime field
<<<<<<< HEAD
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['meals'] = ModelChoiceField(queryset=SavedRecipe.objects.filter(user=user))
=======
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
>>>>>>> 9433bd7b5c2df865c115ccea6c83542370af0277
