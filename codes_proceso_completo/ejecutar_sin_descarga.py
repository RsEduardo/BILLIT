import subprocess
import sys
import os

# Capturar argumentos: folder_path y timestamp específico (opcional)
folder_path = sys.argv[1] if len(sys.argv) > 1 else None
timestamp_filter = sys.argv[2] if len(sys.argv) > 2 else None

# Directorio donde están ubicados los scripts
UPLOAD_FOLDER = os.path.abspath(os.path.join("", "codes_proceso_completo"))

# Lista de scripts a ejecutar en orden
scripts = [
    'info_dian.py', 
    'cuenta_proveedor.py', 
    'importar_doc.py', 
    'info_complem.py',
    'archivo_comprimido.py'
]

# Ruta al archivo de progreso
progress_file_path = os.path.join(UPLOAD_FOLDER, 'progreso.txt')

# Función para actualizar el archivo de progreso
def update_progress(progress):
    with open(progress_file_path, 'w') as f:
        f.write(str(progress))

total_scripts = len(scripts)
progress_percentage = 0
for index, script in enumerate(scripts):
    script_path = os.path.join(UPLOAD_FOLDER, script)
    
    if not os.path.isfile(script_path):
        print(f"Archivo no encontrado: {script_path}")
        break
    
    try:
        # Imprime el inicio de la ejecución
        print(f"Start: {script}", flush=True)
        
        # Construir argumentos según el script
        # archivo_comprimido.py espera: folder_path [timestamp]
        # Los demás scripts esperan: [timestamp]
        if script == 'archivo_comprimido.py' and folder_path:
            args = [sys.executable, script_path, folder_path]
            if timestamp_filter:
                args.append(timestamp_filter)
        else:
            args = [sys.executable, script_path]
            if timestamp_filter:
                args.append(timestamp_filter)
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        
        # Imprime el final de la ejecución
        print(f"End: {script}", flush=True)
        print(f"Ejecutado {script_path} con éxito")
        
        # Actualiza el progreso
        progress_percentage = ((index + 1) / total_scripts) * 100
        update_progress(progress_percentage)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_path}")
        print(e.stderr, flush=True)
        break
    except Exception as e:
        import traceback
        print(f"Excepción al ejecutar {script_path}: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        break

# Si el último script no se ejecutó correctamente (progreso < 100%), salir con error
if progress_percentage < 100:
    sys.exit(1)

# Si todo termina con éxito, asegurar que el progreso llegue al 100%
update_progress(100)