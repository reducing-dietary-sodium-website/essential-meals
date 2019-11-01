# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, User

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
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    DIFFICULTIES = (
        (DIFFICULTY_EASY, u'easy'),
        (DIFFICULTY_MEDIUM, u'normal'),
        (DIFFICULTY_HARD, u'hard'),
    )
    title = models.CharField(u'Title', max_length=255)
    slug = models.SlugField(unique=True)
    ingredients = models.TextField(u'Ingredients',
        help_text=u'One ingredient per line')
    preparation = models.TextField(u'Preparation')
    time_for_preparation = models.IntegerField(u'Preparation time',
        help_text=u'How many minutes will it take?', blank=True, null=True,default = 15)
    number_of_portions = models.PositiveIntegerField(u'Number of portions',default = 1)
    difficulty = models.SmallIntegerField(u'Difficulty',
        choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM)
    category = models.ManyToManyField(Category, verbose_name=u'Categories')
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

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()