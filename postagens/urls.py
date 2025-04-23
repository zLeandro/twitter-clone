from django.urls import path
from .views import CriarPostagemView, ListarPostagensView, CurtirPostagemView, DescurtirPostagemView

urlpatterns = [
    path('criar/', CriarPostagemView.as_view(), name='criar_postagem'),
    path('listar/', ListarPostagensView.as_view(), name='listar_postagens'),
    path('<int:postagem_id>/curtir/', CurtirPostagemView.as_view(), name='curtir_postagem'),
    path('<int:postagem_id>/descurtir/', DescurtirPostagemView.as_view(), name='descurtir_postagem'),
]