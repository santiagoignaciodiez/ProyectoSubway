# Script para asignar contraseña a un empleado específico
# Ejecutar con: python manage.py shell < scripts/asignar_contrasena_empleado.py

from myapp.models import Employee

# CONFIGURACIÓN: Cambiar estos valores
EMPLOYEE_ID = '250001'  # ID del empleado (ej: 250001, 250002, etc.)
NUEVA_CONTRASENA = 'arielozuna'  # Contraseña a asignar

try:
    empleado = Employee.objects.get(employee_id=EMPLOYEE_ID)
    empleado.set_password(NUEVA_CONTRASENA)
    empleado.save()
    print(f"✓ Contraseña asignada exitosamente al empleado {EMPLOYEE_ID}")
    print(f"  Nombre: {empleado.nombre} {empleado.apellido}")
    print(f"  DNI: {empleado.dni}")
    print(f"  Cargo: {empleado.position}")
except Employee.DoesNotExist:
    print(f"✗ Empleado con ID '{EMPLOYEE_ID}' no encontrado")
except Exception as e:
    print(f"✗ Error al asignar contraseña: {str(e)}")
