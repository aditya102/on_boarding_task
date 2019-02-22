from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('folder/', views.FolderListView.as_view(), name="folders_lsit"),
    path('bookmarks/', views.BookmarkListView.as_view(), name="bookmarks_list"),
]   
