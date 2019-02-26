from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import Folder, Bookmark
from .forms import FolderCreateForm, BookmarkCreateForm, FolderUpdateForm


class FolderListView(LoginRequiredMixin, ListView):

    model = Folder
    template_name = 'bookmarks/folder_list.html'
    context_object_name = 'folders'
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


class FolderDeleteView(LoginRequiredMixin, DeleteView):
    model = Folder
    template_name = 'bookmarks/folder_delete_confirm.html'

    def get_object(self):
        id = self.kwargs.get('folder_id')
        return get_object_or_404(Folder, id=id)

    def get_success_url(self):
        return reverse('bookmarks:folders_list')

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()

        if folder.name == "Uncategorized":
            for bookmark in folder.bookmark_set.all():
                bookmark.delete()
            folder.delete()
            return HttpResponseRedirect(reverse('bookmarks:folders_list'))

        if Folder.objects.filter(name='Uncategorized', created_by=self.request.user).exists():
            uncategorized_folder = Folder.objects.get(name="Uncategorized", created_by=self.request.user)
        else:
            uncategorized_folder = Folder.objects.create(name='Uncategorized', created_by=self.request.user)

        for bookmark in folder.bookmark_set.all():
            bookmark.folder = uncategorized_folder
            bookmark.save()
        folder.delete()
        return HttpResponseRedirect(reverse('bookmarks:folders_list'))


class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Bookmark
    template_name = 'bookmarks/bookmark_delete_confirm.html'

    def get_object(self):
        id = self.kwargs.get('bookmark_id')
        return get_object_or_404(Bookmark, id=id)

    def get_success_url(self):
        return reverse('bookmarks:folders_list')

        def get_queryset(self):
            qs = super().get_queryset()
            return qs.filter(created_by=self.request.user)


class FolderUpdateView(LoginRequiredMixin, UpdateView):
    model = Folder
    form_class = FolderUpdateForm
    template_name = 'bookmarks/folder_update_form.html'

    def get_object(self):
        id = self.kwargs.get('folder_id')
        return get_object_or_404(Folder, id=id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_queryset(self):
        return Folder.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse('bookmarks:folders_list')