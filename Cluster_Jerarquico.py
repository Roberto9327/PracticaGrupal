import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from data_processing import limpiar_y_preparar_datos

def procesar_cluster(df):
    """Función para procesar el clustering jerárquico."""
    st.subheader('Clustering Jerárquico')
    df_limpio = limpiar_y_preparar_datos(df)

    st.write("Datos limpios:")
    st.dataframe(df_limpio)

    # Seleccionar columnas para clustering
    lista_columnas = df_limpio.columns
    columnas = st.sidebar.multiselect('Seleccione las columnas a utilizar', lista_columnas)

    if columnas:
        X = df_limpio[columnas]
        st.write(X.head())

        # Seleccionar el tipo de enlace
        enlace = st.sidebar.selectbox('Seleccione el tipo de enlace', ['ward', 'complete', 'average', 'single'])
        
        # Calcular la matriz de enlace
        Z = linkage(X, enlace)

        # Graficar el dendrograma
        fig = plt.figure(figsize=(6, 6))
        corte = st.sidebar.slider('Seleccione el valor de corte', 0, 10, 3)
        dendrogram(Z)
        plt.axhline(y=corte, color='r', linestyle='--')
        st.pyplot(fig)

        # Asignar clusters
        k = st.sidebar.slider('Seleccione el número de clusters', 2, 10, 2)
        clusters = fcluster(Z, k, criterion='maxclust')
        df_limpio['Cluster'] = clusters

        st.write(df_limpio.head())
        fig = plt.figure(figsize=(6, 6))
        sns.scatterplot(x=X.iloc[:, 0], y=X.iloc[:, 1], hue=clusters, palette='tab10', legend='full')
        st.pyplot(fig)

    else:
        st.warning('Seleccione al menos una columna')
