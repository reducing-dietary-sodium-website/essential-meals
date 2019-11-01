from django.contrib import admin


from .models import Board,Topic,Post,Category,Recipe
# Register your models here.
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Recipe)