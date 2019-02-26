from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Folder, Bookmark
from .forms import FolderCreateForm, BookmarkCreateForm


class FolderListView(LoginRequiredMixin, ListView):

    model = Folder
    template_name = 'bookmarks/folder_list.html'
    context_object_name = 'folders'
    paginate_by = 10
    ordering = ['name']


class BookmarkListView(LoginRequiredMixin, ListView):

    model = Bookmark
    template_name = 'bookmarks/folder_detail.html'
    context_object_name = 'bookmarks'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder = Folder.objects.filter(created_by=self.request.user).get(pk=self.kwargs['folder_id'])
        context["bookmarks"] = folder.bookmark_set.all()
        context["folder_id"] = folder.id
        return context


class FolderCreateView(LoginRequiredMixin, CreateView):
    form_class = FolderCreateForm
    template_name = 'bookmarks/folder_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        url = reverse('bookmarks:folders_list')
        return url


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    form_class = BookmarkCreateForm
    template_name = 'bookmarks/bookmark_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'folder': self.kwargs['folder_id']})
        return kwargs

    def get_success_url(self):
        url = reverse('bookmarks:folders_list')
        return url
