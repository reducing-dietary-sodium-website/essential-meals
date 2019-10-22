from django.http import HttpResponse
from django.http import QueryDict
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm, EditProfileForm
from .models import Board, Topic, Post
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views import generic
import requests
import json
from django.template import Context, loader
from .models import Recipe
from django.http import Http404

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
	boards = Board.objects.all()
	return render(request, "home.html", {'boards': boards})

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

def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})

def index2(request,pk):
    recipes = Recipe.objects.all()
    t = loader.get_template('/index2.html')
    c = Context({'object_list': recipes})
    return HttpResponse(t.render(c))

def detail(request,slug):
    recipe = get_object_or_404(Recipe,slug = slug)
    return render(request,'detail.html',{'object':recipe})
    #recipe = get_object_or_404(Recipe,board_pk = pk,pk = recipes_pk )
    # try:
    #     recipe = Recipe.objects.get(slug=slug)
    # except Recipe.DoesNotExist:
    #     raise Http404
    # t = loader.get_template('/detail.html')
    # c = Context({'object': recipe})
    # return HttpResponse(t.render(c))

def search(request):
    return render(request, "search.html", {'title': 'Search'})

def results(request):
    querystr = request.META['QUERY_STRING']
    query = QueryDict(querystr)
    # appID = 'd2952d1f'
    # appKey = '9fda606325713a5d6aff3d0541d6c025'
    # # with open('config.json', 'r') as fh:
    # #     config = json.load(fh)
    # #     appID = config['appID']
    # #     appKey = config['appKEY']
    # task = "https://api.edamam.com/search?q={}&app_id=${}&app_key=${}&from=0&to=10&calories=591-722&nutrients[NA]=0-{}"
    # task = task.format(query['search'], appID, appKey, query['sodium'])
    # if 'vegetarian' in query:
    #     task = task + '&health=vegetarian'
    # if 'gluten' is query:
    #     task = task + '&health=gluten-free'
    # response = requests.get(task)
    # recipes = response.json()['hits']
    # lists = {}
    # for recipe in recipes:
    #     recipe = recipe['recipe']
    #     lists[str(recipe['label'])] = (str(recipe['url']), recipe['image'])
    apiKey = 'a4b86bb5aa9f429f95f5a4c850a8cfe4'
    search = 'https://api.spoonacular.com/recipes/complexSearch?query={}&instructionsRequired=true&number=20&apiKey={}'
    search = search.format(query['search'], apiKey)
    if 'vegetarian' in query:
        search = search + '&diet=vegetarian'
    if 'gluten' is query:
        search = search + '&diet=gluten-free'
    if query['sodium'] != '':
        search = search + '&maxSodium=' + query['sodium']
    response1 = requests.get(search)
    lists = {}
    print(response1.json())
    for recipe in response1.json()['results']:
        print(recipe)
        lists[str(recipe['title'])] = (str(recipe['id']), recipe['image'])
        # info = 'https://api.spoonacular.com/recipes/{}/information?includeNutrition=true'
        # info = info.format(recipe['id'])
        # response2 = requests.get()
    return render(request, "results.html", {'title': 'Results',
        'recipes': lists})

def view_recipe(request, recipe):
    # recipes = Recipe.objects.filter
    toShow = Recipe.objects.get(slug=recipe)
    return render(request, "custom_recipe.html", {'recipe' : toShow})
