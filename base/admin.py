from django.contrib import admin

# Register your models here.

from .models import Picture, Comment, Genre, Like, User

admin.site.register(Genre)
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(User)