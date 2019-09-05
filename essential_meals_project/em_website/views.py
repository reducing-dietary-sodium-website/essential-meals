from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
	return redirect("../accounts/login")

def hello(request):
	return render(request, "helloworld.html")

def login(request):
	return render(request, "Registration/login.html", {'title': 'Login'})

def home(request):
	return render(request, "home.html", {'title': 'Home'})

def main(request):
	return redirect("accounts/login")