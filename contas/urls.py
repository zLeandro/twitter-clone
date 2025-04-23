from django.urls import path
from .views import RegistroUsuarioView, SeguirUsuarioView, DesseguirUsuarioView, FeedPersonalizadoView, EditarPerfilView

urlpatterns = [
    path('registrar/', RegistroUsuarioView.as_view(), name='registrar'),
    path('seguir/<int:pk>/', SeguirUsuarioView.as_view(), name='seguir_usuario'),
    path('desseguir/<int:pk>/', DesseguirUsuarioView.as_view(), name='desseguir_usuario'),
    path('feed/', FeedPersonalizadoView.as_view(), name='feed_personalizado'),
    path('perfil/', EditarPerfilView.as_view(), name='editar_perfil'),
]