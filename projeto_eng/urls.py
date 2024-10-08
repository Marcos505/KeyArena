from django.contrib import admin
from django.urls import path, include
from keyarena import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('criar/', views.modalidade_dinamica, name='modalidade_dinamica'),
    path('', include('keyarena.urls'))
]
