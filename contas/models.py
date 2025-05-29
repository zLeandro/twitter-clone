import os
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def profile_picture_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    ext = ext.lower()

    if base.endswith('.jpeg') or base.endswith('.jpg') or base.endswith('.png'):
        base = base.rsplit('.', 1)[0]

    new_filename = f"{get_random_string(12)}{ext}"

    return os.path.join('profile_pics', new_filename)

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )
    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['username']

class Seguidor(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seguindo'
    )
    seguido = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seguidores'
    )

    class Meta:
        unique_together = ('usuario', 'seguido')

    def __str__(self):
        return f'{self.usuario} segue {self.seguido}'