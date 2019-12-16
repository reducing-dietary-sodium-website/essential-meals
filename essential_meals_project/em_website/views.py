from django.http import HttpResponse, HttpResponseRedirect, QueryDict, Http404
# from events.forms import EventForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm, EditProfileForm, NewRecipeForm, EventForm
from .models import Board, Topic, Post, Event
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
import requests
import json
import datetime
from django.template import Context, loader
from .models import Recipe, SavedRecipe, Event, WeekOfNutrients
from django.http import Http404
from django.template.defaultfilters import slugify
import calendar
from datetime import timedelta, date
from .utils import Calendar
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core import serializers
from django.forms.models import model_to_dict
import ast
import plotly.express as px
import plotly.offline as opy
import plotly.graph_objs as go



# Create your views here.
# def index(request):
# 	return redirect("../accounts/login")

# def signup(request):
#     return render(request, "signup.html", {'title': 'Password Reset'})

def profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('../home')
	else:
		form = EditProfileForm(instance=request.user)
		args = {'form': form}
		return render(request, 'profile.html', args)

def myAccount(request):
    return render(request, "myAccount.html", {'title': 'myAccount'})

def login(request):
	return render(request, "em_website/Registration/login.html", {'title': 'Login'})

# def password_reset(request):
#     return render(request, "em_website/password_reset.html", {'title': 'Password Reset'})

def password_reset_done(request):
    return render(request, "Registration/password_reset_done.html", {'title': 'Password Reset Done'})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'em_website/signup.html'

# class Profile(generic.CreateView):
#     form_class = UserChangeForm
#     success_url = reverse_lazy('login')
#     template_name = 'profile.html'

def register(request):
    return render(request, "Registration/registration.html", {'title': 'Register'})

def home(request):
	saved_recipes = SavedRecipe.objects.filter(user=request.user.username).distinct()
	return render(request, "home.html", {'saved_recipes': saved_recipes})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # <- here
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user  # <- and here
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def new_recipe(request):
     if request.method == 'POST':
         form = NewRecipeForm(request.POST)
         if form.is_valid():
             Recipe.objects.create(
                 title = form.cleaned_data.get('title'),
                 slug = slugify(form.cleaned_data.get('title')+ datetime.datetime.now().strftime('%H%M%S'))  ,
                 ingredients= form.cleaned_data.get('ingredients'),
                 preparation= form.cleaned_data.get('preparation'),
                 time_for_preparation= form.cleaned_data.get('time_for_preparation'),
                 number_of_portions= form.cleaned_data.get('number_of_portions'),
                 author = request.user
             )
             return redirect("../recipes")
     else:
         form = NewRecipeForm()
     return render(request, 'new_recipe.html',{'form': form   })

def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})

def index2(request):
    queryset = Recipe.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request,'index2.html',context)

def detail(request,slug):
    recipe = get_object_or_404(Recipe,slug = slug)
    return render(request,'detail.html',{'object':recipe})

def search(request):
    return render(request, "search.html", {'title': 'Search'})

def results(request):
    querystr = request.META['QUERY_STRING']
    query = QueryDict(querystr)
    apiKey = 'a4b86bb5aa9f429f95f5a4c850a8cfe4'
    search = 'https://api.spoonacular.com/recipes/complexSearch?query={}&instructionsRequired=true&number=20&apiKey={}'
    search = search.format(query['search'], apiKey)
    if 'vegetarian' in query:
        search = search + '&diet=vegetarian'
    if 'gluten' is query:
        search = search + '&diet=gluten-free'
    if query['sodium'] != '':
        search = search + '&maxSodium=' + query['sodium']
    print('before response')
    response1 = requests.get(search)
    print('after response')
    lists = {}
    for recipe in response1.json()['results']:
        print(recipe)
        lists[str(recipe['title'])] = (str(recipe['id']), recipe['image'])

    #custom recipes
    custom_recipes = Recipe.objects.filter(title__contains=query['search'])

    #print(lists)
    return render(request, "results.html", {'title': 'Results', 'custom_recipes' : custom_recipes,
        'recipes': lists})

def view_recipe(request, recipe):
    if request.method == 'POST':
        print("SAVING RECIPE")
        SavedRecipe.objects.create(
            name = request.session['name'],
            user = request.session['user'],
            slug = request.session['slug']
        )
        return render(request, "custom_recipe.html", {'recipe' : request.session['curr'], 'fromAPI' : request.session['fromAPI']})
    else:
        fromAPI = recipe.isnumeric()
        if fromAPI:
            apiKey = 'a4b86bb5aa9f429f95f5a4c850a8cfe4'
            result = 'https://api.spoonacular.com/recipes/{}/information?includeNutrition=True&apiKey={}'
            result = result.format(recipe, apiKey)
            response1 = requests.get(result)

            toShow = {}
            toShow['title'] = response1.json()['title']
            toShow['number_of_servings'] = response1.json()['servings']
            ingredients = ''
            for ingredient in response1.json()['extendedIngredients']:
                ingredients += ingredient['original'] + '\n'
            for nutrient in response1.json()['nutrition']['nutrients']:
                if nutrient['title'] == 'Calories':
                    toShow['calories'] = str(int(nutrient['amount'])) + nutrient['unit']
                if nutrient['title'] == 'Sodium':
                    toShow['sodium'] = str(int(nutrient['amount'])) + nutrient['unit']
            toShow['ingredients'] = ingredients
            toShow['preparation'] = response1.json()['instructions']
            toShow['author'] = response1.json()['sourceName']
            toShow['source'] = response1.json()['sourceUrl']
            request.session['name'] = toShow['title']
            request.session['calories'] = toShow['calories']
            request.session['sodium'] = toShow['sodium']
        if not fromAPI:
            results = Recipe.objects.filter(slug=recipe)
            single = Recipe.objects.get(slug=recipe)
            toShow = model_to_dict(single)
            #toShow = serializers.serialize('json', results)[1:-1]
            print(toShow)
            request.session['name'] = toShow['title']
        request.session['user'] = request.user.username
        request.session['slug'] = recipe
        request.session['curr'] = toShow
        request.session['fromAPI'] = fromAPI
        return render(request, "custom_recipe.html", {'recipe' : toShow, 'fromAPI' : fromAPI})

# def analysis(request):

#     return render(request, "analysis.html", {'title': 'Analysis'})
class Analysis(generic.TemplateView):
    template_name = 'analysis.html'

    def get_context_data(self, **kwargs):
        context = super(Analysis, self).get_context_data(**kwargs)
        today = datetime.datetime.today()
        curr_week = today - datetime.timedelta(days=today.weekday())
        try:
            nutrients = WeekOfNutrients.objects.get(user=self.request.user.username, start_monday=curr_week)
            x = [x for x in range(7)]
            y = [nutrients.sodium_day1, nutrients.sodium_day2, nutrients.sodium_day3, nutrients.sodium_day4, nutrients.sodium_day5, nutrients.sodium_day6, nutrients.sodium_day7]
            trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                                mode="lines",  name='1st Trace')

            data=go.Data([trace1])
            layout=go.Layout(title="Weekly Sodium", xaxis={'title':'Day (Starting with Monday)'}, yaxis={'title':'Sodium (mg)'})
            figure=go.Figure(data=data,layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')
            context['graph'] = div
        except WeekOfNutrients.DoesNotExist:
            context['graph'] = None

        return context


class CalendarView(generic.ListView):
    model = Event
    template_name = 'em_website/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # For calling previous/next month
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.user.username, request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        meal = form.save(commit=False)
        print('RECIPE', request.POST['recipe'], type(request.POST['recipe']))
        rec = ast.literal_eval(request.POST['recipe'])
        meal.user = request.user.username
        meal.slug = rec[0]
        meal.recipe = rec[1]
        meal.save()
        #update the nutritional information if the recipe is from the API
        if meal.slug.isnumeric():
            apiKey = 'a4b86bb5aa9f429f95f5a4c850a8cfe4'
            result = 'https://api.spoonacular.com/recipes/{}/information?includeNutrition=True&apiKey={}'
            result = result.format(rec[0], apiKey)
            response1 = requests.get(result)
            for nutrient in response1.json()['nutrition']['nutrients']:
                if nutrient['title'] == 'Calories':
                    calories = int(nutrient['amount'])
                if nutrient['title'] == 'Sodium':
                    sodium = int(nutrient['amount'])


            print(request.POST['start_time'], 'TYPE:',  type(request.POST['start_time']))
            curr_date = datetime.datetime.strptime(request.POST['start_time'], '%Y-%m-%dT%H:%M').date()
            begin_week = curr_date - datetime.timedelta(days = curr_date.weekday())
            try:
                week = WeekOfNutrients.objects.get(user=request.user.username, start_monday=begin_week)
            except WeekOfNutrients.DoesNotExist:
                week = None
            if week == None:
                WeekOfNutrients.objects.create(
                    user = request.user.username,
                    start_monday = begin_week,
                    end_sunday = begin_week + datetime.timedelta(days=6)
                )
                week = WeekOfNutrients.objects.get(user=request.user.username, start_monday=begin_week)

            if week != None:    
                day = curr_date.weekday()
                if day == 0:
                    week.sodium_day1 += sodium
                    week.calories_day1 += calories
                elif day == 1:
                    week.sodium_day2 += sodium
                    week.calories_day2 += calories
                elif day == 2:
                    week.sodium_day3 += sodium
                    week.calories_day3 += calories
                elif day == 3:
                    week.sodium_day4 += sodium
                    week.calories_day4 += calories
                elif day == 4:
                    week.sodium_day5 += sodium
                    week.calories_day5 += calories
                elif day == 5:
                    week.sodium_day6 += sodium
                    week.calories_day6 += calories
                elif day == 6:
                    week.sodium_day7 += sodium
                    week.calories_day7 += calories
                
                week.save()
            
            #TODO: Finish adding nutrition information
        return HttpResponseRedirect(reverse('em_calendar'))
    return render(request, 'em_website/event.html', {'form': form})
