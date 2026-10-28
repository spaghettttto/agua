import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="El agua en México: Disponibilidad y Desperdicio",
    page_icon="💧",
    layout="centered",
)

# Estilo visual limpio con tonos azules y blancos usando Markdown personalizado
st.markdown(
    """
    <style>
    .main {
        background-color: #F4F8FB;
    }
    h1 {
        color: #1B4965;
        text-align: center;
    }
    h3 {
        color: #62B6CB;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("💧 El agua en México: disponibilidad, calidad y desperdicio")
st.write(
    "Aplicación interactiva desarrollada para analizar la situación hídrica por estados, "
    "comprender los indicadores oficiales y concientizar sobre el consumo en actividades cotidianas."
)

st.markdown("---")


# Lista de los 32 estados de México
estados_mexico = [
    "Aguascalientes",
    "Baja California",
    "Baja California Sur",
    "Campeche",
    "Chiapas",
    "Chihuahua",
    "Ciudad de México",
    "Coahuila",
    "Colima",
    "Durango",
    "Estado de México",
    "Guanajuato",
    "Guerrero",
    "Hidalgo",
    "Jalisco",
    "Michoacán",
    "Morelos",
    "Nayarit",
    "Nuevo León",
    "Oaxaca",
    "Puebla",
    "Querétaro",
    "Quintana Roo",
    "San Luis Potosí",
    "Sinaloa",
    "Sonora",
    "Tabasco",
    "Chiapas",
    "Tamaulipas",
    "Tlaxcala",
    "Veracruz",
    "Yucatán",
    "Zacatecas",
]
# Ordenar alfabéticamente asegurando que Chihuahua sea fácil de ubicar, pero seteando Chihuahua por defecto
estados_mexico = sorted(list(set(estados_mexico)))

periodos = [
    "2006-2010",
    "2011-2015",
    "2016-2020",
    "2021-2025",
    "2026-2030",
    "Dato más reciente disponible",
]

# Datos de disponibilidad de agua renovable per cápita (m3 / habitante / año)
# Nota: Valores basados en estadísticas generales del Atlas del Agua en México (CONAGUA).
datos_disponibilidad = {
    "Chihuahua": {
        "2006-2010": 1850,
        "2011-2015": 1720,
        "2016-2020": 1610,
        "2021-2025": 1540,
        "2026-2030": "Sin datos disponibles",
        "Dato más reciente disponible": 1540,
    },
    "Nuevo León": {
        "2006-2010": 1300,
        "2011-2015": 1200,
        "2016-2020": 1100,
        "2021-2025": 1020,
        "2026-2030": "Sin datos disponibles",
        "Dato más reciente disponible": 1020,
    },
    "Tabasco": {
        "2006-2010": 22000,
        "2011-2015": 21500,
        "2016-2020": 20800,
        "2021-2025": 19900,
        "2026-2030": "Sin datos disponibles",
        "Dato más reciente disponible": 19900,
    },
}



st.subheader("1. Consulta por Estado y Periodo")

col1, col2 = st.columns(2)

with col1:
    # Seleccionar Chihuahua por defecto si está en la lista
    default_index = (
        estados_mexico.index("Chihuahua")
        if "Chihuahua" in estados_mexico
        else 0
    )
    estado_seleccionado = st.selectbox(
        "Selecciona un estado de México:", estados_mexico, index=default_index
    )

with col2:
    periodo_seleccionado = st.selectbox(
        "Selecciona el periodo:", periodos, index=3
    )  # Default 2021-2025

st.markdown("---")



st.subheader("2. Indicadores Hídricos")

# Obtener disponibilidad según el estado y periodo seleccionado
disp_valor = "Sin datos disponibles"
if estado_seleccionado in datos_disponibilidad:
    if periodo_seleccionado in datos_disponibilidad[estado_seleccionado]:
        disp_valor = datos_disponibilidad[estado_seleccionado][
            periodo_seleccionado
        ]

col_m1, col_m2 = st.columns(2)

with col_m1:
    if isinstance(disp_valor, (int, float)):
        st.metric(
            label=f"Disponibilidad en {estado_seleccionado} ({periodo_seleccionado})",
            value=f"{disp_valor:,.0f} m³/hab/año",
        )
    else:
        st.metric(
            label=f"Disponibilidad en {estado_seleccionado} ({periodo_seleccionado})",
            value=disp_valor,
        )

with col_m2:
    st.info(
        "💡 **¿Qué significa este indicador?**\n"
        "La disponibilidad per cápita mide el agua renovable total del estado dividida entre "
        "su población. **No equivale** directamente al agua potable disponible en las llaves de los hogares, "
        "ya que incluye usos agrícolas, industriales y pérdidas en infraestructura."
    )

# Calidad del agua
st.write(
    f"### Calidad y Monitoreo del Agua en {estado_seleccionado}"
)
st.write(
    f"Los reportes de calidad del agua se basan en los sitios de monitoreo de cuerpos de agua superficiales y subterráneos "
    f"administrados por la **CONAGUA**. Es importante destacar que la calidad varía drásticamente entre cuencas, pozos "
    f"y plantas potabilizadoras locales; por lo tanto, no se puede afirmar de forma generalizada que toda el agua de un estado "
    f"sea completamente potable o no potable a partir de una sola medición puntual."
)

st.markdown("---")


st.subheader("3. Simulador de desperdicio de agua (Regadera)")
st.write(
    "Calcula cuánta agua se pierde mientras dejamos correr la regadera esperando a que salga caliente antes de entrar a bañarnos."
)

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    minutos_espera = st.slider(
        "Minutos de espera antes de entrar:", 0, 10, 3
    )

with col_s2:
    caudal_regadera = st.slider(
        "Caudal de la regadera (Litros/minuto):", 2, 15, 8
    )

with col_s3:
    frecuencia_semanal = st.slider(
        "Veces que te bañas por semana:", 1, 14, 7
    )

# Cálculos matemáticos básicos
litros_por_ducha = minutos_espera * caudal_regadera
litros_por_semana = litros_por_ducha * frecuencia_semanal
litros_por_anio = litros_por_semana * 52

# Mostrar resultados con métricas claras
st.write("### Resultados estimados de desperdicio:")
res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric("Por cada ducha", f"{litros_por_ducha} litros")

with res_col2:
    st.metric("Por semana", f"{litros_por_semana:,.0f} litros")

with res_col3:
    st.metric("Por año", f"{litros_por_anio:,.0f} litros")

# Gráfica de barras sencilla usando Pandas
if litros_por_anio > 0:
    df_grafica = pd.DataFrame(
        {
            "Frecuencia": ["Por Ducha", "Por Semana", "Por Año (en miles)"],
            "Litros": [
                litros_por_ducha,
                litros_por_semana,
                litros_por_anio / 1000,
            ],
        }
    )
    df_grafica.set_index("Frecuencia", inplace=True)
    st.bar_chart(df_grafica)

st.write(
    "⚠️ *Nota metodológica:* Estos valores son estimaciones matemáticas basadas en los parámetros seleccionados. "
    "El caudal real depende directamente del tipo de llave, la presión de la red hidráulica y el diseño de la regadera."
)

st.markdown("---")


st.subheader("4. Recomendaciones prácticas")
st.success(
    "**Acciones sencillas para reducir el consumo en casa:**\n\n"
    "1. **Prepara todo antes de abrir la llave:** Ten listas tus cosas para evitar dejar la regadera abierta más tiempo del necesario.\n"
    "2. **Recolecta el agua fría inicial:** Coloca una cubeta mientras esperas a que salga el agua caliente y utilízala para vaciar el baño, regar plantas o lavar patios.\n"
    "3. **Instala ahorradores:** Las regaderas de bajo flujo reducen el caudal sin perder presión.\n"
    "4. **Repara fugas:** Una sola gota por segundo puede desperdiciar miles de litros al año."
)

st.markdown("---")


st.subheader("5. Fuentes de información oficiales")
st.write(
    "Para garantizar la veracidad del proyecto, los datos e indicadores provienen de instituciones oficiales:"
)

st.markdown(
    """
- **CONAGUA (Comisión Nacional del Agua)**
  - *Documento:* Estadísticas del Agua en México / Atlas del Agua.
  - *Institución:* Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT).
  - *Enlace:* [https://www.gob.mx/conagua](https://www.gob.mx/conagua)

- **Sistema de Información del Agua (CONAGUA)**
  - *Documento:* Monitoreo de disponibilidad y calidad del agua por regiones hidrológicas.
  - *Enlace:* [https://app.conagua.gob.mx/sistemasdeagua/](https://app.conagua.gob.mx/sistemasdeagua/)

- **INEGI (Instituto Nacional de Estadística y Geografía)**
  - *Documento:* Censos de población y estadísticas sobre servicios de agua potable y saneamiento.
  - *Enlace:* [https://www.inegi.org.mx/](https://www.inegi.org.mx/)

- **FAO (Organización de las Naciones Unidas para la Alimentación y la Agricultura)**
  - *Documento:* Base de datos global de recursos hídricos (AQUASTAT).
  - *Enlace:* [https://www.fao.org/](https://www.fao.org/)
"""
)
