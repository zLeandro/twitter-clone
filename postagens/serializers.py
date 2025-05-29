from rest_framework import serializers
from .models import Postagem

class PostagemSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    curtido_por_mim = serializers.SerializerMethodField()

    class Meta:
        model = Postagem
        fields = ['id', 'username', 'conteudo', 'data_criacao', 'total_likes', 'avatar', 'curtido_por_mim']

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_username(self, obj):
        return obj.user.username

    def get_avatar(self, obj):
        request = self.context.get('request')
        try:
            avatar_url = obj.user.profile_picture.url
        except Exception:
            return ''
        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url

    def get_curtido_por_mim(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False