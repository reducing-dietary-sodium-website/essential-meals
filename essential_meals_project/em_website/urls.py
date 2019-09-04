from django.urls import path
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='helloworld'),
    path('login/', views.login, name='em_login'),
    path('home/', views.home, name='em_home'),
    path('env/', include('django.contrib.auth.urls')),
]