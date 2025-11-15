from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime

class EmployeeManager(BaseUserManager):
    def generar_employee_id(self):
        """Genera el próximo ID de empleado en formato YYXXXX"""
        anio_actual = datetime.now().year % 100  # Obtiene últimos 2 dígitos del año (25 para 2025)
        prefijo = str(anio_actual)
        
        # Buscar el último empleado del año actual
        ultimo_empleado = self.filter(employee_id__startswith=prefijo).order_by('-employee_id').first()
        
        if ultimo_empleado:
            # Extraer el número secuencial y sumarle 1
            ultimo_numero = int(ultimo_empleado.employee_id[2:])
            nuevo_numero = ultimo_numero + 1
        else:
            # Primer empleado del año
            nuevo_numero = 1
        
        # Formatear como YYXXXX (ej: 250001)
        return f"{prefijo}{nuevo_numero:04d}"

class Employee(AbstractBaseUser, PermissionsMixin):
    # ID de empleado generado automáticamente
    employee_id = models.CharField("ID de Empleado", max_length=6, unique=True, primary_key=True)
    
    # Información personal básica
    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    dni = models.CharField("DNI", max_length=8, unique=True)
    cuil = models.CharField("CUIL", max_length=11, unique=True)
    foto_perfil = models.ImageField("Foto de Perfil", upload_to='empleados/', null=True, blank=True)
    
    email = models.EmailField("Correo Electrónico", blank=True, null=True)
    
    setup_completo = models.BooleanField("Setup Completo", default=False)
    
    # Datos demográficos
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    genero = models.CharField("Género", max_length=1, choices=GENERO_CHOICES)
    edad = models.IntegerField("Edad")
    fecha_nacimiento = models.DateField("Fecha de Nacimiento")
    
    ESTADO_CIVIL_CHOICES = [
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('divorciado', 'Divorciado/a'),
        ('viudo', 'Viudo/a'),
    ]
    estado_civil = models.CharField("Estado Civil", max_length=20, choices=ESTADO_CIVIL_CHOICES)
    tiene_hijos = models.BooleanField("Tiene Hijos", default=False)
    
    # Información de domicilio
    nombre_domicilio = models.CharField("Nombre del Domicilio", max_length=200)
    numero_departamento = models.CharField("Número de Departamento", max_length=10, blank=True, null=True)
    piso_departamento = models.CharField("Piso de Departamento", max_length=10, blank=True, null=True)
    numero_casa = models.CharField("Número de Casa", max_length=10, blank=True, null=True)
    
    # Contacto de emergencia
    numero_emergencia = models.CharField("Número de Emergencia", max_length=20)
    
    # Información laboral
    position = models.CharField("Cargo", max_length=100, default="Empleado")
    is_manager = models.BooleanField("Es Gerente", default=False)
    is_active = models.BooleanField("Activo", default=True)
    password = models.CharField("Contraseña", max_length=128)
    
    objects = EmployeeManager()
    
    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'dni']
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
    
    def __str__(self):
        return f"{self.employee_id} - {self.nombre} {self.apellido}"
    
    def save(self, *args, **kwargs):
        # Generar employee_id automáticamente si no existe
        if not self.employee_id:
            self.employee_id = Employee.objects.generar_employee_id()
        super().save(*args, **kwargs)


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='registros_asistencia', verbose_name="Empleado")
    check_in = models.DateTimeField("Hora de Entrada", auto_now_add=True)
    check_out = models.DateTimeField("Hora de Salida", null=True, blank=True)
    date = models.DateField("Fecha", auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"
        ordering = ['-check_in']
    
    def __str__(self):
        return f"{self.employee.nombre} - {self.date}"
