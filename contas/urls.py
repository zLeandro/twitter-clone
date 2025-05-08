from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroUsuarioView,
    SeguirUsuarioView,
    DesseguirUsuarioView,
    FeedPersonalizadoView,
    EditarPerfilView,
    UsuarioViewSet
)

# CRIAÇÃO DO ROUTER
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

# URLPATTERNS
urlpatterns = [
    path('', include(router.urls)),  # inclui as rotas do ViewSet
    path('registrar/', RegistroUsuarioView.as_view(), name='registrar'),
    path('seguir/<int:pk>/', SeguirUsuarioView.as_view(), name='seguir_usuario'),
    path('desseguir/<int:pk>/', DesseguirUsuarioView.as_view(), name='desseguir_usuario'),
    path('feed/', FeedPersonalizadoView.as_view(), name='feed_personalizado'),
    path('perfil/', EditarPerfilView.as_view(), name='editar_perfil'),
]