import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================
st.set_page_config(
    page_title="Panel de Emisiones GEI - UPCH",
    layout="wide"
)

# ==================================================
# ESTILO Y DISEÑO PERSONALIZADO
# ==================================================
estilo_diseño = """
<style>
/* Fondo degradado suave y moderno para toda la aplicación */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f4f7f6 0%, #e2ebf0 100%);
    background-attachment: fixed;
}

/* Hacer la barra lateral más limpia y profesional */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e0e0e0;
}

/* Darle estilo a los títulos y textos */
h1 {
    color: #0A2540;
    font-weight: 800 !important;
}
h2 {
    color: #1A365D;
}
</style>
"""
st.markdown(estilo_diseño, unsafe_allow_html=True)

# ==================================================
# BARRA LATERAL (Logo de Universidad e Info de Autor)
# ==================================================
with st.sidebar:
    # URL oficial de la imagen del logo de la UPCH
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQboXRC_mMBO5jSs8RObrKqgR6w-ln0yX7xFty4ZVDqz4mElYhGED0QBCGb&s=10", 
        use_container_width=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏫 **Facultad de Ciencias**")
    st.markdown("**Proyecto:** Monitoreo de Gases de Efecto Invernadero")
    st.markdown("**Estudiante:** Ruth Turpo y Leonela Aldana")
    st.write("---")
    st.info("💡 *Consejo: Navega por las pestañas superiores para explorar los diferentes contaminantes medidos en Gigagramos.*")

# ==========================
# CARGA DE DATOS
# ==========================
df = pd.read_csv(
    "Dataset GEI CSV_0 (1).csv",
    sep=";"
)

# Convertir ANIO correctamente
df["ANIO"] = pd.to_numeric(df["ANIO"], errors="coerce")
df = df.dropna(subset=["ANIO"])
df["ANIO"] = df["ANIO"].astype(int)

# ==========================
# TÍTULO PRINCIPAL CON SÍMBOLO
# ==========================
st.title("🏭 Emisiones de gases de efecto invernadero (GEI)")
st.markdown("Análisis ambiental avanzado de emisiones de Gases de Efecto Invernadero por sectores y subcategorías.")

# ==========================
# PESTAÑAS (5 pestañas)
# ==========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Evolución Temporal",
    "☁️ Dióxido de Carbono (CO₂)",
    "🍕 Metano (CH₄)",
    "🍕 Metano Equivalente",
    "🍕 Óxido Nitroso (N₂O)"
])

# Lista de años única para los selectores
lista_anios = sorted(df["ANIO"].unique())

# ==================================================
# TAB 1 - EVOLUCIÓN TEMPORAL
# ==================================================
with tab1:
    st.header("📈 Emisiones de Dióxido de Carbono a través del tiempo")

    df_linea = (
        df.groupby(
            ["ANIO", "SUBCATEGORIA"]
        )["DIOXIDO_DE_CARBONO_GGCO2"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        df_linea,
        x="ANIO",
        y="DIOXIDO_DE_CARBONO_GGCO2",
        color="SUBCATEGORIA",
        markers=True,
        title="Evolución histórica de emisiones de CO₂"
    )

    fig1.update_layout(
        xaxis_title="Año",
        yaxis_title="Gigagramos de CO₂",
        legend_title="Subcategoría",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# TAB 2 - CO2
# ==================================================
with tab2:
    st.header("☁️ Porcentaje de emisiones de Dióxido de Carbono (CO₂)")

    anio_co2 = st.selectbox(
        "Seleccione un año de análisis para CO₂:",
        lista_anios,
        key="co2"
    )

    df_co2 = (
        df[df["ANIO"] == anio_co2]
        .groupby("SUBCATEGORIA")["DIOXIDO_DE_CARBONO_GGCO2"]
        .sum()
        .reset_index()
    )

    if not df_co2.empty:
        fig_co2 = px.pie(
            df_co2,
            names="SUBCATEGORIA",
            values="DIOXIDO_DE_CARBONO_GGCO2",
            title=f"Participación porcentual de CO₂ - Año {anio_co2}",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.YlOrRd_r
        )

        fig_co2.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )
        
        fig_co2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_co2, use_container_width=True)
    else:
        st.warning("No existen datos para el año seleccionado.")

# ==================================================
# TAB 3 - METANO
# ==================================================
with tab3:
    st.header("🦠 Porcentaje de emisiones de Metano (GGCH₄)")

    anio_metano = st.selectbox(
        "Seleccione un año de análisis para CH₄:",
        lista_anios,
        key="metano"
    )

    df_metano = (
        df[df["ANIO"] == anio_metano]
        .groupby("SUBCATEGORIA")["METANO_GGCH4"]
        .sum()
        .reset_index()
    )

    if not df_metano.empty:
        fig_metano = px.pie(
            df_metano,
            names="SUBCATEGORIA",
            values="METANO_GGCH4",
            title=f"Participación porcentual de Metano - Año {anio_metano}",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        fig_metano.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_metano.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_metano, use_container_width=True)
    else:
        st.warning("No existen datos para el año seleccionado.")

# ==================================================
# TAB 4 - METANO EQUIVALENTE
# ==================================================
with tab4:
    st.header("🔄 Porcentaje de emisiones de Metano Equivalente")

    anio_equiv = st.selectbox(
        "Seleccione un año de análisis equivalente:",
        lista_anios,
        key="metano_equivalente"
    )

    df_equiv = (
        df[df["ANIO"] == anio_equiv]
        .groupby("SUBCATEGORIA")["METANO_EQUIVALENTE_GGCO2EQ"]
        .sum()
        .reset_index()
    )

    if not df_equiv.empty:
        fig_equiv = px.pie(
            df_equiv,
            names="SUBCATEGORIA",
            values="METANO_EQUIVALENTE_GGCO2EQ",
            hole=0.35,
            title=f"Porcentaje de emisiones de Metano Equivalente - Año {anio_equiv}",
            color_discrete_sequence=px.colors.sequential.Purples_r
        )

        fig_equiv.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_equiv.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_equiv, use_container_width=True)
    else:
        st.warning("No existen datos para el año seleccionado.")

# ==================================================
# TAB 5 - ÓXIDO NITROSO
# ==================================================
with tab5:
    st.header("🧪 Porcentaje de emisiones de Óxido Nitroso (N₂O)")

    anio_n2o = st.selectbox(
        "Seleccione un año de análisis para N₂O:",
        lista_anios,
        key="n2o"
    )

    df_n2o = (
        df[df["ANIO"] == anio_n2o]
        .groupby("SUBCATEGORIA")["OXIDO_NITROSO_GGN2O"]
        .sum()
        .reset_index()
    )

    if not df_n2o.empty:
        fig_n2o = px.pie(
            df_n2o,
            names="SUBCATEGORIA",
            values="OXIDO_NITROSO_GGN2O",
            hole=0.35,
            title=f"Porcentaje de emisiones de Óxido Nitroso - Año {anio_n2o}",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )

        fig_n2o.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig_n2o.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_n2o, use_container_width=True)
    else:
        st.warning("No existen datos para el año seleccionado.")
