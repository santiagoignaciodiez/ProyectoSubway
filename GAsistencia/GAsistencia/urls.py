from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from myapp import views
from django.urls import path
from myapp.views import api_asistencia_hoy, api_asistencia_rango, api_sync_zkteco

urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),

    path('admin/', admin.site.urls),

    # LOGIN
    path('login/', views.vista_login, name='login'),

    # MENÚS
    path('menuGerente/', views.vista_menu_gerente, name='menu_gerente'),
    path('menuEmpleado/', views.vista_menu_empleado, name='menu_empleado'),

    # GERENTE
    path('asistenciaGerente/', views.vista_asistencia, name='asistencia_gerente'),
    path('justificacionesGerente/', views.vista_justificaciones_gerente, name='justificaciones_gerente'),
    path('listaEmpleados/', views.vista_lista_empleados, name='lista_empleados'),
    path('agregarEmpleado/', views.vista_agregar_empleado, name='agregar_empleado'),
    path('editarEmpleado/<str:employee_id>/', views.vista_editar_empleado, name='editar_empleado'),
    path('sanciones/', views.sanciones, name='sanciones'),
    
    #path('sanciones/<str:employee_id>/', views.sanciones, name='sanciones'),
    #path('sanciones/<str:employee_id>/guardar/', views.guardar_sancion, name='guardar_sancion'),
    #path('amonestaciones/<str:employee_id>/guardar/', views.guardar_amonestacion, name='guardar_amonestacion'),


    # EMPLEADO
    path('datosasistenciaE/', views.asistencia_e, name='datosasistenciaE'),
    
    # Alias para evitar errores desde HTML antiguos
    path('asistenciaE/', views.asistencia_e, name='asistenciaE'),
    
    path('datosempleadosE/', views.datos_e, name='datosE'),
    path('justificacionesE/', views.justificacionesE, name='justificacionesE'),
    path('cronogramaE/', views.cronograma_e, name='cronogramaE'),

    # GENERAL
    path('recuperar-contrasena/', views.vista_recuperar_contrasena, name='recuperar_contrasena'),
    path('configuracion-inicial/', views.vista_configuracion_inicial, name='configuracion_inicial'),
    path('cronograma/', views.cronograma, name='cronograma'),

    # APIs
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/empleados/crear/', views.api_crear_empleado, name='api_crear_empleado'),
    path('api/empleados/<str:employee_id>/editar/', views.api_editar_empleado, name='api_editar_empleado'),
    path('api/recuperar-contrasena/', views.api_recuperar_contrasena, name='api_recuperar_contrasena'),
    path('api/configuracion-inicial/', views.api_configuracion_inicial, name='api_configuracion_inicial'),
    path('api/empleado/<str:employee_id>/', views.api_obtener_empleado, name='api_obtener_empleado'),
    path('api/empleados/<str:employee_id>/desactivar/', views.api_desactivar_empleado, name='api_desactivar_empleado'),
    path('api/empleados/<str:employee_id>/reactivar/', views.api_reactivar_empleado, name='api_reactivar_empleado'),
    path('verEmpleado/<str:employee_id>/', views.vista_ver_empleado, name='ver_empleado'),

    path('api/asistencia-hoy/', api_asistencia_hoy, name='api_asistencia_hoy'),
    path('api/asistencia-rango/', api_asistencia_rango, name='api_asistencia_rango'),
    path('api/sync_zkteco/', api_sync_zkteco, name='api_sync_zkteco'),
]

