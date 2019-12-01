# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
from django import forms



# class User(AbstractUser):
#     numOfPatrons = models.IntegerField(default=1)

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,on_delete = models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User,on_delete = models.CASCADE, related_name='topics')


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,on_delete = models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User,on_delete = models.CASCADE, null=True, related_name='+')
    #test1 = models.CharField(max_length= 100, null = True)
class Category(models.Model):
    """
    A model class describing a category.
    """
    name = models.CharField(u'Name', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(u'Description', blank=True)

    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'

    def __unicode__(self):
        return self.name
class Recipe(models.Model):
    """
    A model describing a coobook recipe.
    """
    title = models.CharField(u'Title', max_length=255)
    slug = models.SlugField(unique=True)
    ingredients = models.TextField(u'Ingredients',
        help_text=u'One ingredient per line')
    preparation = models.TextField(u'Preparation')
    time_for_preparation = models.IntegerField(u'Preparation time',
        help_text=u'How many minutes will it take?', blank=True, null=True,default = 15)
    number_of_portions = models.PositiveIntegerField(u'Number of portions',default = 1)
    author = models.ForeignKey(User,on_delete = models.CASCADE, verbose_name=u'Author')
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    class Meta:
        verbose_name = u'Recipe'
        verbose_name_plural = u'Recipes'
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Recipe, self).save(*args, **kwargs)


class SavedRecipe(models.Model):
    """
    A model class describing a saved recipe.
    """
    name = models.CharField(u'Name', max_length=100)
    user = models.CharField(u'User', max_length=100)
    slug = models.SlugField(unique=False)

    class Meta:
        verbose_name = u'Saved Recipe'
        verbose_name_plural = u'Saved Recipes'
        ordering = ['name', 'user']

    def __unicode__(self):
        return self.name

class Event(models.Model):


#     # print(saved_recipes)
#     title = models.CharField(max_length=2, choices=[])
#     # meals = models.CharField(max_length=2)
#     # description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     @property
#     def get_html_url(self):
#         url = reverse('event_edit', args=(self.id,))
#         return f'<a href="{url}"> {self.title} </a>'

#     def set_recipes(self, user):
#         saved_recipes = SavedRecipe.objects.filter(user=user)
#         recipes = []
#         for recipe in saved_recipes:
#             recipes.append((recipe.name, recipe.name))
#         self.title = models.CharField(max_length=2, choices=recipes)


    recipe = models.CharField(max_length=200)
    slug = models.CharField(u'Link', max_length=100, null=True)
    start_time = models.DateField()
    user = models.CharField(u'Calendar', max_length=100, null=True)

    @property
    def get_html_url(self):
        print(self.slug)
        url = reverse('em_view_recipe', args=(self.slug,))
        return f'<a href="{url}"> {self.recipe} </a>'

class WeekOfNutrients(models.Model):
    user = models.CharField(null = False, max_length=100)
    start_monday = models.DateField()
    end_sunday = models.DateField()
    sodium_day1 = models.PositiveIntegerField(u'Monday Sodium',default = 0)
    sodium_day2 = models.PositiveIntegerField(u'Tuesday Sodium',default = 0)
    sodium_day3 = models.PositiveIntegerField(u'Wednesday Sodium',default = 0)
    sodium_day4 = models.PositiveIntegerField(u'Thursday Sodium',default = 0)
    sodium_day5 = models.PositiveIntegerField(u'Friday Sodium',default = 0)
    sodium_day6 = models.PositiveIntegerField(u'Saturday Sodium',default = 0)
    sodium_day7 = models.PositiveIntegerField(u'Sunday Sodium',default = 0)
    calories_day1 = models.PositiveIntegerField(u'Monday Calories',default = 0)
    calories_day2 = models.PositiveIntegerField(u'Tuesday Calories',default = 0)
    calories_day3 = models.PositiveIntegerField(u'Wednesday Calories',default = 0)
    calories_day4 = models.PositiveIntegerField(u'Thursday Calories',default = 0)
    calories_day5 = models.PositiveIntegerField(u'Friday Calories',default = 0)
    calories_day6 = models.PositiveIntegerField(u'Saturday Calories',default = 0)
    calories_day7 = models.PositiveIntegerField(u'Sunday Calories',default = 0)
