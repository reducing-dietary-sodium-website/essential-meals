from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("Hello, World. You're at the em_website's index.")
# def login(request):
# 	return render(request, 'login.html')