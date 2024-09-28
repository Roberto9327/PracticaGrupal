import streamlit as st
from data_processing import cargar_datos, procesar_datos

st.title('Análisis de Datos con Streamlit')

st.sidebar.title('Opciones')

opciones = ['Cargar datos', 'Realizar Análisis']
opcion = st.sidebar.selectbox('Seleccione una opción', opciones)

if opcion == 'Cargar datos':
    st.write("Sube tu archivo CSV o XLSX para iniciar el análisis.")
    archivo = st.file_uploader('Seleccione un archivo', type=['csv', 'xlsx'])
    
    if archivo:
        st.session_state.df = cargar_datos(archivo)
        if st.session_state.df is not None:
            st.success('Datos cargados exitosamente.')
else:
    if 'df' in st.session_state:
        procesar_datos(st.session_state.df)
    else:
        st.warning('No hay datos cargados. Por favor, carga un archivo primero.')
