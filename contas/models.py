from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

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

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

class Seguidor(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="seguindo", on_delete=models.CASCADE)
    seguido = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="seguidores", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} segue {self.seguido}"