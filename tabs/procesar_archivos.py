import streamlit as st
import os
import subprocess
import sys
from datetime import datetime

def run(subfolder):
    st.markdown("## Procesar Archivos")
    st.markdown("### Subida de Archivos")
    col1, col2, col3 = st.columns(3)

    with col1:
        dian_file = st.file_uploader("Sube el archivo DIAN.xlsx", type="xlsx", key='dian')
        st.markdown("- **Nombre reporte:** *Facturas recibidas* - *Reporte Dian*")
        st.markdown("- **Especificación:** Reporte *Detallado de documentos electronicos recibidos - emitido por la DIAN*")

    with col2:
        sinco_file = st.file_uploader("Sube el archivo SINCO.xlsx", type="xlsx", key='sinco')
        st.markdown("- **Nombre reporte:** *Movimiento por documento y cuenta*")
        st.markdown("- **Fecha a seleccionar:** *Periodo del reporte DIAN*")
        st.markdown("- **Especificación:**  Seleccionar *Concepto y Doc del tercero*")
        st.markdown("- **Seleccion de Cuenta:** Cuentas *Activo 1 - Costo 7*")

    with col3:
        cuentas_file = st.file_uploader("Sube el archivo MovDocCuenta_CSV.csv", type="csv", key='cuentas')
        st.markdown("- **Nombre reporte:** *Movimiento por documento y cuenta*")
        st.markdown("- **Fecha a seleccionar:** *Varios periodos anteriores*")
        st.markdown("- **Especificación:** *No seleccionar especificaciones*")
        st.markdown("- **Seleccion de Cuenta:** Cuentas *Pasivo 2 - Costo 7*")

    if st.button('Procesar Archivos'):
        if dian_file and sinco_file and cuentas_file:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")

            subfolder_path = os.path.join(subfolder, timestamp)
            os.makedirs(subfolder_path, exist_ok=True)

            dian_path = os.path.join(subfolder_path, 'DIAN.xlsx')
            sinco_path = os.path.join(subfolder_path, 'SINCO.xlsx')
            cuentas_path = os.path.join(subfolder_path, 'MovDocCuenta_CSV.csv')

            with open(dian_path, 'wb') as f:
                f.write(dian_file.getbuffer())
            with open(sinco_path, 'wb') as f:
                f.write(sinco_file.getbuffer())
            with open(cuentas_path, 'wb') as f:
                f.write(cuentas_file.getbuffer())

            st.markdown('<style>div[data-testid="stProgress"] { height: 24px; }</style>', unsafe_allow_html=True)
            progress_bar = st.progress(0)

            try:
                UPLOAD_FOLDER = os.path.abspath("archivos_usuarios")
                fixed_script_path = os.path.abspath("codes_proceso_completo/ejecutar_complet.py")

                process = subprocess.Popen(
                    [sys.executable, fixed_script_path, dian_path, sinco_path, cuentas_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                total_scripts = 8
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
            st.error('Todos los archivos deben ser seleccionados')
