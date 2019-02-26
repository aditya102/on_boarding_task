from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('folder/', views.FolderListView.as_view(), name="folders_list"),
    path('folder/<int:folder_id>/', views.BookmarkListView.as_view(), name='folder_detail'),
    path('create/', views.FolderCreateView.as_view(), name="folder_create"),
    path('<int:folder_id>/delete/', views.FolderDeleteView.as_view(), name="folder_delete"),
    path('folder/<int:folder_id>/create/', views.BookmarkCreateView.as_view(), name="bookmark_create"),
    path('folder/<int:bookmark_id>/delete', views.BookmarkDeleteView.as_view(), name='bookmark_delete'),
    path('<folder_id>/edit/', views.FolderUpdateView.as_view(), name="folder_update"),
]
