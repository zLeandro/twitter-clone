from rest_framework import serializers
from .models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'conteudo', 'data_criacao', 'username', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        try:
            avatar_url = obj.user.profile_picture.url
        except Exception:
            return ''
        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url