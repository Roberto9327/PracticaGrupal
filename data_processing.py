import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos(archivo):
    """Carga datos desde un archivo CSV o XLSX."""
    try:
        # Verificar que el archivo se haya subido
        if archivo is not None:
            if archivo.name.endswith('.csv'):
                df = pd.read_csv(archivo)  # Cargar CSV
                return df
            elif archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)  # Cargar XLSX
                return df
            else:
                st.error("Formato no soportado. Utilice archivos CSV o XLSX.")
                return None
        else:
            st.error("No se ha subido ningún archivo.")
            return None
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el archivo: {e}")
        return None

def limpiar_y_preparar_datos(df):
    """Limpia y prepara los datos eliminando filas con valores NaN."""
    if df is not None:  # Verificar que el DataFrame no sea None
        df = df.dropna()  # Eliminar filas con NaN
    else:
        st.error("No hay datos para limpiar.")
    return df
