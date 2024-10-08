from django.contrib import admin
from django.urls import path, include
from keyarena import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('criar/', views.modalidade_dinamica, name='modalidade_dinamica'),
    path('page_home/', views.home_page, name='home_page'),
    path('', include('keyarena.urls')),
    
    # URL para a primeira etapa do cadastro (informações básicas do torneio)
    path('criar/etapa1/', views.salvar_torneio1, name='salvar_torneio1'),

    # URL para a segunda etapa do cadastro (datas do torneio e inscrição)
    path('criar/etapa2/', views.salvar_torneio2, name='salvar_torneio2'),

]
