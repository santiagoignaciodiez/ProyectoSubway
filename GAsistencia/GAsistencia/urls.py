from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from myapp import views

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    
    path('admin/', admin.site.urls),
    
    path('login/', views.vista_login, name='login'),
    path('menuGerente/', views.vista_menu_gerente, name='menu_gerente'),
    path('asistencia/', views.vista_asistencia, name='asistencia'),
    path('listaEmpleados/', views.vista_lista_empleados, name='lista_empleados'),
    path('agregarEmpleado/', views.vista_agregar_empleado, name='agregar_empleado'),
    
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/empleados/crear/', views.api_crear_empleado, name='api_crear_empleado'),
]
