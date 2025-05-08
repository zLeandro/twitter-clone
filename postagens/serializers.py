from rest_framework import serializers
from .models import Postagem, Like

class PostagemSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Postagem
        fields = ['id', 'username', 'conteudo', 'data_criacao', 'total_likes', 'avatar']

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_username(self, obj):
        return obj.user.username

    def get_avatar(self, obj):
        avatar = getattr(obj.user, 'profile_picture', None)
        if avatar and hasattr(avatar, 'url'):
            return avatar.url
        return ''
