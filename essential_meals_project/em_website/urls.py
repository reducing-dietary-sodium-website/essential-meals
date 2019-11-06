from django.urls import path
from django.urls import path, include
from django.urls import re_path
from django.conf.urls import url

from em_website import views

urlpatterns = [
    path('', views.home, name='em_home'),
    path('login/', views.login, name='em_login'),
    path('home/', views.home, name='em_home'),
    path('profile/', views.profile, name='em_profile'),
    path('myAccount/', views.myAccount, name='em_myAccount'),
    # path('password_reset/', views.password_reset, name='em_password_reset'),
    path('password_reset_done/', views.password_reset_done, name='em_password_reset_done'),
    # path('profile/', views.Profile.as_view(), name='em_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('env/', include('django.contrib.auth.urls')),
    path('search/', views.search, name='em_search'),
    path('results/', views.results, name='em_results'),
    path('view_recipe/<slug:recipe>/', views.view_recipe, name='em_view_recipe'),
    path('view_recipe/<slug:recipe>/post', views.view_recipe, name='em_view_recipe'),
   
    #path('recipes/',views.detail,name = 'detail'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    #re_path(r'boards/(?P<pk>\d+)/category/(?P<slug>\d+)/details$',views.detail, name = 'detail'),
    #re_path('boards/(?P<slug>\d+)/category/recipes$',views.index2, name = 'index2'),
    
    re_path(r'^recipes/(?P<slug>[-\w]+)/$',views.detail, name = 'details'),
    re_path(r'^recipes/new', views.new_recipe, name = 'new_recipe'),
    re_path(r'^recipes', views.index2, name = 'index2'),
    path('calendar/', views.CalendarView.as_view(), name='em_calendar'),
]
