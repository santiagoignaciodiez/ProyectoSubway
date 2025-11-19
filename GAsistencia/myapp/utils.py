import os
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pathlib import Path
from io import BytesIO
from zk import ZK

def process_employee_photo(photo_file, employee_id):
    """
    Procesa y renombra automáticamente la foto del empleado
    """
    try:
        # Validar que sea una imagen
        img = Image.open(photo_file)
        img.verify()
        
        # Obtener extensión original
        extension = photo_file.name.split('.')[-1].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            raise ValueError("Formato de imagen no válido")
        
        # Crear nuevo nombre: employee_id.extension
        new_filename = f"{employee_id}.{extension}"
        
        # Ruta de almacenamiento: profile_pictures/employee_id.extension
        file_path = f"profile_pictures/{new_filename}"
        
        return file_path, photo_file
        
    except Exception as e:
        print(f"[v0] Error procesando foto para {employee_id}: {str(e)}")
        return None, None

def optimize_employee_photo(photo_file, employee_id, max_size=(500, 500)):
    """
    Optimiza la foto del empleado redimensionándola y la guarda en el almacenamiento
    
    Args:
        photo_file: Archivo de foto subido
        employee_id: ID único del empleado
        max_size: Tamaño máximo de la imagen
    
    Returns:
        Ruta del archivo guardado
    """
    try:
        # Abrir y validar imagen
        img = Image.open(photo_file)
        
        # Redimensionar si es más grande
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es PNG con transparencia
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        extension = photo_file.name.split('.')[-1].lower()
        new_filename = f"{employee_id}.jpg"  # Siempre guardar como JPEG para consistencia
        file_path = f"profile_pictures/{new_filename}"
        
        # Guardar imagen optimizada en el almacenamiento
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        
        # Guardar en el almacenamiento de Django
        file_path_saved = default_storage.save(file_path, ContentFile(buffer.read()))
        
        print(f"[v0] Foto guardada para {employee_id} en: {file_path_saved}")
        
        return file_path_saved
        
    except Exception as e:
        print(f"[v0] Error optimizando foto para {employee_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def obtener_dispositivo():
    """
    Conecta con el dispositivo ZKTeco y devuelve la instancia conectada.
    """
    try:
        zk = ZK(
            '192.168.1.201',  # IP del dispositivo
            port=4370,
            timeout=5,
            password=0,
            force_udp=False,
            ommit_ping=False
        )
        dispositivo = zk.connect()
        return dispositivo
    except Exception as e:
        print(f"[ERROR] No se pudo conectar al dispositivo: {e}")
        return None