from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.page_apresentation, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('auth/home_page/', views.home_page, name='home_page')
]
