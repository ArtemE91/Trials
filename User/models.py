from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    avatar = models.FileField(upload_to=None, null=True, blank=True)
    date_of_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def get_avatar(self):
        if not self.avatar.name:
            return f'{settings.MEDIA_URL}/user/avatar.png'
        return f'{settings.MEDIA_URL}/{self.avatar.name}'

