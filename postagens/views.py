from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Postagem, Like
from .serializers import PostagemSerializer
from rest_framework.permissions import IsAuthenticated

class CriarPostagemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostagemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarPostagensView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        postagens = Postagem.objects.all().order_by('-data_criacao')
        serializer = PostagemSerializer(postagens, many=True)
        return Response(serializer.data)

class CurtirPostagemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, postagem_id):
        try:
            postagem = Postagem.objects.get(id=postagem_id)
        except Postagem.DoesNotExist:
            return Response({"erro": "Postagem não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, postagem=postagem)

        if not created:
            return Response({"mensagem": "Você já curtiu essa postagem."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"mensagem": "Postagem curtida com sucesso!"}, status=status.HTTP_201_CREATED)

class DescurtirPostagemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, postagem_id):
        try:
            postagem = Postagem.objects.get(id=postagem_id)
        except Postagem.DoesNotExist:
            return Response({'erro': 'Postagem não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(postagem=postagem, user=request.user)
            like.delete()
            return Response({'mensagem': 'Postagem descurtida com sucesso!'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'erro': 'Você ainda não curtiu esta postagem.'}, status=status.HTTP_400_BAD_REQUEST)