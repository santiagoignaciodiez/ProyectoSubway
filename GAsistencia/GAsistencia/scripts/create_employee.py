"""
Script para crear un usuario empleado de prueba
Ejecutar con: python manage.py shell < scripts/create_employee.py
"""

from myapp.models import Employee
from datetime import date

# Crear o actualizar el usuario empleado
try:
    empleado = Employee.objects.get(employee_id="Empleado")
    empleado.set_password("arielozuna")
    empleado.is_manager = False
    empleado.is_active = True
    empleado.save()
    print("✓ Empleado actualizado exitosamente")
except Employee.DoesNotExist:
    empleado = Employee(
        employee_id="Empleado",
        nombre="Ariel",
        apellido="Ozuna",
        dni="12345678",
        cuil="20-12345678-9",
        email="ariel.ozuna@subway.com",
        genero="M",
        edad=25,
        fecha_nacimiento=date(1999, 1, 1),
        estado_civil="soltero",
        tiene_hijos=False,
        nombre_domicilio="Calle Principal 123",
        numero_casa="123",
        numero_emergencia="1234567890",
        position="Empleado",
        is_manager=False,
        is_active=True
    )
    empleado.set_password("arielozuna")
    empleado.save()
    print("✓ Empleado creado exitosamente")

print(f"\n{'='*50}")
print(f"ID de Empleado: {empleado.employee_id}")
print(f"Nombre: {empleado.nombre} {empleado.apellido}")
print(f"Contraseña: arielozuna")
print(f"Es gerente: {empleado.is_manager}")
print(f"Email: {empleado.email}")
print(f"{'='*50}\n")
