from django.urls import path
from .views import CriarComentarioView, ListarComentariosView, DeletarComentarioView

urlpatterns = [
    path('<int:postagem_id>/comentar/', CriarComentarioView.as_view(), name='criar_comentario'),
    path('<int:postagem_id>/comentarios/', ListarComentariosView.as_view(), name='listar_comentarios'),
    path('comentarios/<int:comentario_id>/deletar/', DeletarComentarioView.as_view(), name='deletar_comentario'),
]