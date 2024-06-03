from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('salir', LogoutView.as_view(), name = 'logout'),
    path('entrar', views.LoginView.as_view(), name = 'login'),
    path('registrar', views.RegistrarView.as_view(), name = 'registrar'),
    path('perfil', views.CrearPerfilView.as_view(), name = 'perfil'),
    path('activar/<slug:uidb64>/<slug:token> ', views.ActivarCuentaView.as_view(), name = 'activar '),
    path('grupos/', views.asignar_grupos, name='asignar_grupos'),
    path('lista_usuarios/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),

    
]

    # urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
