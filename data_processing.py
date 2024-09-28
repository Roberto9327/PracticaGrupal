import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

@st.cache_data
def cargar_datos(archivo):
    """Carga datos desde un archivo CSV o XLSX."""
    try:
        if archivo.name.endswith('.csv'):
            return pd.read_csv(archivo)
        elif archivo.name.endswith('.xlsx'):
            return pd.read_excel(archivo)
        else:
            st.error("Formato no soportado. Utilice archivos CSV o XLSX.")
            return None
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        return None

def limpiar_y_preparar_datos(df):
    """Limpia y prepara los datos."""
    df = df.dropna()  # Eliminar filas con NaN
    return df

def reducir_dimensionalidad(df):
    """Aplica t-SNE para reducir la dimensionalidad."""
    tsne_model = TSNE(n_components=2, random_state=42)
    return tsne_model.fit_transform(df)

def realizar_clustering(data, n_clusters):
    """Realiza clustering KMeans en los datos reducidos."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    return kmeans.fit_predict(data)

def procesar_datos(df):
    """Función principal para procesar los datos cargados."""
    st.subheader('Datos Cargados')
    st.dataframe(df)

    df_limpio = limpiar_y_preparar_datos(df)

    st.write("Datos limpios:")
    st.dataframe(df_limpio)

    # Reducción de Dimensionalidad
    if st.checkbox('Aplicar reducción de dimensionalidad'):
        reduced_data = reducir_dimensionalidad(df_limpio.select_dtypes(include=['float', 'int']))
        
        # Slider para el número de clusters
        n_clusters = st.slider('Número de clusters', 2, 10, 3)

        # Clustering
        clusters = realizar_clustering(reduced_data, n_clusters)

        # Agregar la columna de clusters al DataFrame
        df_limpio['Cluster'] = clusters

        # Visualización del gráfico de t-SNE
        st.write("Gráfico de t-SNE:")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=clusters, palette='tab10', legend='full')
        plt.title(f'T-SNE con {n_clusters} Clusters')
        st.pyplot(plt)

        st.write("Datos con clusters asignados:")
        st.dataframe(df_limpio)
