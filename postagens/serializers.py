from rest_framework import serializers
from .models import Postagem
from .models import Like

class PostagemSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Postagem
        fields = ['id', 'user', 'conteudo', 'data_criacao', 'total_likes']
        read_only_fields = ['user']

    def get_total_likes(self, obj):
        return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'postagem', 'data_criacao']
        read_only_fields = ['user', 'data_criacao']

