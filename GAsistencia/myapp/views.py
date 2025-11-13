from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth import login, logout
from .models import Employee
import json

def vista_login(request):
    return render(request, 'login.html')

def vista_menu_gerente(request):
    return render(request, 'menuGerente.html')

def vista_lista_empleados(request):
    empleados = Employee.objects.all().exclude(employee_id='Gerente')
    return render(request, 'listaEmpleados.html', {'empleados': empleados})

def vista_agregar_empleado(request):
    return render(request, 'agregarEmpleado.html')

def vista_asistencia(request):
    return render(request, 'asistencia.html')

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employee_id = data.get('employee_id') or data.get('id_empleado', '').strip()
            password = data.get('password') or data.get('contrasena', '').strip()
            
            print(f"[DEBUG] Login attempt - employee_id: '{employee_id}', password length: {len(password)}")
            
            if employee_id.upper() == 'GERENTE' and password == 'hola1234':
                print("[DEBUG] Credenciales de gerente detectadas")
                
                # Crear o actualizar el usuario gerente
                try:
                    gerente = Employee.objects.get(employee_id='Gerente')
                    print("[DEBUG] Gerente encontrado en BD")
                except Employee.DoesNotExist:
                    print("[DEBUG] Creando usuario gerente...")
                    gerente = Employee(
                        employee_id='Gerente',
                        nombre='Gerente',
                        apellido='Sistema',
                        dni='00000000',
                        cuil='00-00000000-0',
                        position='Gerente',
                        is_manager=True,
                        is_active=True,
                        genero='M',
                        edad=30,
                        fecha_nacimiento='2000-01-01',
                        estado_civil='soltero',
                        tiene_hijos=False,
                        nombre_domicilio='Sistema',
                        numero_emergencia='0000000000'
                    )
                    gerente.set_password('hola1234')
                    gerente.is_staff = True
                    gerente.is_superuser = True
                    gerente.save()
                    print("[DEBUG] Gerente creado exitosamente")
                
                # Asegurar que siempre tenga los permisos correctos
                gerente.is_manager = True
                gerente.is_staff = True
                gerente.is_superuser = True
                gerente.save()
                
                print("[DEBUG] Login exitoso para gerente")
                
                return JsonResponse({
                    'exito': True,
                    'mensaje': 'Inicio de sesión exitoso',
                    'empleado': {
                        'employee_id': gerente.employee_id,
                        'nombre': gerente.nombre,
                        'apellido': gerente.apellido,
                        'es_gerente': True
                    }
                })
            
            # Verificar empleado normal
            print(f"[DEBUG] Buscando empleado normal con ID: {employee_id}")
            try:
                empleado = Employee.objects.get(employee_id=employee_id)
                print(f"[DEBUG] Empleado encontrado: {empleado.nombre}")
                
                if empleado.check_password(password):
                    print("[DEBUG] Contraseña correcta")
                    return JsonResponse({
                        'exito': True,
                        'mensaje': 'Inicio de sesión exitoso',
                        'empleado': {
                            'employee_id': empleado.employee_id,
                            'nombre': empleado.nombre,
                            'apellido': empleado.apellido,
                            'es_gerente': empleado.is_manager
                        }
                    })
                else:
                    print("[DEBUG] Contraseña incorrecta")
                    return JsonResponse({
                        'exito': False,
                        'mensaje': 'Contraseña incorrecta'
                    }, status=401)
            except Employee.DoesNotExist:
                print(f"[DEBUG] Empleado con ID '{employee_id}' no encontrado en BD")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Empleado no encontrado'
                }, status=404)
                
        except Exception as e:
            print(f"[DEBUG] ERROR en api_login: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'exito': True, 'mensaje': 'Sesión cerrada'})
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_crear_empleado(request):
    if request.method == 'POST':
        try:
            # El employee_id se generará automáticamente en el modelo
            empleado = Employee.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                dni=request.POST.get('dni'),
                cuil=request.POST.get('cuil'),
                genero=request.POST.get('genero'),
                edad=int(request.POST.get('edad')),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                estado_civil=request.POST.get('estado_civil'),
                tiene_hijos=request.POST.get('tiene_hijos') == 'true',
                nombre_domicilio=request.POST.get('nombre_domicilio'),
                numero_casa=request.POST.get('numero_casa', ''),
                piso_departamento=request.POST.get('piso_departamento', ''),
                numero_departamento=request.POST.get('numero_departamento', ''),
                numero_emergencia=request.POST.get('numero_emergencia'),
                position='Empleado',
                is_active=True
            )
            
            # Manejar foto de perfil si existe
            if request.FILES.get('foto_perfil'):
                empleado.foto_perfil = request.FILES['foto_perfil']
                empleado.save()
            
            # Establecer contraseña por defecto (se puede cambiar después)
            empleado.set_password('subway2025')
            empleado.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': 'Empleado creado exitosamente',
                'employee_id': empleado.employee_id
            })
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': str(e)
            }, status=400)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)
