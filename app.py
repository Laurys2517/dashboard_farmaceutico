import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Analítico - Sector Farmacéutico",
    page_icon="💊",
    layout="wide"
)

# Título Principal
st.title("💊 Dashboard de Control de Ventas e Inventario Farmacéutico")
st.markdown("Plataforma interactiva para el seguimiento de métricas comerciales, rotación de productos y niveles de stock.")

# Datos de demostración
@st.cache_data
def cargar_datos():
    data = {
        "Medicamento": ["Acetaminofén 500mg", "Ibuprofeno 400mg", "Amoxicilina 500mg", "Loratadina 10mg", "Omeprazol 20mg", "Vitamina C 1g"],
        "Categoría": ["Analgesia", "Analgesia", "Antibióticos", "Antihistamínicos", "Gastroenterología", "Vitaminas"],
        "Ventas_USD": [12500, 9800, 15400, 6200, 8900, 11100],
        "Unidades_Vendidas": [5000, 3900, 2200, 3100, 2950, 4400],
        "Stock_Actual": [120, 45, 300, 80, 15, 600]
    }
    return pd.DataFrame(data)

df = cargar_datos()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros de Consulta")
categorias = st.sidebar.multiselect(
    "Selecciona Categorías:",
    options=df["Categoría"].unique(),
    default=df["Categoría"].unique()
)

df_filtrado = df[df["Categoría"].isin(categorias)]

# Sección de KPIs principales
col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales ($)", f"${df_filtrado['Ventas_USD'].sum():,.2f}")
col2.metric("Unidades Despachadas", f"{df_filtrado['Unidades_Vendidas'].sum():,} uds")
col3.metric("Productos en Alerta Stock (<50)", len(df_filtrado[df_filtrado['Stock_Actual'] < 50]))

st.divider()

# Gráficos interactivos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Ventas por Categoría ($)")
    fig_ventas = px.bar(
        df_filtrado, 
        x="Categoría", 
        y="Ventas_USD", 
        color="Categoría",
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_ventas, use_container_width=True)

with col_right:
    st.subheader("📦 Estado de Stock e Inventario")
    fig_stock = px.bar(
        df_filtrado, 
        x="Medicamento", 
        y="Stock_Actual", 
        color="Stock_Actual",
        color_continuous_scale="Reds_r",
        text_auto=True
    )
    st.plotly_chart(fig_stock, use_container_width=True)

# Tabla de Datos
st.subheader("📋 Detalle General de Productos")
st.dataframe(df_filtrado, use_container_width=True)