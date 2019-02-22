from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Folder, Bookmark


class FolderListView(LoginRequiredMixin, ListView):

    model = Folder
    template_name = 'bookmarks/folder_list.html'
    context_object_name = 'folders'
    paginate_by = 10
    ordering = ['name']


class BookmarkListView(LoginRequiredMixin, ListView):

    model = Bookmark
    template_name = 'bookmarks/bookmark_list.html'
    context_object_name = 'bookmarks' 
    ordering = ['name']