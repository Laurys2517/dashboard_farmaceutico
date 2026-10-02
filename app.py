import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(
    page_title="Gestión Comercial y Stock | Droguería",
    page_icon="🏥",
    layout="wide"
)

# Estilo CSS personalizado para limpiar espacio e interfaces
st.markdown("""
    <style>
    .block-container { padding-top: 1.8rem; padding-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #1E293B; }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem; color: #64748B; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# Cargar datos
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

# Encabezado principal
st.title("🏥 Reporte de Gestión Comercial e Inventario")
st.caption("Monitoreo ejecutivo de indicadores de venta, distribución y control de stock.")
st.divider()

# Sidebar - Filtros
with st.sidebar:
    st.header("⚙️ Parámetros")
    categorias_sel = st.multiselect(
        "Filtrar por Categoría:",
        options=df["Categoría"].unique(),
        default=df["Categoría"].unique()
    )

df_filtrado = df[df["Categoría"].isin(categorias_sel)]

# Métricas Principales (KPI Cards)
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Ventas Totales", f"${df_filtrado['Ventas_USD'].sum():,.2f}")

with col2:
    with st.container(border=True):
        st.metric("Volumen Despachado", f"{df_filtrado['Unidades_Vendidas'].sum():,} uds")

with col3:
    with st.container(border=True):
        prom_venta = df_filtrado['Ventas_USD'].mean() if not df_filtrado.empty else 0
        st.metric("Ticket Promedio / Prod.", f"${prom_venta:,.2f}")

with col4:
    with st.container(border=True):
        alertas = len(df_filtrado[df_filtrado['Stock_Actual'] < 50])
        st.metric("Críticos en Stock (<50)", f"{alertas} prod.", delta_color="inverse")

st.markdown("##")

# Pestañas para organizar la información
tab_ventas, tab_stock, tab_tabla = st.tabs([
    "📊 Análisis de Ventas", 
    "📦 Control de Stock", 
    "📋 Base de Datos"
])

# Pestaña 1: Ventas
with tab_ventas:
    df_cat = df_filtrado.groupby("Categoría", as_index=False)["Ventas_USD"].sum().sort_values("Ventas_USD", ascending=True)
    
    fig_ventas = px.bar(
        df_cat,
        x="Ventas_USD",
        y="Categoría",
        orientation="h",
        text_auto="$,.2f",
        title="<b>Ventas Consolidadas por Categoría (USD)</b>",
        color_discrete_sequence=["#2563EB"]
    )
    
    fig_ventas.update_layout(
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=10, r=20, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380
    )
    fig_ventas.update_traces(textposition="outside", cliponaxis=False)
    
    st.plotly_chart(fig_ventas, use_container_width=True)

# Pestaña 2: Stock
with tab_stock:
    df_stock = df_filtrado.sort_values("Stock_Actual", ascending=False)
    
    # Marcamos en rojo si está crítico
    colors = ["#EF4444" if val < 50 else "#0EA5E9" for val in df_stock["Stock_Actual"]]
    
    fig_stock = px.bar(
        df_stock,
        x="Medicamento",
        y="Stock_Actual",
        text_auto=True,
        title="<b>Nivel de Inventario Actual por Producto</b> (Rojo = Crítico < 50 unidades)"
    )
    
    fig_stock.update_traces(marker_color=colors, textposition="outside")
    fig_stock.update_layout(
        xaxis_title="",
        yaxis_title="Unidades en Depósito",
        margin=dict(l=10, r=20, t=40, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380
    )
    
    st.plotly_chart(fig_stock, use_container_width=True)

# Pestaña 3: Tabla Detallada
with tab_tabla:
    st.subheader("Detalle del Inventario y Ventas")
    
    # Formateo de la tabla de datos
    st.dataframe(
        df_filtrado,
        column_config={
            "Medicamento": "Producto / Presentación",
            "Categoría": "Categoría Terapéutica",
            "Ventas_USD": st.column_config.NumberColumn("Ventas Totales", format="$%,.2f"),
            "Unidades_Vendidas": st.column_config.NumberColumn("Unidades Vendidas", format="%d uds"),
            "Stock_Actual": st.column_config.NumberColumn("Stock Disponible", format="%d uds"),
        },
        hide_index=True,
        use_container_width=True
    )
