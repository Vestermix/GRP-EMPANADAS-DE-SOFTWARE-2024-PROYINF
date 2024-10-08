from django.urls import path
from . import views

#almacena las direcciones asociadas a la app visorDicom para facilitar su importación

urlpatterns = [

    path('', views.menuPrincipal, name='menu'),
    path('formulario/', views.formulario, name='formulario'),
    path('login/', views.login, name='login'),
    path('cabecera/', views.cabecera, name='cabecera'),
]