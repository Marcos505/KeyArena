from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import page_not_found_view  
urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home_page/', views.home_page, name='home_page'),
    path('torneios/', views.entrartorneio, name='torneios'),
    
    path('perfil/', views.perfil, name='perfil'),

    path('participar/', views.participar, name='participar'),
    path('criar/', views.salvar_torneio1, name='salvar_torneio1'),
    path('criar/etapa2/', views.salvar_torneio2, name='salvar_torneio2'),

    path('sair/', views.sair, name='sair'),
    path('inscricao/<int:torneio_id>/', views.inscricao, name='inscricao'),
    path('cancelar_inscricao/<int:torneio_id>/', views.cancelar_inscricao, name='cancelar_inscricao'),
    path('qrcode_login/', views.qrcode_login, name='qrcode_login'),
    path('qrcode_auth/', views.qrcode_auth, name='qrcode_auth'),
    path('esqueci_senha/', views.esqueci_senha, name='esqueci_senha'),
    path('mudar_senha/', views.mudar_senha, name='mudar_senha'),
    path('troca_senha/', views.troca_senha, name='troca_senha'),
    path('validacao_otp/', views.validacao_otp, name='validacao_otp')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view 