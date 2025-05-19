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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class SeguirSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    segue = serializers.StringRelatedField()

    class Meta:
        model = Seguidor
        fields = ['id', 'usuario', 'segue', 'data_criacao']

    def create(self, validated_data):
        validated_data.pop('data_criacao', None)
        return Seguidor.objects.create(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'profile_picture']