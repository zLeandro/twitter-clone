from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroUsuarioView,
    SeguirUsuarioView,
    DesseguirUsuarioView,
    FeedPersonalizadoView,
    EditarPerfilView,
    UsuarioViewSet,
    CustomTokenObtainPairView,
    TokenRefreshView,
    PerfilView,
    PerfilUsuarioView,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('registrar/', RegistroUsuarioView.as_view(), name='registrar'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('seguir/<int:pk>/', SeguirUsuarioView.as_view(), name='seguir_usuario'),
    path('desseguir/<int:pk>/', DesseguirUsuarioView.as_view(), name='desseguir_usuario'),
    path('feed/', FeedPersonalizadoView.as_view(), name='feed_personalizado'),
    path('perfil/editar/', EditarPerfilView.as_view(), name='editar_perfil'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/<str:username>/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
]