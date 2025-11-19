from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import Employee, Asistencia, Amonestacion
import json
from myapp.utils import process_employee_photo, optimize_employee_photo, obtener_dispositivo
from zk import ZK, const
from datetime import datetime, date
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
import traceback
from django.http import JsonResponse
from myapp.models import Asistencia, Employee
from django.utils.timezone import localdate


def asistencia(request):
    return render(request, 'datosasistencia.html')

def sanciones(request):
    return render(request, 'sanciones.html')

def asistencia_e(request):
    return render(request, 'datosasistenciaE.html')
                  
def justificacionesE(request):
    return render(request, 'justificacionesEmpleado.html')

def datos_e(request):
    return render(request, 'datosempleadosE.html')
                  
def cronograma_e(request):
    return render(request, 'cronogramaEmpleado.html')

def cronograma(request):
    hoy = date.today()  # fecha real del sistema
    return render(request, 'cronograma.html', {
        'hoy': hoy
    })



def asistencia_e(request):
    """Vista de asistencia para empleados"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        hoy = date.today()
        
        # Obtener asistencias del empleado
        asistencias = Asistencia.objects.filter(
            empleado=empleado,
            timestamp__date=hoy
        ).order_by('timestamp')
        
        context = {
            'empleado': empleado,
            'asistencias': asistencias,
            'fecha': hoy
        }
        return render(request, 'myapp/asistenciaEmpleado.html', context)
    except Employee.DoesNotExist:
        return redirect('login')

def datos_e(request):
    """Vista de datos personales del empleado"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        
        # Obtener asistencia del día
        hoy = date.today()
        entrada = Asistencia.objects.filter(
            empleado=empleado,
            timestamp__date=hoy,
            tipo='entrada'
        ).first()
        
        salida = Asistencia.objects.filter(
            empleado=empleado,
            timestamp__date=hoy,
            tipo='salida'
        ).first()
        
        context = {
            'empleado': empleado,
            'entrada': entrada,
            'salida': salida
        }
        return render(request, 'myapp/datosAsistenciaEmpleado.html', context)
    except Employee.DoesNotExist:
        return redirect('login')

def justificacionesE(request):
    """Vista de justificaciones del empleado"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        # TODO: Implementar modelo de Justificaciones
        context = {
            'empleado': empleado,
            'justificaciones': []  # Agregar cuando se implemente el modelo
        }
        return render(request, 'myapp/justificacionesEmpleado.html', context)
    except Employee.DoesNotExist:
        return redirect('login')

def cronograma(request):
    """Vista de cronograma para gerente"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        if not empleado.is_manager:
            return redirect('login')
        
        # TODO: Implementar modelo de Cronograma
        context = {
            'empleado': empleado,
            'hoy': date.today()
        }
        return render(request, 'myapp/cronograma.html', context)
    except Employee.DoesNotExist:
        return redirect('login')

def cronograma_e(request):
    """Vista de cronograma para empleado"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        # TODO: Implementar modelo de Cronograma
        context = {
            'empleado': empleado,
            'hoy': date.today()
        }
        return render(request, 'myapp/cronogramaEmpleado.html', context)
    except Employee.DoesNotExist:
        return redirect('login')

def vista_menu_empleado(request):
    """Vista del menú principal para empleados"""
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        return render(request, 'myapp/menuEmpleado.html', {'empleado': empleado})
    except Employee.DoesNotExist:
        return redirect('login')
    
def guardar_amonestacion(request, employee_id):
    if request.method == "POST":
        empleado = Employee.objects.get(employee_id=employee_id)

        Amonestacion.objects.create(
            empleado=empleado,
            motivo=request.POST.get("motivo"),
            fecha_inicio=request.POST.get("fecha_inicio"),
            fecha_fin=request.POST.get("fecha_fin"),
            observacion=request.POST.get("observacion")
        )

        return redirect("sanciones", employee_id=employee_id)
    


def vista_login(request):
    """Login unificado para empleados y gerente con formulario normal (sin JS)."""
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        password = request.POST.get('password', '').strip()

        if not employee_id or not password:
            messages.error(request, 'Debe completar todos los campos')
            return render(request, 'myapp/login.html')

        # LOGIN GERENTE ESPECIAL
        if employee_id.upper() == 'GERENTE' and password == 'hola1234':
            gerente, created = Employee.objects.get_or_create(
                employee_id='Gerente',
                defaults={
                    'nombre': 'Gerente',
                    'apellido': 'Sistema',
                    'dni': '00000000',
                    'cuil': '00-00000000-0',
                    'position': 'Gerente',
                    'is_manager': True,
                    'is_active': True,
                    'genero': 'M',
                    'edad': 30,
                    'fecha_nacimiento': '2000-01-01',
                    'estado_civil': 'soltero',
                    'tiene_hijos': False,
                    'nombre_domicilio': 'Sistema',
                    'numero_emergencia': '0000000000',
                    'setup_completo': False
                }
            )

            # Elevar permisos del gerente
            gerente.is_manager = True
            gerente.is_staff = True
            gerente.is_superuser = True
            gerente.save()

            request.session['employee_id'] = gerente.employee_id
            return redirect('menu_gerente')

        # LOGIN EMPLEADO NORMAL
        try:
            empleado = Employee.objects.get(employee_id__iexact=employee_id)
        except Employee.DoesNotExist:
            messages.error(request, 'Empleado no encontrado')
            return render(request, 'myapp/login.html')

        if not empleado.check_password(password):
            messages.error(request, 'Contraseña incorrecta')
            return render(request, 'myapp/login.html')

        # Guardar sesión
        request.session['employee_id'] = empleado.employee_id

        # Redirección por tipo de usuario
        if empleado.is_manager:
            return redirect('menu_gerente')
        else:
            return redirect('menu_empleado')

    return render(request, 'myapp/login.html')

def vista_menu_gerente(request):
    # Verificar que hay un usuario en sesión
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('login')
    
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        if not empleado.is_manager:
            return redirect('login')
        
        return render(request, 'myapp/menuGerente.html', {'empleado': empleado})
    except Employee.DoesNotExist:
        return redirect('login')

def vista_lista_empleados(request):
    status = request.GET.get('status', 'activo')
    search = request.GET.get('search', '')
    
    if status == 'activo':
        empleados = Employee.objects.filter(is_manager=False, is_active=True)
    else:
        empleados = Employee.objects.filter(is_manager=False, is_active=False)
    
    if search:
        empleados = empleados.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(dni__icontains=search) |
            Q(employee_id__icontains=search)
        )
    
    return render(request, 'myapp/listaEmpleados.html', {
        'empleados': empleados,
        'status': status,
        'search': search
    })

def vista_agregar_empleado(request):
    if request.method == 'POST':
        try:
            empleado = Employee.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                dni=request.POST.get('dni'),
                cuil=request.POST.get('cuil'),
                email=request.POST.get('email', ''),
                genero=request.POST.get('genero'),
                edad=int(request.POST.get('edad')),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                estado_civil=request.POST.get('estado_civil'),
                tiene_hijos=request.POST.get('tiene_hijos') == 'on',
                nombre_domicilio=request.POST.get('nombre_domicilio'),
                numero_casa=request.POST.get('numero_casa', ''),
                piso_departamento=request.POST.get('piso_departamento', ''),
                numero_departamento=request.POST.get('numero_departamento', ''),
                numero_emergencia=request.POST.get('numero_emergencia', ''),
                position=request.POST.get('cargo', 'Principiante'),
                is_active=True
            )
            
            if request.FILES.get('foto_perfil'):
                photo_file = request.FILES['foto_perfil']
                file_path, processed_file = optimize_employee_photo(photo_file, empleado.employee_id)
                
                if file_path and processed_file:
                    empleado.foto_perfil = processed_file
                    empleado.foto_perfil.name = file_path
                    empleado.save()
            
            empleado.set_password('1234')
            empleado.save()
            
            return redirect('/listaEmpleados/')
        except Exception as e:
            return render(request, 'myapp/agregarEmpleado.html', {
                'error': f'Error al crear empleado: {str(e)}'
            })
    
    return render(request, 'myapp/agregarEmpleado.html')

def vista_asistencia(request):
    if request.method == 'POST':
        # Sincronizar asistencias
        try:
            zk_config = settings.ZKTECO
            zk = ZK(zk_config["ip"], port=zk_config["port"], timeout=zk_config["timeout"])
            conn = zk.connect()
            registros = conn.get_attendance()
            
            count = 0
            for r in registros:
                empleado = Employee.objects.filter(dni=str(r.user_id)).first()
                if not empleado:
                    empleado = Employee.objects.filter(employee_id=str(r.user_id)).first()
                
                if empleado:
                    existe = Asistencia.objects.filter(
                        empleado=empleado,
                        timestamp=r.timestamp
                    ).exists()
                    
                    if not existe:
                        tipo_registro = 'entrada' if r.punch in [0, 1] else 'salida'
                        Asistencia.objects.create(
                            empleado=empleado,
                            timestamp=r.timestamp,
                            tipo=tipo_registro
                        )
                        count += 1
            
            conn.disconnect()
            
            from django.contrib import messages
            messages.success(request, f'{count} registros sincronizados')
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error al sincronizar: {str(e)}')
        
        return redirect('vista_asistencia')
    
    # GET - Mostrar asistencia
    tab = request.GET.get('tab', 'diaria')
    status = request.GET.get('status', 'presente')
    hoy = date.today()
    
    # Obtener asistencias del día
    asistencias_hoy = Asistencia.objects.filter(
        timestamp__date=hoy,
        empleado__isnull=False
    ).select_related('empleado').order_by('-timestamp')
    
    # Agrupar por empleado
    empleados_dict = {}
    for asistencia in asistencias_hoy:
        emp = asistencia.empleado
        if emp.employee_id not in empleados_dict:
            empleados_dict[emp.employee_id] = {
                'nombre': emp.nombre,
                'apellido': emp.apellido,
                'dni': emp.dni,
                'cargo': emp.position,
                'entrada': None,
                'salida': None
            }
        
        if asistencia.tipo == 'entrada' and not empleados_dict[emp.employee_id]['entrada']:
            empleados_dict[emp.employee_id]['entrada'] = asistencia.timestamp
        elif asistencia.tipo == 'salida':
            empleados_dict[emp.employee_id]['salida'] = asistencia.timestamp
    
    empleados_asistencia = list(empleados_dict.values())
    
    # Filtrar según status
    if status == 'presente':
        empleados_asistencia = [e for e in empleados_asistencia if e['entrada']]
    elif status == 'ausente':
        empleados_asistencia = [e for e in empleados_asistencia if not e['entrada']]
    
    context = {
        'tab': tab,
        'status': status,
        'empleados_asistencia': empleados_asistencia,
        'tabla_asistencia': list(empleados_dict.values()),
        'fecha': hoy
    }
    
    return render(request, 'myapp/asistenciaGerente.html', context)

def vista_recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor ingresa tu correo electrónico')
            return render(request, 'myapp/recuperarContrasena.html')
        
        empleados = Employee.objects.filter(email=email)
        
        if not empleados.exists():
            messages.error(request, 'Correo electrónico no encontrado en el sistema')
            return render(request, 'myapp/recuperarContrasena.html')

        empleado = empleados.first()  # Si hay más de uno, toma el primero
        
        try:
            send_mail(
                subject=f'Solicitud de recuperación de contraseña - {empleado.nombre} {empleado.apellido}',
                message=f'''
Solicitud de recuperación de contraseña

Datos del empleado:
- ID: {empleado.employee_id}
- Nombre: {empleado.nombre} {empleado.apellido}
- Email: {empleado.email}
- DNI: {empleado.dni}
- Posición: {empleado.position}

El empleado ha solicitado una nueva contraseña.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['santiagoignaciodiez@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, '¡Solicitud enviada exitosamente! El administrador recibirá el correo.')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {e}')

    return render(request, 'myapp/recuperarContrasena.html')

def vista_configuracion_inicial(request):
    return render(request, 'myapp/configuracionInicial.html')

def vista_justificaciones_gerente(request):
    return render(request, 'myapp/justificacionesGerente.html')

def vista_editar_empleado(request, employee_id):
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        
        if request.method == 'POST':
            try:
                empleado.nombre = request.POST.get('nombre')
                empleado.apellido = request.POST.get('apellido')
                empleado.dni = request.POST.get('dni')
                empleado.cuil = request.POST.get('cuil')
                empleado.email = request.POST.get('email', '')
                empleado.genero = request.POST.get('genero')
                empleado.edad = int(request.POST.get('edad'))
                empleado.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                empleado.estado_civil = request.POST.get('estado_civil')
                empleado.tiene_hijos = request.POST.get('tiene_hijos') == 'on'
                empleado.nombre_domicilio = request.POST.get('nombre_domicilio')
                empleado.numero_casa = request.POST.get('numero_casa', '')
                empleado.piso_departamento = request.POST.get('piso_departamento', '')
                empleado.numero_departamento = request.POST.get('numero_departamento', '')
                empleado.numero_emergencia = request.POST.get('numero_emergencia')
                empleado.position = request.POST.get('cargo')
                empleado.is_active = request.POST.get('is_active') == 'on'
                
                if request.FILES.get('foto_perfil'):
                    photo_file = request.FILES['foto_perfil']
                    file_path, processed_file = optimize_employee_photo(photo_file, empleado.employee_id)
                    
                    if file_path and processed_file:
                        empleado.foto_perfil = processed_file
                        empleado.foto_perfil.name = file_path
                
                empleado.save()
                return redirect('/listaEmpleados/')
            except Exception as e:
                return render(request, 'myapp/editarEmpleado.html', {
                    'empleado': empleado,
                    'error': str(e)
                })
        
        return render(request, 'myapp/editarEmpleado.html', {'empleado': empleado})
    except Employee.DoesNotExist:
        return redirect('/listaEmpleados/')

def vista_ver_empleado(request, employee_id):
    try:
        empleado = Employee.objects.get(employee_id=employee_id)
        return render(request, 'myapp/verEmpleado.html', {'empleado': empleado})
    except Employee.DoesNotExist:
        return redirect('/listaEmpleados/')

def vista_logout(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('vista_login')
    return redirect('vista_login')

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employee_id = (data.get('employee_id') or data.get('id_empleado', '')).strip()
            password = (data.get('password') or data.get('contrasena', '')).strip()

            print(f"[DEBUG] employee_id recibido: '{employee_id}'")
            print(f"[DEBUG] password recibido: '{password}'")

            if not employee_id:
                return JsonResponse({'exito': False, 'mensaje': 'ID de empleado vacío'}, status=400)

            # Buscar en la base de datos (sin diferenciar mayúsculas/minúsculas)
            try:
                empleado = Employee.objects.get(employee_id__iexact=employee_id)
                print(f"[DEBUG] Empleado encontrado: {empleado.nombre} {empleado.apellido}")
            except Employee.DoesNotExist:
                print(f"[DEBUG] Empleado NO encontrado en la base de datos")
                return JsonResponse({'exito': False, 'mensaje': 'Empleado no encontrado'}, status=404)

            if empleado.check_password(password):
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
                print(f"[DEBUG] Contraseña incorrecta para empleado {empleado.employee_id}")
                return JsonResponse({'exito': False, 'mensaje': 'Contraseña incorrecta'}, status=401)

        except Exception as e:
            print(f"[ERROR] Error en api_login: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'exito': False, 'mensaje': f'Error del servidor: {str(e)}'}, status=500)

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
            empleado = Employee.objects.create(
                nombre=request.POST.get('nombre'),
                apellido=request.POST.get('apellido'),
                dni=request.POST.get('dni'),
                cuil=request.POST.get('cuil'),
                genero=request.POST.get('genero'),
                edad=int(request.POST.get('edad')),
                email=request.POST.get('email'),
                fecha_nacimiento=request.POST.get('fecha_nacimiento'),
                estado_civil=request.POST.get('estado_civil'),
                tiene_hijos=request.POST.get('tiene_hijos') == 'true',
                nombre_domicilio=request.POST.get('nombre_domicilio'),
                numero_casa=request.POST.get('numero_casa', ''),
                piso_departamento=request.POST.get('piso_departamento', ''),
                numero_departamento=request.POST.get('numero_departamento', ''),
                numero_telefono=request.POST.get('numero_telefono', ''),
                numero_emergencia=request.POST.get('numero_emergencia'),
                position=request.POST.get('cargo', 'Principiante'),
                is_active=True
            )
            
            if request.FILES.get('foto_perfil'):
                photo_file = request.FILES['foto_perfil']
                file_path, processed_file = optimize_employee_photo(photo_file, empleado.employee_id)
                
                if file_path and processed_file:
                    empleado.foto_perfil = processed_file
                    empleado.foto_perfil.name = file_path
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

@csrf_exempt
def api_recuperar_contrasena(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employee_id = data.get('employee_id', '').strip().upper()
            email = data.get('email', '').strip()
            
            if not employee_id or not email:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Por favor completa los campos requeridos'
                }, status=400)
            
            try:
                empleado = Employee.objects.get(email=email)
            except Employee.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Correo electrónico no encontrado en el sistema'
                }, status=404)
            
            if employee_id == 'GERENTE':
                nombre = data.get('nombre', empleado.nombre)
                apellido = data.get('apellido', empleado.apellido)
                dni = data.get('dni', empleado.dni)
                cuil = data.get('cuil', empleado.cuil)
                numero_emergencia = data.get('numero_emergencia', empleado.numero_emergencia)
                
                asunto = f'Solicitud de recuperación de contraseña - GERENTE {nombre} {apellido}'
                mensaje = f'''
Solicitud de recuperación de contraseña - GERENTE

Datos del Gerente:
- ID: {empleado.employee_id}
- Nombre: {nombre}
- Apellido: {apellido}
- Email: {email}
- DNI: {dni}
- CUIL: {cuil}
- Teléfono de Emergencia: {numero_emergencia}
- Posición: {empleado.position}

El gerente ha solicitado una nueva contraseña.
                '''
            else:
                asunto = f'Solicitud de recuperación de contraseña - {empleado.nombre} {empleado.apellido}'
                mensaje = f'''
Solicitud de recuperación de contraseña

Datos del empleado:
- ID: {empleado.employee_id}
- Nombre: {empleado.nombre} {empleado.apellido}
- Email: {empleado.email}
- DNI: {empleado.dni}
- Posición: {empleado.position}

El empleado ha solicitado una nueva contraseña.
                '''
            
            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    ['santiagoignaciodiez@gmail.com'],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'exito': True,
                    'mensaje': 'Solicitud enviada exitosamente.'
                })
            except Exception as e:
                print(f"[ERROR] Error al enviar correo: {str(e)}")
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Error al enviar el correo.'
                }, status=500)
                
        except Exception as e:
            print(f"[ERROR] Error en api_recuperar_contrasena: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_obtener_empleado(request, employee_id):
    if request.method == 'GET':
        try:
            empleado = Employee.objects.get(employee_id=employee_id.upper())
            return JsonResponse({
                'exito': True,
                'empleado': {
                    'employee_id': empleado.employee_id,
                    'nombre': empleado.nombre,
                    'apellido': empleado.apellido,
                    'email': empleado.email,
                    'dni': empleado.dni,
                    'cuil': empleado.cuil,
                    'numero_emergencia': empleado.numero_emergencia,
                    'position': empleado.position
                }
            })
        except Employee.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empleado no encontrado'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'exito': False,
                'mensaje': str(e)
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_configuracion_inicial(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre', '').strip()
            apellido = data.get('apellido', '').strip()
            dni = data.get('dni', '').strip()
            cuil = data.get('cuil', '').strip()
            email = data.get('email', '').strip()
            telefono_emergencia = data.get('telefono_emergencia', '').strip()
            
            if not all([nombre, apellido, dni, cuil, email, telefono_emergencia]):
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Todos los campos son obligatorios'
                }, status=400)
            
            if '@' not in email or '.' not in email:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'El correo electrónico no es válido'
                }, status=400)
            
            try:
                gerente = Employee.objects.get(employee_id='Gerente')
            except Employee.DoesNotExist:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Usuario gerente no encontrado'
                }, status=404)
            
            gerente.nombre = nombre
            gerente.apellido = apellido
            gerente.dni = dni
            gerente.cuil = cuil
            gerente.email = email
            gerente.numero_emergencia = telefono_emergencia
            gerente.setup_completo = True
            gerente.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': 'Configuración completada exitosamente'
            })
            
        except Exception as e:
            print(f"[ERROR] Error en api_configuracion_inicial: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_lista_empleados(request):
    if request.method == 'GET':
        try:
            empleados = Employee.objects.filter(is_manager=False).values(
                'employee_id', 
                'nombre', 
                'apellido', 
                'dni', 
                'position',
                'is_active'
            )
            
            empleados_list = list(empleados)
            
            return JsonResponse({
                'exito': True,
                'empleados': empleados_list
            })
        except Exception as e:
            print(f"[ERROR] Error en api_lista_empleados: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_desactivar_empleado(request, employee_id):
    if request.method == 'POST':
        try:
            empleado = Employee.objects.get(employee_id=employee_id)
            empleado.is_active = False
            empleado.save()
            
            messages.success(request, f'Empleado {empleado.nombre} {empleado.apellido} desactivado exitosamente')
            return redirect('lista_empleados')  # redirige y muestra mensaje
        except Employee.DoesNotExist:
            messages.error(request, 'Empleado no encontrado')
            return redirect('lista_empleados')
        except Exception as e:
            print(f"[ERROR] Error en api_desactivar_empleado: {str(e)}")
            messages.error(request, f'Error del servidor: {str(e)}')
            return redirect('lista_empleados')
    
    messages.error(request, 'Método no permitido')
    return redirect('lista_empleados')

@csrf_exempt
def api_reactivar_empleado(request, employee_id):
    if request.method == 'POST':
        try:
            empleado = Employee.objects.get(employee_id=employee_id)
            empleado.is_active = True
            empleado.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': f'Empleado {empleado.nombre} {empleado.apellido} reactivado exitosamente'
            })
        except Employee.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empleado no encontrado'
            }, status=404)
        except Exception as e:
            print(f"[ERROR] Error en api_reactivar_empleado: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_editar_empleado(request, employee_id):
    if request.method == 'POST':
        try:
            empleado = Employee.objects.get(employee_id=employee_id)
            data = json.loads(request.body)
            
            empleado.nombre = data.get('nombre', empleado.nombre)
            empleado.apellido = data.get('apellido', empleado.apellido)
            empleado.dni = data.get('dni', empleado.dni)
            empleado.cuil = data.get('cuil', empleado.cuil)
            empleado.email = data.get('email', empleado.email)
            empleado.genero = data.get('genero', empleado.genero)
            empleado.edad = int(data.get('edad', empleado.edad))
            empleado.fecha_nacimiento = data.get('fecha_nacimiento', empleado.fecha_nacimiento)
            empleado.estado_civil = data.get('estado_civil', empleado.estado_civil)
            empleado.tiene_hijos = data.get('tiene_hijos', empleado.tiene_hijos)
            empleado.nombre_domicilio = data.get('nombre_domicilio', empleado.nombre_domicilio)
            empleado.numero_casa = data.get('numero_casa', empleado.numero_casa)
            empleado.piso_departamento = data.get('piso_departamento', empleado.piso_departamento)
            empleado.numero_departamento = data.get('numero_departamento', empleado.numero_departamento)
            empleado.numero_emergencia = data.get('numero_telefono', empleado.numero_emergencia)
            empleado.position = data.get('cargo', empleado.position)
            empleado.is_active = data.get('is_active', empleado.is_active)
            
            if request.FILES.get('foto_perfil'):
                photo_file = request.FILES['foto_perfil']
                file_path, processed_file = optimize_employee_photo(photo_file, empleado.employee_id)
                
                if file_path and processed_file:
                    empleado.foto_perfil = processed_file
                    empleado.foto_perfil.name = file_path
            
            empleado.save()
            
            return JsonResponse({
                'exito': True,
                'mensaje': 'Empleado actualizado exitosamente',
                'empleado': {
                    'employee_id': empleado.employee_id,
                    'nombre': empleado.nombre,
                    'apellido': empleado.apellido
                }
            })
        except Employee.DoesNotExist:
            return JsonResponse({
                'exito': False,
                'mensaje': 'Empleado no encontrado'
            }, status=404)
        except Exception as e:
            print(f"[ERROR] Error en api_editar_empleado: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': f'Error del servidor: {str(e)}'
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def api_sync_zkteco(request):
    """Sincroniza los registros desde el dispositivo ZKTeco y asigna entrada/salida correctamente."""

    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

    try:
        zk_config = settings.ZKTECO
        zk = ZK(zk_config["ip"], port=zk_config["port"], timeout=zk_config["timeout"])
        conn = zk.connect()
        registros = conn.get_attendance()  # <-- Tu función original para obtener los registros

        count = 0
        errores = []
        registros_guardados = []

        for r in registros:
            try:
                # Asegurar timezone
                if timezone.is_naive(r.timestamp):
                    timestamp_real = timezone.make_aware(r.timestamp, timezone.get_default_timezone())
                else:
                    timestamp_real = r.timestamp

                # Buscar empleado
                empleado = Employee.objects.filter(employee_id=str(r.user_id)).first()
                if not empleado:
                    errores.append(f"Empleado {r.user_id} no encontrado en DB")
                    continue

                # Evitar duplicados exactos
                if Asistencia.objects.filter(empleado=empleado, timestamp=timestamp_real).exists():
                    continue

                # --- Lógica entrada/salida en la misma card ---
                registro_hoy = next((reg for reg in registros_guardados if reg['employee_id'] == empleado.employee_id), None)

                if registro_hoy is None:
                    # Primer registro del día → entrada
                    tipo_registro = 'entrada'
                    nuevo_registro = Asistencia.objects.create(
                        empleado=empleado,
                        timestamp=timestamp_real,
                        tipo=tipo_registro,
                        created_at=timezone.now()
                    )
                    registros_guardados.append({
                        'employee_id': empleado.employee_id,
                        'nombre': empleado.nombre,
                        'apellido': empleado.apellido,
                        'dni': empleado.dni,
                        'cargo': empleado.position,
                        'entrada': timestamp_real.strftime("%H:%M:%S"),
                        'salida': None
                    })
                else:
                    # Segundo registro del día → salida
                    tipo_registro = 'salida'
                    nuevo_registro = Asistencia.objects.create(
                        empleado=empleado,
                        timestamp=timestamp_real,
                        tipo=tipo_registro,
                        created_at=timezone.now()
                    )
                    # Actualizamos la misma "card" con la salida
                    registro_hoy['salida'] = timestamp_real.strftime("%H:%M:%S")

                count += 1

            except Exception as e:
                errores.append(f"Error guardando registro {r.user_id}: {str(e)}")

        conn.disconnect()

        return JsonResponse({
            'exito': True,
            'mensaje': f"{count} registros sincronizados",
            'empleados': registros_guardados,
            'advertencias': errores
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'exito': False,
            'mensaje': f'Error de conexión o procesamiento: {str(e)}'
        }, status=500)







def api_asistencia_hoy(request):
    """Devuelve ENTRADA y SALIDA de cada empleado para hoy (una card por empleado)."""
    try:
        hoy = timezone.localdate()
        inicio = timezone.make_aware(datetime.combine(hoy, datetime.min.time()))
        fin = timezone.make_aware(datetime.combine(hoy, datetime.max.time()))

        # Traer solo registros de hoy
        registros_hoy = Asistencia.objects.filter(timestamp__range=(inicio, fin)).order_by('timestamp')

        # Empleados que registraron hoy
        empleados_ids = registros_hoy.values_list('empleado', flat=True).distinct()

        resultado = []

        for emp_id in empleados_ids:
            # Tomamos todos los registros del empleado
            registros_emp = registros_hoy.filter(empleado_id=emp_id).order_by('timestamp')
            emp = registros_emp.first().empleado

            # Primer registro tipo entrada
            entrada_obj = registros_emp.filter(tipo='entrada').first()
            entrada = entrada_obj.timestamp if entrada_obj else None

            # Último registro tipo salida
            salida_obj = registros_emp.filter(tipo='salida').last()
            salida = salida_obj.timestamp if salida_obj else None

            resultado.append({
                "nombre": emp.nombre,
                "apellido": emp.apellido,
                "dni": emp.dni,
                "cargo": emp.position,
                "hora_entrada": entrada.strftime("%H:%M:%S") if entrada else "— Sin registro —",
                "hora_salida": salida.strftime("%H:%M:%S") if salida else "— Sin registro —",
            })

        return JsonResponse({
            "exito": True,
            "empleados": resultado
        })

    except Exception as e:
        return JsonResponse({
            "exito": False,
            "error": str(e)
        }, status=500)

@csrf_exempt
def api_sincronizar(request):
    if request.method == 'GET':
        try:
            dispositivo = obtener_dispositivo()  
            if not dispositivo:
                return JsonResponse({'exito': False, 'mensaje': 'No se puede conectar al dispositivo'})

            logs = dispositivo.get_attendance()
            ultimo = None  # <--- guardamos el último registro

            for log in logs:
                emp, created = Employee.objects.get_or_create(
                    codigo_biometrico=log.user_id,
                    defaults={'nombre': 'Desconocido', 'apellido': '', 'position': ''}
                )

                ultimo = Asistencia.objects.create(
                    empleado=emp,
                    timestamp=log.timestamp
                )

            if not ultimo:
                return JsonResponse({'exito': False, 'mensaje': 'No hay registros nuevos'})

            return JsonResponse({
                'exito': True,
                'mensaje': 'Sincronización completa',
                'empleado': {
                    'nombre': ultimo.empleado.nombre,
                    'apellido': ultimo.empleado.apellido,
                    'position': ultimo.empleado.position,
                    'hora': ultimo.timestamp.strftime('%H:%M:%S'),
                    'fecha': ultimo.timestamp.date().isoformat()
                }
            })

        except Exception as e:
            return JsonResponse({'exito': False, 'mensaje': str(e)}, status=500)


@csrf_exempt
def api_asistencia(request):
    """Devuelve todos los registros de asistencia sin filtrar por fecha"""
    if request.method != 'GET':
        return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)

    try:
        registros = Asistencia.objects.select_related('empleado').order_by('-timestamp')

        empleados = []
        for r in registros:
            empleados.append({
                'employee_id': r.empleado.employee_id,
                'nombre': r.empleado.nombre,
                'apellido': r.empleado.apellido,
                'cargo': r.empleado.position,
                'entrada': r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.tipo=='entrada' else None,
                'salida': r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.tipo=='salida' else None,
                'tipo': r.tipo,
            })

        return JsonResponse({
            'exito': True,
            'empleados': empleados
        })

    except Exception as e:
        return JsonResponse({
            'exito': False,
            'mensaje': str(e)
        }, status=500)
    
@csrf_exempt
def api_asistencia_rango(request):
    """Obtiene registros de asistencia en un rango de fechas"""
    if request.method == 'GET':
        try:
            fecha_inicio = request.GET.get('fecha_inicio')
            fecha_fin = request.GET.get('fecha_fin')
            employee_id = request.GET.get('employee_id')
            
            if not fecha_inicio or not fecha_fin:
                return JsonResponse({
                    'exito': False,
                    'mensaje': 'Se requieren fecha_inicio y fecha_fin'
                }, status=400)
            
            inicio = datetime.fromisoformat(fecha_inicio).date()
            fin = datetime.fromisoformat(fecha_fin).date()
            
            query = Asistencia.objects.filter(
                timestamp__date__gte=inicio,
                timestamp__date__lte=fin
            ).select_related('empleado').order_by('-timestamp')
            
            if employee_id:
                query = query.filter(empleado__employee_id=employee_id)
            
            datos_agrupados = {}
            for reg in query:
                fecha = reg.timestamp.date().isoformat()
                emp_id = reg.empleado.employee_id
                
                if fecha not in datos_agrupados:
                    datos_agrupados[fecha] = {}
                
                if emp_id not in datos_agrupados[fecha]:
                    datos_agrupados[fecha][emp_id] = {
                        'employee_id': emp_id,
                        'nombre': reg.empleado.nombre,
                        'apellido': reg.empleado.apellido,
                        'registros': []
                    }
                
                datos_agrupados[fecha][emp_id]['registros'].append({
                    'timestamp': reg.timestamp.isoformat(),
                    'tipo': reg.tipo
                })
            
            return JsonResponse({
                'exito': True,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'datos': datos_agrupados
            })
        except Exception as e:
            print(f"[ERROR] Error en api_asistencia_rango: {str(e)}")
            return JsonResponse({
                'exito': False,
                'mensaje': str(e)
            }, status=500)
    
    return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'}, status=405)


def obtener_asistencia_del_dia(empleado):
    hoy = localdate()

    registros = Asistencia.objects.filter(
        empleado=empleado,
        timestamp__date=hoy
    ).order_by("timestamp")

    entrada = None
    salida = None

    if registros.exists():
        # Primer registro del día → entrada
        entrada_reg = registros.first()
        entrada = entrada_reg.timestamp.strftime("%H:%M:%S")

        # Si hay más de un registro, la última es salida
        if registros.count() > 1:
            salida_reg = registros.last()
            salida = salida_reg.timestamp.strftime("%H:%M:%S")

    return entrada, salida