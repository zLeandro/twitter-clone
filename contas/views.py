from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from postagens.models import Postagem
from postagens.serializers import PostagemSerializer
from .models import Seguidor
from .serializers import SeguirSerializer, UserProfileSerializer
from .serializers import UsuarioSerializer

User = get_user_model()

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({"id": usuario.id, "username": usuario.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeguirUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Seguir outro usuário.
        """
        try:
            segue_usuario = get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return Response({'erro': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == segue_usuario:
            return Response({'erro': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        if Seguidor.objects.filter(usuario=request.user, segue=segue_usuario).exists():
            return Response({'erro': 'Você já segue este usuário.'}, status=status.HTTP_400_BAD_REQUEST)

        # Criar o relacionamento de seguir
        seguidor = Seguidor.objects.create(usuario=request.user, segue=segue_usuario)
        return Response(SeguirSerializer(seguidor).data, status=status.HTTP_201_CREATED)

class DesseguirUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Desseguir outro usuário.
        """
        try:
            segue_usuario = get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return Response({'erro': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        relacionamento = Seguidor.objects.filter(usuario=request.user, segue=segue_usuario).first()

        if not relacionamento:
            return Response({'erro': 'Você não segue este usuário.'}, status=status.HTTP_400_BAD_REQUEST)

        relacionamento.delete()
        return Response({'mensagem': 'Usuário desseguido com sucesso!'}, status=status.HTTP_204_NO_CONTENT)


class FeedPersonalizadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios_seguidos = Seguidor.objects.filter(usuario=request.user).values_list('segue', flat=True)

        postagens = Postagem.objects.filter(user__in=usuarios_seguidos).order_by('-data_criacao')

        serializer = PostagemSerializer(postagens, many=True)

        return Response(serializer.data)

class DesseguirUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            usuario_para_parar_de_seguir = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"erro": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if usuario_para_parar_de_seguir == request.user:
            return Response({"erro": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        relacao = Seguidor.objects.filter(usuario=request.user, segue=usuario_para_parar_de_seguir).first()
        if relacao:
            relacao.delete()
            return Response({"mensagem": "Você deixou de seguir este usuário."})
        else:
            return Response({"erro": "Você não segue este usuário."}, status=status.HTTP_400_BAD_REQUEST)


class EditarPerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def home_view(request):
    return HttpResponse("Bem-vindo à página inicial!")