from django.contrib import admin
from .models import Board,Topic,Post,Category,Recipe,Event, SavedRecipe, WeekOfNutrients
# Register your models here.
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(SavedRecipe)
admin.site.register(Event)
admin.site.register(WeekOfNutrients)