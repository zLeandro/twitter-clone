from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Seguidor

User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SeguirSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    seguido = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Seguidor
        fields = ['id', 'usuario', 'seguido']

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'bio', 'profile_picture', 'password']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture:
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return settings.MEDIA_URL + obj.profile_picture.name
        return None

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance