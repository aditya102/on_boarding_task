import factory

from apps.users.models import User
from apps.bookmarks.models import Folder, Bookmark


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')


class FolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Folder

    name = factory.Faker('name')
    created_by = factory.SubFactory(UserFactory)


class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    folder = factory.SubFactory(FolderFactory)
    name = factory.Faker('name')
    url = factory.Faker('url')
    created_by = factory.SubFactory(UserFactory)
