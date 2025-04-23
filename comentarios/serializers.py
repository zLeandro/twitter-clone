from rest_framework import serializers
from .models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'user', 'postagem', 'conteudo', 'data_criacao']
        read_only_fields = ['user', 'data_criacao', 'postagem']