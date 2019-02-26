from django.contrib import admin
from .models import Folder, Bookmark
from apps.users.models import User

# Register your models here.
admin.site.register(Folder)
admin.site.register(Bookmark)
admin.site.register(User)