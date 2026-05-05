import subprocess
import sys
import os

# Capturar argumentos de entrada
input_args = sys.argv[1:]

# Obtener la ruta de la carpeta principal
if len(input_args) > 0:
    folder_path = os.path.dirname(os.path.dirname(input_args[0]))
else:
    folder_path = None

# Directorio donde están ubicados los scripts
UPLOAD_FOLDER = os.path.abspath(os.path.join("", "codes_proceso_completo"))

# Lista de scripts a ejecutar en orden
scripts = [
    'dian_contable_coparativo.py',
    'fe_anulada.py',
    'downloand.py', 
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
for index, script in enumerate(scripts):
    script_path = os.path.join(UPLOAD_FOLDER, script)
    
    if not os.path.isfile(script_path):
        print(f"Archivo no encontrado: {script_path}")
        break
    
    try:
        # Imprime el inicio de la ejecución
        print(f"Start: {script}", flush=True)
        
        # Si es archivo_comprimido.py, pasarle la ruta de la carpeta
        if script == 'archivo_comprimido.py' and folder_path:
            result = subprocess.run([sys.executable, script_path, folder_path], check=True, capture_output=True, text=True)
        else:
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        
        # Imprime el final de la ejecución
        print(f"End: {script}", flush=True)
        print(f"Ejecutado {script_path} con éxito")
        print(result.stdout, flush=True)
        
        # Actualiza el progreso
        progress_percentage = ((index + 1) / total_scripts) * 100
        update_progress(progress_percentage)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_path}")
        print(e.stderr, flush=True)
        break  # Detener la ejecución si hay un error

# Si todo termina con éxito, asegurar que el progreso llegue al 100%
update_progress(100)



