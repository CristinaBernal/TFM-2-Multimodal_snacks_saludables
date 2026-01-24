# ============================================================
# app.py - Dashboard Streamlit Snacks Saludables
# ============================================================

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# BLOQUE 0: Configuración básica
# ============================================================
st.set_page_config(
    page_title="Dashboard Snacks Saludables",
    layout="wide",
    initial_sidebar_state="expanded"
)

OUTPUT_PATH = Path(r"H:\Cristina\Mis documentos\Github\TFM-2-A.Multimodal_snacks_saludables\outputs")

st.title("Dashboard Snacks Saludables")
st.markdown("---")

# ============================================================
# BLOQUE 1: Mostrar resumen generado por LLM
# ============================================================
resumen_path = OUTPUT_PATH / "resumen_mercado_snacks_saludables.txt"
if resumen_path.exists():
    with open(resumen_path, "r", encoding="utf-8") as f:
        resumen_texto = f.read()
    st.subheader("Resumen de Mercado")
    st.markdown(resumen_texto)
else:
    st.warning("No se encontró el resumen generado.")

st.markdown("---")

# ============================================================
# BLOQUE 2: Cargar CSV de barras y heatmap
# ============================================================
barras_path = OUTPUT_PATH / "barras.csv"
heatmap_path = OUTPUT_PATH / "heatmap.csv"

df_barras = pd.read_csv(barras_path) if barras_path.exists() else pd.DataFrame()
df_heatmap = pd.read_csv(heatmap_path) if heatmap_path.exists() else pd.DataFrame()

# ============================================================
# BLOQUE 3: Filtros sidebar
# ============================================================
st.sidebar.header("Filtros Interactivos")

# Filtro categorías
categorias = df_barras['Lista_Categorias'].unique() if not df_barras.empty else []
categorias_seleccionadas = st.sidebar.multiselect(
    "Selecciona categorías:",
    options=categorias,
    default=categorias
)

# Filtro atributos para heatmap
atributos = df_heatmap['Lista_Atributos'].unique() if not df_heatmap.empty else []
atributos_seleccionados = st.sidebar.multiselect(
    "Selecciona atributos (heatmap):",
    options=atributos,
    default=atributos
)

st.markdown("---")

# ============================================================
# BLOQUE 4: Mostrar tabla y gráfica de barras apiladas
# ============================================================
if not df_barras.empty:
    df_barras_filtrado = df_barras[df_barras['Lista_Categorias'].isin(categorias_seleccionadas)]
    st.subheader("Barras apiladas por número de menciones")
    st.dataframe(df_barras_filtrado)

    # Gráfico de barras apiladas
    tabla_abs = pd.crosstab(df_barras_filtrado['Lista_Categorias'], df_barras_filtrado['Sentimiento'])
    tabla_abs = tabla_abs[['negativo','neutro','positivo']] if all(x in tabla_abs.columns for x in ['negativo','neutro','positivo']) else tabla_abs

    colores = {'negativo':'#e74c3c','neutro':'#95a5a6','positivo':'#2ecc71'}
    colores_plot = [colores[c] for c in tabla_abs.columns]

    fig, ax = plt.subplots(figsize=(12,7))
    tabla_abs.plot(kind='barh', stacked=True, color=colores_plot, ax=ax, width=0.75, edgecolor='white')
    ax.set_xlabel("Número de menciones")
    ax.set_ylabel("")
    ax.set_title("Panorama del Mercado: ¿De qué se habla más y con qué valoración?", fontsize=14, fontweight='bold')
    ax.legend(title="Sentimiento", bbox_to_anchor=(1,1), loc='upper left')
    st.pyplot(fig)
else:
    st.warning("No se encontró el CSV de barras.")

st.markdown("---")

# ============================================================
# BLOQUE 5: Mostrar heatmap
# ============================================================
if not df_heatmap.empty:
    df_heatmap_filtrado = df_heatmap[
        (df_heatmap['Lista_Categorias'].isin(categorias_seleccionadas)) &
        (df_heatmap['Lista_Atributos'].isin(atributos_seleccionados))
    ]
    if not df_heatmap_filtrado.empty:
        st.subheader("Heatmap de Categoría vs Atributo")
        matriz = pd.crosstab(df_heatmap_filtrado['Lista_Categorias'], df_heatmap_filtrado['Lista_Atributos'])
        fig, ax = plt.subplots(figsize=(12,7))
        sns.heatmap(matriz, annot=True, fmt='d', cmap="Blues", linewidths=1, cbar_kws={'label':'Menciones'}, ax=ax)
        ax.set_xlabel("Atributo")
        ax.set_ylabel("Categoría")
        st.pyplot(fig)
    else:
        st.info("No hay datos para mostrar en el heatmap con los filtros seleccionados.")
else:
    st.warning("No se encontró el CSV de heatmap.")
