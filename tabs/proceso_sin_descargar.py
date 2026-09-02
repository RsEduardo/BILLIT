import streamlit as st
import os
from datetime import datetime
import subprocess
import sys

def run(subfolder):
    st.markdown("## Procesar Archivos")
    st.markdown("### Subida de Archivos")
    
    col1, col2 = st.columns(2)

    with col1:
        uploaded_files = st.file_uploader("Cargar facturas (puede seleccionar múltiples archivos)", type="pdf", accept_multiple_files=True)
        st.markdown("- **Documentos:** Facturas electronicas")
        st.markdown("- **Especifición:**  *Formato Dian* - *Formato Pdf*")

    with col2:
        cuentas_file = st.file_uploader("Sube el archivo MovDocCuenta_CSV.csv", type="csv", key='cuentas')
        st.markdown("- **Nombre reporte:** *Movimiento por documento y cuenta*")
        st.markdown("- **Fecha a seleccionar:** *Varios periodos anteriores*")
        st.markdown("- **Especifición:** *No seleccionar especificaciones*")
        st.markdown("- **Seleccion de Cuenta:** Cuentas *Pasivo 2 - Costo 7*")
    
    if st.button('Procesar Facturas y CSV'):
        if uploaded_files and cuentas_file:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")

            subfolder_path = os.path.join(subfolder, timestamp)
            os.makedirs(subfolder_path, exist_ok=True)

            for uploaded_file in uploaded_files:
                file_path = os.path.join(subfolder_path, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            csv_file_path = os.path.join(subfolder_path, "MovDocCuenta_CSV.csv")
            with open(csv_file_path, "wb") as f:
                f.write(cuentas_file.getbuffer())

            st.success(f'Se han guardado {len(uploaded_files)} archivos PDF y el archivo CSV en la carpeta {timestamp}')

            st.markdown('<style>div[data-testid="stProgress"] { height: 24px; }</style>', unsafe_allow_html=True)
            progress_bar = st.progress(0)

            try:
                UPLOAD_FOLDER = os.path.abspath("codes_proceso_completo")
                fixed_script_path = os.path.join(UPLOAD_FOLDER, 'ejecutar_sin_descarga.py')

                process = subprocess.Popen(
                    [sys.executable, fixed_script_path, subfolder, timestamp],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                total_scripts = 5
                completed_scripts = 0

                with st.spinner('Procesando...'):
                    for line in iter(process.stdout.readline, ''):
                        line = line.strip()
                        if "Start:" in line:
                            pass
                        elif "End:" in line:
                            completed_scripts += 1
                            progress = completed_scripts / total_scripts
                            progress_bar.progress(progress)

                    process.wait()
                    process.communicate()

                    if process.returncode == 0:
                        st.success('Los archivos fueron procesados con éxito')

                        zip_filename = f"{timestamp}.zip"
                        zip_filepath = os.path.join(subfolder, zip_filename)

                        if os.path.exists(zip_filepath):
                            with open(zip_filepath, "rb") as f:
                                st.download_button(
                                    label="Descargar archivo ZIP",
                                    data=f,
                                    file_name=zip_filename,
                                    mime='application/zip'
                                )
                        else:
                            st.error('Ocurrió un error en el sistema, comuníquese con soporte')
                    else:
                        st.error('Ocurrió un error en el sistema, comuníquese con soporte')
            except Exception as e:
                st.error('Ocurrió un error en el sistema, comuníquese con soporte')
        else:
            st.error('Debe cargar al menos un archivo de factura y el archivo CSV')

if __name__ == "__main__":
    subfolder = os.path.abspath("archivos_usuarios")
    os.makedirs(subfolder, exist_ok=True)
    run(subfolder)
