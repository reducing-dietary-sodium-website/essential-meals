from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("Hello, World. You're at the em_website's index.")

def hello(request):
	return render(request, "helloworld.html")

def login(request):
	return render(request, "login.html", {'title': 'Login'})

def home(request):
	return render(request, "home.html", {'title': 'Home'})