# Script para actualizar el cargo de un empleado existente
# Ejecutar con: python manage.py shell < scripts/actualizar_cargo_empleado.py

from myapp.models import Employee

# ID del empleado a actualizar
EMPLOYEE_ID = '250002'  # Penayo Ariel Enrique
NUEVO_CARGO = 'Principiante'  # Puede ser: Principiante, A, o B

try:
    empleado = Employee.objects.get(employee_id=EMPLOYEE_ID)
    empleado.position = NUEVO_CARGO
    empleado.save()
    print(f"✓ Cargo actualizado exitosamente")
    print(f"  Empleado: {empleado.nombre} {empleado.apellido}")
    print(f"  ID: {empleado.employee_id}")
    print(f"  Nuevo cargo: {empleado.position}")
except Employee.DoesNotExist:
    print(f"✗ Empleado con ID '{EMPLOYEE_ID}' no encontrado")
except Exception as e:
    print(f"✗ Error al actualizar el cargo: {str(e)}")
