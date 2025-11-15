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
    path('recuperar-contrasena/', views.vista_recuperar_contrasena, name='recuperar_contrasena'),
    path('configuracion-inicial/', views.vista_configuracion_inicial, name='configuracion_inicial'),
    
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/empleados/crear/', views.api_crear_empleado, name='api_crear_empleado'),
    path('api/recuperar-contrasena/', views.api_recuperar_contrasena, name='api_recuperar_contrasena'),
    path('api/configuracion-inicial/', views.api_configuracion_inicial, name='api_configuracion_inicial'),
    path('api/empleado/<str:employee_id>/', views.api_obtener_empleado, name='api_obtener_empleado'),
]
