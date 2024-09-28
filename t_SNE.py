import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from data_processing import limpiar_y_preparar_datos

def procesar_tsne(df):
    """Función para procesar t-SNE."""
    st.title('t-SNE')
    df_limpio = limpiar_y_preparar_datos(df)

    st.write("Datos limpios:")
    st.dataframe(df_limpio)

    # Verificar si la columna 'Alcohol' está presente
    if 'Alcohol' in df_limpio.columns:
        n_components = st.sidebar.slider('Número de componentes', 2, 10, 2)
        perplexity = st.sidebar.slider('Perplexity', 5, 50, 30)
        n_sample = st.sidebar.slider('Número de muestras', 1000, 70000, 5000)

        x = np.asanyarray(df_limpio.drop(columns=['Alcohol']))[:n_sample, :]  # Cambiado a 'Alcohol'
        y = np.asanyarray(df_limpio['Alcohol'])[:n_sample].ravel()  # Cambiado a 'Alcohol'

        tsne = TSNE(n_components=n_components, perplexity=perplexity)
        x2 = tsne.fit_transform(x)

        if n_components == 2:
            fig = plt.figure(figsize=(6, 6))
            sns.scatterplot(x=x2[:, 0], y=x2[:, 1], hue=y, palette='viridis', s=50)
            st.pyplot(fig)
        else:
            fig_3d = plt.figure(figsize=(6, 6))
            ax = fig_3d.add_subplot(111, projection='3d')
            ax.scatter(x2[:, 0], x2[:, 1], x2[:, 2], c=y, cmap='viridis', s=50)
            st.pyplot(fig_3d)
    else:
        st.warning("La columna 'Alcohol' no está presente en los datos.")
