import streamlit as st
from data_processing import cargar_datos, limpiar_y_preparar_datos

st.title('Análisis de Datos de Vinos')

st.sidebar.title('Opciones')

opciones = ['Cargar datos', 'Clustering Jerárquico', 't-SNE']
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
        df = limpiar_y_preparar_datos(st.session_state.df)  # Limpiar datos antes de procesar
        if opcion == 'Clustering Jerárquico':
            from Cluster_Jerarquico import procesar_cluster
            procesar_cluster(df)
        elif opcion == 't-SNE':
            from t_SNE import procesar_tsne
            procesar_tsne(df)
    else:
        st.warning('No hay datos cargados. Por favor, carga un archivo primero.')
