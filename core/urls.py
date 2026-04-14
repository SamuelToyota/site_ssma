from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('formacao/', views.formacao, name='formacao'),
    path('videos/', views.videos, name='videos'),
    path('contato/', views.contato, name='contato'),
    path('sucesso/', views.sucesso, name='sucesso'),
]