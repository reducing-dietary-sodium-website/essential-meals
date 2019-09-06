from django.urls import path
from django.urls import path, include
from django.urls import re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='helloworld'),
    # path('login/', views.login, name='em_login'),
    path('home/', views.home, name='em_home'),
    path('profile/', views.profile, name='em_profile'),
    path('password_reset/', views.password_reset, name='em_password_reset'),
    path('password_reset_done/', views.password_reset_done, name='em_password_reset_done'),
    # path('profile/', views.Profile.as_view(), name='em_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('env/', include('django.contrib.auth.urls')),
    re_path('boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path('boards/(?P<pk>\d+)/new$', views.new_topic, name='new_topic'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
]