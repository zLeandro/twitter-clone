from django.db import models
from django.conf import settings


class Postagem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relacionando ao usuário
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Postagem de {self.user.username} em {self.data_criacao}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='likes')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'postagem')

    def __str__(self):
        return f"{self.user.username} curtiu {self.postagem.id}"