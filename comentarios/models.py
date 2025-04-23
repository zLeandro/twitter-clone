from django.db import models
from django.conf import settings
from postagens.models import Postagem

class Comentario(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, related_name='comentarios', on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.postagem.id}"