import sys
import traceback
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_token_autenticacao(sender, instance=None, created=False, **kwargs):
    if 'createsuperuser' in sys.argv:
        return

    def criar_token():
        try:
            Token.objects.get_or_create(user=instance)
        except Exception:
            print("Erro ao criar token para o usuário:")
            traceback.print_exc()  # isso vai printar o erro no terminal

    if created:
        transaction.on_commit(criar_token)