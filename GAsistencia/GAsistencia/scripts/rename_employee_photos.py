import os
import sys
from pathlib import Path
from PIL import Image
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GAsistencia.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from myapp.models import Employee

def rename_and_organize_photos():
    """
    Renombra todas las fotos en la carpeta empleados y las asocia con el employee_id
    """
    # Rutas
    base_dir = Path(__file__).resolve().parent.parent
    media_root = base_dir / 'media'
    empleados_folder = media_root / 'profile_pictures'
    
    # Crear carpeta si no existe
    empleados_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"[v0] Escaneando fotos en: {empleados_folder}")
    
    renamed_count = 0
    
    # Buscar todas las imágenes en la carpeta
    for image_file in empleados_folder.glob('*'):
        if image_file.is_file() and image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            try:
                # Intentar abrir la imagen para validarla
                with Image.open(image_file) as img:
                    # La imagen es válida
                    pass
                
                print(f"[v0] Procesando imagen: {image_file.name}")
                
                # Aquí puedes agregar lógica adicional como:
                # - Buscar el employee_id basado en metadatos
                # - Crear una relación entre foto y empleado
                # - Renombrar la foto
                
                renamed_count += 1
                
            except Exception as e:
                print(f"[v0] Error procesando {image_file.name}: {str(e)}")
    
    print(f"[v0] Procesadas {renamed_count} fotos correctamente")

if __name__ == '__main__':
    rename_and_organize_photos()
