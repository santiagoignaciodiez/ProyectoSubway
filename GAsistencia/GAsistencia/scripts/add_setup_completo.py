# Script para agregar el campo setup_completo a la tabla de empleados
# Ejecutar con: python manage.py shell < scripts/add_setup_completo.py

from myapp.models import Employee

# Actualizar el usuario Gerente para que requiera configuración inicial
try:
    gerente = Employee.objects.get(employee_id='Gerente')
    gerente.setup_completo = False
    gerente.save()
    print(f"✓ Usuario Gerente actualizado: setup_completo = {gerente.setup_completo}")
except Employee.DoesNotExist:
    print("✗ Usuario Gerente no encontrado")

# Verificar otros empleados
empleados = Employee.objects.all()
print(f"\nTotal empleados: {empleados.count()}")
for emp in empleados:
    print(f"- {emp.employee_id}: setup_completo = {emp.setup_completo}")
