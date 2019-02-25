from django.contrib import admin
from apps.users.models import User
from apps.bookmarks.models import Bookmark, Folder
# Register your models here.

admin.site.register(User)
admin.site.register(Bookmark)
admin.site.register(Folder)
