"""
Script para crear el usuario gerente con credenciales específicas
Ejecutar con: python manage.py shell < scripts/create_manager.py
"""

from myapp.models import Employee

# Crear o actualizar el usuario gerente
try:
    gerente = Employee.objects.get(username="Gerente")
    gerente.set_password("hola1234")
    gerente.is_manager = True
    gerente.is_active_employee = True
    gerente.save()
    print("✓ Gerente actualizado exitosamente")
except Employee.DoesNotExist:
    gerente = Employee.objects.create_user(
        username="Gerente",
        employee_id="Gerente",
        password="hola1234",
        first_name="Gerente",
        last_name="Subway",
        is_manager=True,
        is_active_employee=True,
        position="Gerente General",
        email="gerente@subway.com"
    )
    print("✓ Gerente creado exitosamente")

print(f"Usuario: Gerente")
print(f"Contraseña: hola1234")
print(f"Es gerente: {gerente.is_manager}")
