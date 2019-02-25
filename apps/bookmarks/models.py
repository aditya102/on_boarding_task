from django.db import models

from apps.users.models import User


class Folder(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    url = models.URLField(max_length=230)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
