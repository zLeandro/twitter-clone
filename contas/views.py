from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from postagens.models import Postagem
from postagens.serializers import PostagemSerializer
from .models import Seguidor
from .serializers import SeguirSerializer, UserProfileSerializer, UsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()


class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({"id": usuario.id, "username": usuario.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class SeguirUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            segue_usuario = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'erro': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == segue_usuario:
            return Response({'erro': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        if Seguidor.objects.filter(usuario=request.user, seguido=segue_usuario).exists():
            return Response({'erro': 'Você já segue este usuário.'}, status=status.HTTP_400_BAD_REQUEST)

        seguidor = Seguidor.objects.create(usuario=request.user, seguido=segue_usuario)
        return Response(SeguirSerializer(seguidor).data, status=status.HTTP_201_CREATED)


class DesseguirUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            usuario_para_parar_de_seguir = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"erro": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if usuario_para_parar_de_seguir == request.user:
            return Response({"erro": "Você não pode deixar de seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        relacao = Seguidor.objects.filter(usuario=request.user, seguido=usuario_para_parar_de_seguir).first()
        if relacao:
            relacao.delete()
            return Response({"mensagem": "Você deixou de seguir este usuário."})
        else:
            return Response({"erro": "Você não segue este usuário."}, status=status.HTTP_400_BAD_REQUEST)


class FeedPersonalizadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios_seguidos = Seguidor.objects.filter(usuario=request.user).values_list('seguido', flat=True)
        postagens = Postagem.objects.filter(user__in=usuarios_seguidos).order_by('-data_criacao')
        serializer = PostagemSerializer(postagens, many=True)
        return Response(serializer.data)


class EditarPerfilView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home_view(request):
    return HttpResponse("Bem-vindo à página inicial!")


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})
        data = serializer.data
        data.update({
            'stats': {
                'seguidores': user.seguidores.count(),
                'seguindo': user.seguindo.count(),
                'postagens': user.postagens.count(),
            },
            'is_me': True,
            'is_following': False
        })
        return Response(data)

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserProfileSerializer(user, context={'request': request})
            data = serializer.data
            data.update({
                'id': user.id,
                'stats': {
                    'seguidores': user.seguidores.count(),
                    'seguindo': user.seguindo.count(),
                    'postagens': user.postagens.count(),
                },
                'is_me': request.user == user,
                'is_following': Seguidor.objects.filter(
                    usuario=request.user,
                    seguido=user
                ).exists()
            })
            return Response(data)
        except User.DoesNotExist:
            return Response(
                {"detail": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
