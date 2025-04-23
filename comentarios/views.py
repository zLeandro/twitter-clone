from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Comentario
from .serializers import ComentarioSerializer
from postagens.models import Postagem


class CriarComentarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, postagem_id):
        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except Postagem.DoesNotExist:
            return Response({'erro': 'Postagem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, postagem=postagem)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarComentariosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, postagem_id):
        comentarios = Comentario.objects.filter(postagem_id=postagem_id).order_by('-data_criacao')
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)


class DeletarComentarioView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comentario_id):
        try:
            comentario = Comentario.objects.get(id=comentario_id)
        except Comentario.DoesNotExist:
            return Response({"erro": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar se o usuário é o dono do comentário ou um superusuário
        if comentario.user != request.user:
            return Response({"erro": "Você não pode deletar um comentário que não é seu."}, status=status.HTTP_403_FORBIDDEN)

        comentario.delete()
        return Response({"mensagem": "Comentário deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
