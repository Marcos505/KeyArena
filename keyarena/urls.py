from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

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

    path('validacao_otp/', views.validacao_otp, name='validacao_otp')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)