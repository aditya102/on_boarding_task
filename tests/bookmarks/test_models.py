from django.test import TestCase
from apps.bookmarks.models import Folder, Bookmark

from apps.bookmarks.factory import UserFactory, FolderFactory, BookmarkFactory


class ModelTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.folder1 = FolderFactory(created_by=self.user)
        self.folder2 = FolderFactory(created_by=self.user)
        self.folder3 = FolderFactory(created_by=self.user)
        self.bookmark1 = BookmarkFactory(created_by=self.user, folder=self.folder1)
        self.bookmark2 = BookmarkFactory(created_by=self.user, folder=self.folder2)
        self.bookmark3 = BookmarkFactory(created_by=self.user, folder=self.folder3)

    def test_folder_ordering(self):
        self.assertQuerysetEqual(Folder.objects.all(), Folder.objects.all().order_by('name'), lambda x: x)

    def test_bookmark_ordering(self):
        self.assertQuerysetEqual(Bookmark.objects.all(), Bookmark.objects.all().order_by('name'), lambda x: x)
