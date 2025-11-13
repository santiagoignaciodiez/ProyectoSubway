from django.contrib import admin
from .models import Employee, AttendanceRecord

@admin.register(Employee)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'nombre', 'apellido', 'dni', 'position', 'is_manager', 'is_active']
    list_filter = ['is_manager', 'is_active', 'genero', 'estado_civil']
    search_fields = ['employee_id', 'nombre', 'apellido', 'dni', 'cuil']
    ordering = ['employee_id']
    
    fieldsets = (
        ('Información de Empleado', {
            'fields': ('employee_id', 'password')
        }),
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'dni', 'cuil', 'foto_perfil', 'genero', 'edad', 'fecha_nacimiento', 'estado_civil', 'tiene_hijos')
        }),
        ('Información de Domicilio', {
            'fields': ('nombre_domicilio', 'numero_departamento', 'piso_departamento', 'numero_casa', 'telefono_emergencia')
        }),
        ('Información Laboral', {
            'fields': ('position', 'is_manager')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

@admin.register(AttendanceRecord)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ['employee', 'check_in', 'check_out']
    list_filter = ['check_in', 'check_out']
    search_fields = ['employee__employee_id', 'employee__nombre', 'employee__apellido']
    ordering = ['-check_in']
