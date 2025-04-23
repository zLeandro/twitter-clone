from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contas/', include('contas.urls')),
    path('api/postagens/', include('postagens.urls')),
    path('api/token/', views.obtain_auth_token),
    path('api/comentarios/', include('comentarios.urls')),

]
