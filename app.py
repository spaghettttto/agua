import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="El agua en México: Disponibilidad y Desperdicio 💧",
    page_icon="💧",
    layout="centered"
)

st.markdown("""
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
/* Estilos para el Centro de Juegos Hídricos */
.main-header {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 20px;
    border: 2px solid #90CAF9;
    text-align: center;
    box-shadow: 0 4px 14px rgba(33, 150, 243, 0.12);
    margin-bottom: 25px;
}
.main-title {
    color: #0277BD !important;
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
}
.main-subtitle {
    color: #4FC3F7;
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("💧 El agua en México: disponibilidad, calidad y desperdicio")

st.write(
    "Aplicación interactiva desarrollada para analizar la situación "
    "hídrica por estados, comprender los indicadores oficiales y "
    "concientizar sobre el consumo en actividades cotidianas."
)

# =====================================================
# 1. DATOS DE LOS ESTADOS
# =====================================================

estados_mexico = sorted([
    "Aguascalientes", "Baja California", "Baja California Sur",
    "Campeche", "Chiapas", "Chihuahua", "Ciudad de México",
    "Coahuila", "Colima", "Durango", "Estado de México",
    "Guanajuato", "Guerrero", "Hidalgo", "Jalisco",
    "Michoacán", "Morelos", "Nayarit", "Nuevo León",
    "Oaxaca", "Puebla", "Querétaro", "Quintana Roo",
    "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco",
    "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán",
    "Zacatecas"
])

periodos = [
    "2006-2010",
    "2011-2015",
    "2016-2020",
    "2021-2025",
    "2026-2030",
    "Dato más reciente disponible"
]

# =====================================================
# 2. DISPONIBILIDAD DE AGUA
# =====================================================

datos_disponibilidad = {
    "Aguascalientes": [420, 390, 360, 340],
    "Baja California": [980, 920, 870, 810],
    "Baja California Sur": [780, 730, 690, 650],
    "Campeche": [18500, 18000, 17500, 16900],
    "Chiapas": [24000, 23200, 22500, 21800],
    "Chihuahua": [1850, 1720, 1610, 1540],
    "Ciudad de México": [160, 150, 140, 130],
    "Coahuila": [1450, 1380, 1310, 1250],
    "Colima": [3200, 3050, 2900, 2780],
    "Durango": [3100, 2950, 2800, 2680],
    "Estado de México": [260, 240, 220, 210],
    "Guanajuato": [680, 630, 590, 550],
    "Guerrero": [5800, 5500, 5200, 4950],
    "Hidalgo": [1950, 1850, 1750, 1680],
    "Jalisco": [1550, 1470, 1390, 1320],
    "Michoacán": [2900, 2750, 2600, 2480],
    "Morelos": [1150, 1080, 1020, 970],
    "Nayarit": [7800, 7400, 7000, 6650],
    "Nuevo León": [1300, 1200, 1100, 1020],
    "Oaxaca": [8500, 8100, 7700, 7300],
    "Puebla": [950, 890, 840, 790],
    "Querétaro": [820, 770, 720, 680],
    "Quintana Roo": [12500, 11800, 11100, 10500],
    "San Luis Potosí": [1650, 1560, 1480, 1400],
    "Sinaloa": [5200, 4900, 4600, 4350],
    "Sonora": [2800, 2650, 2500, 2380],
    "Tabasco": [22000, 21500, 20800, 19900],
    "Tamaulipas": [2100, 1980, 1870, 1780],
    "Tlaxcala": [510, 480, 450, 420],
    "Veracruz": [11500, 10900, 10300, 9800],
    "Yucatán": [9200, 8700, 8200, 7800],
    "Zacatecas": [1250, 1180, 1110, 1050]
}

# =====================================================
# 3. COBERTURA Y POTABILIDAD
# =====================================================

datos_cobertura_potable = {
    "Aguascalientes": (98.8, "Buena (Tratamiento constante)"),
    "Baja California": (97.5, "Aceptable / Alta salinidad en zonas"),
    "Baja California Sur": (95.2, "Moderada (Presencia de minerales)"),
    "Campeche": (89.4, "Aceptable"),
    "Chiapas": (88.8, "Baja en zonas rurales (Riesgo biológico)"),
    "Chihuahua": (98.1, "Buena (Monitoreo continuo de arsénico)"),
    "Ciudad de México": (98.6, "Variable según alcaldía / Red antigua"),
    "Coahuila": (98.4, "Aceptable"),
    "Colima": (99.0, "Buena"),
    "Durango": (96.5, "Moderada (Presencia de flúor en acuíferos)"),
    "Estado de México": (96.2, "Variable / Presión intermitente"),
    "Guanajuato": (96.8, "Moderada (Tratamiento por metales en pozos)"),
    "Guerrero": (87.1, "Baja (Deficiencia en cloración municipal)"),
    "Hidalgo": (94.3, "Aceptable"),
    "Jalisco": (97.8, "Buena en ZMM / Variable en zonas agrícolas"),
    "Michoacán": (94.6, "Aceptable"),
    "Morelos": (96.9, "Buena"),
    "Nayarit": (95.1, "Aceptable"),
    "Nuevo León": (98.9, "Alta (Red automatizada y potabilizada)"),
    "Oaxaca": (85.5, "Baja en zonas rurales (Falta de potabilizadoras)"),
    "Puebla": (94.8, "Aceptable / Vulnerable en cuencas urbanas"),
    "Querétaro": (97.3, "Buena"),
    "Quintana Roo": (97.1, "Aceptable (Monitoreo de dureza y karst)"),
    "San Luis Potosí": (94.2, "Moderada"),
    "Sinaloa": (96.7, "Aceptable"),
    "Sonora": (97.6, "Moderada (Tratamiento en acuíferos del norte)"),
    "Tabasco": (88.2, "Moderada (Alta turbiedad en ríos)"),
    "Tamaulipas": (96.1, "Aceptable"),
    "Tlaxcala": (97.9, "Aceptable"),
    "Veracruz": (89.7, "Variable (Vulnerable a eventos meteorológicos)"),
    "Yucatán": (96.8, "Moderada (Agua dura / Acuífero somero)"),
    "Zacatecas": (96.3, "Moderada")
}

datos_consumo_agua = {
    "Aguascalientes": 680, "Baja California": 2950, "Baja California Sur": 480,
    "Campeche": 510, "Chiapas": 2400, "Chihuahua": 5150,
    "Ciudad de México": 1150, "Coahuila": 2350, "Colima": 1520,
    "Durango": 2100, "Estado de México": 2450, "Guanajuato": 4450,
    "Guerrero": 1350, "Hidalgo": 2650, "Jalisco": 4850,
    "Michoacán": 5400, "Morelos": 1320, "Nayarit": 1680,
    "Nuevo León": 2150, "Oaxaca": 1580, "Puebla": 2250,
    "Querétaro": 1050, "Quintana Roo": 790, "San Luis Potosí": 1540,
    "Sinaloa": 9850, "Sonora": 7200, "Tabasco": 690,
    "Tamaulipas": 4300, "Tlaxcala": 360, "Veracruz": 5600,
    "Yucatán": 1480, "Zacatecas": 1750
}

# =====================================================
# PESTAÑAS PRINCIPALES
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Situación por Estado",
    "🚿 Simulador y Ahorro",
    "🎮 Interactivos",
    "📚 Fuentes"
])

# =====================================================
# TAB 1: CONSULTA POR ESTADO Y MAPA
# =====================================================
with tab1:
    st.subheader("1. Consulta por Estado y Periodo")

    col1, col2 = st.columns(2)

    with col1:
        estado_seleccionado = st.selectbox(
            "Selecciona un estado de México:",
            estados_mexico,
            index=estados_mexico.index("Chihuahua")
        )

    with col2:
        periodo_seleccionado = st.selectbox(
            "Selecciona el periodo:",
            periodos,
            index=3
        )

    st.subheader("2. Indicadores Hídricos y Potabilidad")

    indice_periodo = periodos.index(periodo_seleccionado)

    if indice_periodo < 4:
        disp_valor = datos_disponibilidad[estado_seleccionado][indice_periodo]
    elif indice_periodo == 5:
        disp_valor = datos_disponibilidad[estado_seleccionado][3]
    else:
        disp_valor = "Sin datos disponibles"

    cobertura, potabilidad = datos_cobertura_potable[estado_seleccionado]

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        if isinstance(disp_valor, (int, float)):
            st.metric(
                f"Disponibilidad per cápita ({periodo_seleccionado})",
                f"{disp_valor:,.0f} m³/hab/año"
            )
        else:
            st.metric("Disponibilidad per cápita", disp_valor)

    with col_m2:
        st.metric("Cobertura de Agua Entubada", f"{cobertura}%")

    with col_m3:
        st.metric("Calidad / Potabilidad General", potabilidad)

    st.info("""
    💡 **¿Qué significan estos indicadores?**

    - **Disponibilidad:** Mide el agua renovable total del estado dividida entre su población.
    - **Cobertura:** Porcentaje de hogares conectados a la red pública de agua entubada.
    - **Potabilidad:** Diagnóstico regional sobre la aptitud del agua para uso doméstico y los retos de tratamiento local.
    """)

    st.markdown("---")
    st.subheader("🗺️ Mapa de Consumo Total de Agua por Estado")

    st.write(
        "Visualización geográfica del volumen anual de agua concesionada/consumida "
        "(incluye uso agrícola, público e industrial en millones de m³)."
    )

    df_mapa = pd.DataFrame({
        "Estado": list(datos_consumo_agua.keys()),
        "Consumo_Mm3": list(datos_consumo_agua.values())
    })

    url_geojson = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
    mapa_mexico = alt.Data(
        url=url_geojson,
        format=alt.DataFormat(property="features", type="json")
    )

    fig_mapa = alt.Chart(mapa_mexico).mark_geoshape(
        stroke="white",
        strokeWidth=0.8
    ).encode(
        color=alt.Color(
            "Consumo_Mm3:Q",
            scale=alt.Scale(scheme="blues"),
            title="Consumo (Mm³/año)"
        ),
        tooltip=[
            alt.Tooltip("properties.name:N", title="Estado"),
            alt.Tooltip("Consumo_Mm3:Q", title="Consumo (Mm³/año)", format=",.0f")
        ]
    ).transform_lookup(
        lookup="properties.name",
        from_=alt.LookupData(df_mapa, "Estado", ["Consumo_Mm3"])
    ).project(
        type="mercator"
    ).properties(
        width=650,
        height=420
    ).configure_view(
        strokeWidth=0
    ).configure(
        background="#F4F8FB"
    )

    st.altair_chart(fig_mapa, use_container_width=True)

    estado_max = df_mapa.loc[df_mapa["Consumo_Mm3"].idxmax()]
    consumo_sel = datos_consumo_agua.get(estado_seleccionado, 0)

    st.warning(
        f"📊 **Mayor consumidor a nivel nacional:** **{estado_max['Estado']}** con aproximadamente "
        f"**{estado_max['Consumo_Mm3']:,.0f} millones de m³ al año** (impulsado principalmente por su alta actividad agrícola).\n\n"
        f"📍 **Estado seleccionado ({estado_seleccionado}):** Consume aproximadamente **{consumo_sel:,.0f} millones de m³ al año**."
    )

# =====================================================
# TAB 2: SIMULADOR DE DESPERDICIO Y RETO DE AHORRO
# =====================================================
with tab2:
    st.subheader("3. Simulador de desperdicio en botellas de agua (500 ml)")

    st.write(
        "Calcula cuántas botellas de 500 ml y cuánto dinero equivaldría "
        "el agua que se desperdicia mientras esperas a que salga caliente "
        "en la regadera."
    )

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        minutos_espera = st.slider("Minutos de espera:", 0, 10, 3)

    with col_s2:
        caudal_regadera = st.slider("Caudal (Litros/min):", 2, 15, 8)

    with col_s3:
        frecuencia_semanal = st.slider("Duchas por semana:", 1, 14, 7)

    with col_s4:
        costo_botella = st.number_input(
            "Precio por botella de 500 ml ($ MXN):",
            value=15.0,
            step=1.0
        )

    litros_ducha = minutos_espera * caudal_regadera
    litros_semana = litros_ducha * frecuencia_semanal
    litros_mes = litros_semana * 4.33
    litros_anio = litros_semana * 52

    botellas_ducha = litros_ducha * 2
    botellas_semana = litros_semana * 2
    botellas_mes = litros_mes * 2
    botellas_anio = litros_anio * 2

    costo_ducha = botellas_ducha * costo_botella
    costo_semana = botellas_semana * costo_botella
    costo_mes = botellas_mes * costo_botella
    costo_anio = botellas_anio * costo_botella

    st.write("### 🫗 Impacto económico y volumen desperdiciado")

    res_col1, res_col2, res_col3, res_col4 = st.columns(4)

    with res_col1:
        st.metric(
            "Por ducha",
            f"${costo_ducha:,.2f} MXN",
            f"{int(botellas_ducha):,} botellas"
        )

    with res_col2:
        st.metric(
            "Por semana",
            f"${costo_semana:,.2f} MXN",
            f"{int(botellas_semana):,} botellas"
        )

    with res_col3:
        st.metric(
            "Por mes",
            f"${costo_mes:,.2f} MXN",
            f"{int(botellas_mes):,} botellas"
        )

    with res_col4:
        st.metric(
            "Por año",
            f"${costo_anio:,.2f} MXN",
            f"{int(botellas_anio):,} botellas"
        )

    if botellas_anio > 0:
        df_grafica = pd.DataFrame({
            "Periodo": ["Por ducha", "Por semana", "Por mes", "Por año"],
            "Costo_MXN": [
                costo_ducha,
                costo_semana,
                costo_mes,
                costo_anio
            ],
            "Botellas": [
                botellas_ducha,
                botellas_semana,
                botellas_mes,
                botellas_anio
            ]
        })

        st.markdown("### 📊 Comparación del desperdicio")
        st.caption(
            "Costo equivalente del agua desperdiciada según el periodo."
        )

        chart = alt.Chart(df_grafica).mark_bar(
            cornerRadiusEnd=8,
            height=28,
            color="#62B6CB"
        ).encode(
            x=alt.X(
                "Costo_MXN:Q",
                scale=alt.Scale(type="symlog"),
                axis=alt.Axis(
                    title="Costo equivalente (MXN)",
                    grid=True,
                    format="$,.0f"
                )
            ),
            y=alt.Y(
                "Periodo:N",
                sort=["Por ducha", "Por semana", "Por mes", "Por año"],
                axis=alt.Axis(
                    title=None,
                    labelFontSize=12
                )
            ),
            tooltip=[
                alt.Tooltip("Periodo:N", title="Periodo"),
                alt.Tooltip(
                    "Costo_MXN:Q",
                    title="Costo",
                    format="$,.2f"
                ),
                alt.Tooltip(
                    "Botellas:Q",
                    title="Botellas de 500 ml",
                    format=",.0f"
                )
            ]
        ).properties(
            height=190
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            gridColor="#E5EDF2",
            domain=False,
            tickColor="#E5EDF2"
        ).configure(
            background="#F4F8FB"
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

    st.caption(
        "Nota metodológica: cada litro equivale a dos botellas de 500 ml. "
        "El costo es una equivalencia ilustrativa, no una pérdida monetaria real."
    )

    st.subheader("4. Recomendaciones prácticas")

    st.success("""
    **Acciones sencillas para reducir el consumo en casa:**

    1. **Prepara todo antes de abrir la llave:** Ten listas tus cosas para evitar dejar la regadera abierta.
    2. **Recolecta el agua fría inicial:** Coloca una cubeta mientras esperas el agua caliente y reutilízala en otras tareas.
    3. **Instala ahorradores:** Las regaderas de bajo flujo pueden reducir el consumo.
    4. **Repara fugas:** Evita que el agua se pierda continuamente.
    """)

    st.markdown("---")
    st.subheader("5. 💧 Reto interactivo: ¿cuánta agua puedes ahorrar?")

    st.write(
        "Personaliza tus hábitos y descubre cuántos litros de agua "
        "podrías ahorrar al reducir el tiempo de ducha."
    )

    st.markdown("#### 🌱 Personaliza tu reto")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        minutos_reducidos = st.slider(
            "¿Cuántos minutos menos duraría tu ducha?",
            0, 10, 2,
            key="minutos_reto"
        )

        caudal_reto = st.slider(
            "Caudal de tu regadera (litros/minuto):",
            2, 15, 8,
            key="caudal_reto"
        )

    with col_r2:
        dias_reto = st.slider(
            "¿Cuántos días por semana aplicarías el cambio?",
            1, 7, 7,
            key="dias_reto"
        )

        personas = st.number_input(
            "¿Cuántas personas participarían?",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

    litros_ahorrados_dia = (
        minutos_reducidos * caudal_reto * personas
    )

    litros_ahorrados_semana = (
        litros_ahorrados_dia * dias_reto
    )

    litros_ahorrados_mes = litros_ahorrados_semana * 4.33

    st.markdown("#### 📊 Tu ahorro estimado")

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "En un día",
        f"{litros_ahorrados_dia:,.1f} L"
    )

    m2.metric(
        "En una semana",
        f"{litros_ahorrados_semana:,.1f} L"
    )

    m3.metric(
        "En un mes",
        f"{litros_ahorrados_mes:,.1f} L"
    )

    st.progress(
        min(litros_ahorrados_semana / 500, 1.0)
    )

    st.caption(
        "La barra alcanza el 100 % al llegar a 500 litros de ahorro semanal."
    )

    with st.expander("🧮 ¿Cómo se calcula?"):
        st.write(
            "Litros ahorrados = minutos reducidos × caudal de la regadera "
            "× personas × días de aplicación."
        )

        st.latex(
            r"\text{Ahorro semanal} = "
            r"\text{minutos} \times "
            r"\text{litros/minuto} \times "
            r"\text{personas} \times \text{días}"
        )

# =====================================================
# TAB 3: INTERACTIVOS (CENTRO DE JUEGOS HÍDRICOS)
# =====================================================
with tab3:
    if "juego_activo" not in st.session_state:
        st.session_state.juego_activo = "menu"

    # --- VISTA: MENÚ PRINCIPAL ---
    if st.session_state.juego_activo == "menu":
        st.markdown("""
            <div class="main-header">
                <h2 class="main-title">💧 Centro de Juegos Hídricos</h2>
                <p class="main-subtitle">Elige un minijuego interactivo para aprender sobre el agua y el medio ambiente</p>
            </div>
        """, unsafe_allow_html=True)

        col_j1, col_j2, col_j3 = st.columns(3, gap="medium")

        with col_j1:
            st.markdown("""
                <div style="background: #FFFFFF; border: 2.5px solid #81D4FA; border-radius: 18px; padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 42px; margin-bottom: 6px;">💧</div>
                        <h3 style="color: #01579B; margin: 0 0 8px 0; font-size: 18px;">AquaPou</h3>
                        <p style="color: #0277BD; font-size: 13px; line-height: 1.35;">
                            Atrapa agua limpia y esquiva industrias contaminantes.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🎮", key="btn_pou", use_container_width=True):
                st.session_state.juego_activo = "pou"
                st.rerun()

        with col_j2:
            st.markdown("""
                <div style="background: #FFFFFF; border: 2.5px solid #81D4FA; border-radius: 18px; padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 42px; margin-bottom: 6px;">🚰</div>
                        <h3 style="color: #01579B; margin: 0 0 8px 0; font-size: 18px;">Cierra la Llave</h3>
                        <p style="color: #0277BD; font-size: 13px; line-height: 1.35;">
                            Detén fugas y desperdicios domésticos a contratiempo.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🎮", key="btn_llave", use_container_width=True):
                st.session_state.juego_activo = "llave"
                st.rerun()

        with col_j3:
            st.markdown("""
                <div style="background: #FFFFFF; border: 2.5px solid #81D4FA; border-radius: 18px; padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 42px; margin-bottom: 6px;">🌱</div>
                        <h3 style="color: #01579B; margin: 0 0 8px 0; font-size: 18px;">Rescata el Río</h3>
                        <p style="color: #0277BD; font-size: 13px; line-height: 1.35;">
                            Limpia los desechos flotantes antes de que contaminen el río.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🎮", key="btn_rio", use_container_width=True):
                st.session_state.juego_activo = "rio"
                st.rerun()

    # --- VISTA: JUEGO 1 (AQUAPOU) ---
    elif st.session_state.juego_activo == "pou":
        if st.button("⬅️ Volver al menú de juegos"):
            st.session_state.juego_activo = "menu"
            st.rerun()
        
        st.markdown("### 💧 AquaPou: ¡Alimenta la Gota!")
        
        pou_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
            body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
            #game-wrapper {
                position: relative; width: 520px; height: 540px; border-radius: 20px; overflow: hidden;
                border: 3px solid #64B5F6; background: linear-gradient(180deg, #E1F5FE 0%, #B3E5FC 65%, #FFFFFF 100%);
                box-shadow: 0 8px 20px rgba(2, 119, 189, 0.15);
            }
            canvas { display: block; width: 100%; height: 100%; cursor: none; }
            #hud { position: absolute; top: 15px; left: 20px; right: 20px; display: flex; justify-content: space-between; pointer-events: none; }
            .badge { background: rgba(255, 255, 255, 0.9); color: #0277BD; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 15px; border: 2px solid #81D4FA; }
            .overlay {
                position: absolute; inset: 0; background: rgba(255, 255, 255, 0.93);
                display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 25px; text-align: center; z-index: 10;
            }
            .hidden { display: none !important; }
            .fact-card {
                background: #E3F2FD; border: 2px solid #42A5F5; border-radius: 14px; padding: 14px; margin: 12px 0 18px 0; color: #0D47A1; text-align: left;
            }
            .fact-card h3 { margin: 0 0 6px 0; color: #D32F2F; font-size: 17px; }
            .fact-card p { margin: 4px 0; font-size: 14px; line-height: 1.4; }
            .btn {
                background: linear-gradient(135deg, #29B6F6, #0288D1); color: white; border: none;
                padding: 10px 24px; font-size: 16px; font-weight: bold; border-radius: 25px; cursor: pointer;
            }
        </style>
        </head>
        <body>
        <div id="game-wrapper">
            <div id="hud">
                <div class="badge">💧 Puntos: <span id="score">0</span></div>
                <div class="badge">🏆 Récord: <span id="highscore">0</span></div>
            </div>
            <canvas id="gameCanvas" width="520" height="540"></canvas>
            <div id="start-screen" class="overlay">
                <div style="font-size: 54px; margin-bottom: 8px;">💧</div>
                <h2 style="color: #01579B; margin: 0 0 8px 0;">¡Alimenta a AquaPou!</h2>
                <p style="color: #0277BD; font-size: 15px; margin-bottom: 18px;">Atrapa agua limpia y evita las industrias contaminantes.</p>
                <button class="btn" onclick="startGame()">¡Empezar a jugar!</button>
            </div>
            <div id="gameover-screen" class="overlay hidden">
                <div style="font-size: 46px;">😵‍💫💦</div>
                <h2 style="color: #C62828; margin: 4px 0;">¡AquaPou se contaminó!</h2>
                <p style="color: #0277BD; font-weight: bold; margin: 0 0 10px 0;">Puntaje: <span id="final-score">0</span> pts</p>
                <div class="fact-card">
                    <h3 id="fact-title">⚠️ Impacto</h3>
                    <p id="fact-water"></p>
                    <p id="fact-country"></p>
                </div>
                <button class="btn" onclick="startGame()">Volver a intentar</button>
            </div>
        </div>
        <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        let gameRunning = false, score = 0, highScore = 0, items = [], spawnTimer = 0, speedMultiplier = 1;
        const pou = { x: canvas.width / 2, y: canvas.height - 60, radius: 36, speed: 8 };
        let keys = { ArrowLeft: false, ArrowRight: false };
        window.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft" || e.key === "ArrowRight") keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { if (e.key === "ArrowLeft" || e.key === "ArrowRight") keys[e.key] = false; });
        canvas.addEventListener("mousemove", (e) => {
            if (!gameRunning) return;
            const rect = canvas.getBoundingClientRect();
            pou.x = Math.max(pou.radius, Math.min(canvas.width - pou.radius, e.clientX - rect.left));
        });
        const GOOD_ITEMS = [{ emoji: "💧", name: "Gota", points: 10 }, { emoji: "🧴", name: "Botella", points: 15 }];
        const BAD_ITEMS = [
            { emoji: "👕", category: "Industria Textil", waterFact: "Consume <b>93 mil millones de m³ de agua al año</b>; unos jeans requieren 7,500 L.", countryFact: "<b>China e India</b> lideran la contaminación por tintes en ríos." },
            { emoji: "🥩", category: "Ganadería Intensiva", waterFact: "Usa casi el <b>30% del agua dulce mundial</b>; 1 kg de res consume ~15,000 L.", countryFact: "<b>Brasil y EE.UU.</b> concentran la mayor huella hídrica ganadera." },
            { emoji: "🛢️", category: "Industria Petrolera", waterFact: "1 litro de petróleo derramado puede contaminar hasta <b>1 millón de litros de agua</b>.", countryFact: "<b>EE.UU. y Rusia</b> lideran extracción; graves daños en Nigeria." },
            { emoji: "🛍️", category: "Plásticos", waterFact: "Más de <b>8 millones de toneladas</b> llegan a océanos cada año.", countryFact: "<b>Filipinas e India</b> encabezan descargas plásticas en ríos." }
        ];
        function startGame() {
            document.getElementById("start-screen").classList.add("hidden");
            document.getElementById("gameover-screen").classList.add("hidden");
            score = 0; items = []; spawnTimer = 0; speedMultiplier = 1;
            pou.x = canvas.width / 2; document.getElementById("score").innerText = score;
            gameRunning = true; requestAnimationFrame(gameLoop);
        }
        function triggerGameOver(item) {
            gameRunning = false;
            if (score > highScore) { highScore = score; document.getElementById("highscore").innerText = highScore; }
            document.getElementById("final-score").innerText = score;
            document.getElementById("fact-title").innerText = "⚠️ " + item.category;
            document.getElementById("fact-water").innerHTML = "💧 <b>Daño:</b> " + item.waterFact;
            document.getElementById("fact-country").innerHTML = "🌍 <b>Global:</b> " + item.countryFact;
            document.getElementById("gameover-screen").classList.remove("hidden");
        }
        function spawnItem() {
            let isGood = Math.random() < 0.55;
            let template = isGood ? GOOD_ITEMS[Math.floor(Math.random() * GOOD_ITEMS.length)] : BAD_ITEMS[Math.floor(Math.random() * BAD_ITEMS.length)];
            items.push({ x: Math.random() * (canvas.width - 60) + 30, y: -30, radius: 20, speed: (3 + Math.random() * 1.5) * speedMultiplier, isGood, data: template });
        }
        function drawPou() {
            ctx.save(); ctx.translate(pou.x, pou.y);
            ctx.beginPath();
            ctx.moveTo(0, -pou.radius - 10);
            ctx.bezierCurveTo(pou.radius + 10, -4, pou.radius + 6, pou.radius, 0, pou.radius);
            ctx.bezierCurveTo(-pou.radius - 6, pou.radius, -pou.radius - 10, -4, 0, -pou.radius - 10);
            ctx.fillStyle = "#29B6F6"; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = "#0288D1"; ctx.stroke();
            ctx.fillStyle = "white"; ctx.beginPath(); ctx.arc(-10, 3, 7, 0, Math.PI * 2); ctx.arc(10, 3, 7, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#01579B"; ctx.beginPath(); ctx.arc(-9, 3, 3.5, 0, Math.PI * 2); ctx.arc(9, 3, 3.5, 0, Math.PI * 2); ctx.fill();
            ctx.restore();
        }
        function gameLoop() {
            if (!gameRunning) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (keys.ArrowLeft) pou.x = Math.max(pou.radius, pou.x - pou.speed);
            if (keys.ArrowRight) pou.x = Math.min(canvas.width - pou.radius, pou.x + pou.speed);
            spawnTimer++;
            if (spawnTimer >= Math.max(26, Math.floor(50 - score * 0.1))) { spawnItem(); spawnTimer = 0; }
            ctx.font = "32px Arial"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
            for (let i = items.length - 1; i >= 0; i--) {
                let it = items[i]; it.y += it.speed;
                ctx.beginPath(); ctx.arc(it.x, it.y, 20, 0, Math.PI * 2);
                ctx.fillStyle = it.isGood ? "rgba(255,255,255,0.75)" : "rgba(255,235,238,0.85)"; ctx.fill();
                ctx.fillText(it.data.emoji, it.x, it.y + 1);
                if (Math.hypot(it.x - pou.x, it.y - pou.y) < pou.radius + it.radius - 4) {
                    if (it.isGood) { score += it.data.points; speedMultiplier = 1 + (score / 220); document.getElementById("score").innerText = score; items.splice(i, 1); continue; }
                    else { triggerGameOver(it.data); return; }
                }
                if (it.y > canvas.height + 30) items.splice(i, 1);
            }
            drawPou(); requestAnimationFrame(gameLoop);
        }
        </script>
        </body>
        </html>
        """
        components.html(pou_html, height=560)

    # --- VISTA: JUEGO 2 (CIERRA LA LLAVE) ---
    elif st.session_state.juego_activo == "llave":
        if st.button("⬅️ Volver al menú de juegos"):
            st.session_state.juego_activo = "menu"
            st.rerun()

        st.markdown("### 🚰 ¡Cierra la Llave! (Desafío de Ahorro)")

        llave_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; user-select: none; }
            body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
            #container {
                position: relative; width: 520px; background: #FFFFFF; border: 3px solid #64B5F6;
                border-radius: 20px; padding: 18px; box-shadow: 0 8px 20px rgba(2, 119, 189, 0.15);
            }
            #top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
            .stat-pill { background: #E1F5FE; color: #0277BD; padding: 6px 12px; border-radius: 14px; font-weight: 700; font-size: 14px; border: 1.5px solid #81D4FA; }
            #tank-wrapper { width: 100%; height: 20px; background: #ECEFF1; border-radius: 10px; overflow: hidden; border: 2px solid #90CAF9; margin-bottom: 14px; position: relative; }
            #tank-fill { width: 100%; height: 100%; background: linear-gradient(90deg, #4FC3F7, #0288D1); transition: width 0.2s ease; }
            #tank-label { position: absolute; inset: 0; display: flex; justify-content: center; align-items: center; font-size: 11px; font-weight: 800; color: #01579B; }
            #grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
            .pipe-hole {
                height: 105px; background: linear-gradient(180deg, #F0F8FF 0%, #E1F5FE 100%);
                border: 2px solid #B3E5FC; border-radius: 15px; display: flex; flex-direction: column;
                justify-content: center; align-items: center; cursor: pointer; position: relative;
            }
            .pipe-hole.leak { background: #FFF3E0; border-color: #FF9800; }
            .pipe-hole.good { background: #E8F5E9; border-color: #66BB6A; }
            .emoji { font-size: 38px; line-height: 1; }
            .tag { font-size: 10px; font-weight: 700; margin-top: 4px; padding: 2px 6px; border-radius: 6px; }
            .leak .tag { background: #FFE0B2; color: #E65100; }
            .good .tag { background: #C8E6C9; color: #1B5E20; }
            .overlay {
                position: absolute; inset: 0; background: rgba(255, 255, 255, 0.95);
                border-radius: 17px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 24px; text-align: center; z-index: 20;
            }
            .hidden { display: none !important; }
            .info-box { background: #E3F2FD; border: 2px solid #42A5F5; border-radius: 12px; padding: 12px; margin: 10px 0 16px 0; color: #0D47A1; font-size: 13.5px; line-height: 1.4; }
            .btn { background: linear-gradient(135deg, #29B6F6, #0288D1); color: white; border: none; padding: 10px 24px; font-size: 15px; font-weight: bold; border-radius: 25px; cursor: pointer; }
        </style>
        </head>
        <body>
        <div id="container">
            <div id="top-bar">
                <div class="stat-pill">⏱️ Tiempo: <span id="time">30</span>s</div>
                <div class="stat-pill">💧 Salvados: <span id="saved">0</span> L</div>
            </div>
            <div id="tank-wrapper">
                <div id="tank-fill"></div>
                <div id="tank-label">Reserva: <span id="tank-pct">100</span>%</div>
            </div>
            <div id="grid"></div>
            <div id="start-overlay" class="overlay">
                <div style="font-size: 50px; margin-bottom: 6px;">🚰💧</div>
                <h2 style="color: #01579B; margin: 0 0 8px 0;">¡Detén las Fugas!</h2>
                <p style="color: #0277BD; font-size: 14px; margin-bottom: 16px;">Haz clic rápido en las fugas antes de que se vacíe el tanque.</p>
                <button class="btn" onclick="startGame()">Comenzar Reto</button>
            </div>
            <div id="end-overlay" class="overlay hidden">
                <div id="end-emoji" style="font-size: 46px;">🎉💧</div>
                <h2 id="end-title" style="color: #01579B; margin: 4px 0;">¡Terminado!</h2>
                <p style="color: #0277BD; font-weight: 700; font-size: 16px; margin: 4px 0;">Salvaste <span id="final-liters">0</span> litros</p>
                <div class="info-box" id="impact-text"></div>
                <button class="btn" onclick="startGame()">Jugar de nuevo</button>
            </div>
        </div>
        <script>
        const grid = document.getElementById("grid");
        let holes = [], timeLeft = 30, savedLiters = 0, tankLevel = 100, gameActive = false, timerInterval, spawnInterval, drainInterval;
        const EVENTS = [
            { type: "leak", emoji: "🚰", label: "Fuga (+20 L)", liters: 20 },
            { type: "leak", emoji: "🚿", label: "Ducha (+50 L)", liters: 50 },
            { type: "leak", emoji: "💦", label: "Manguera (+80 L)", liters: 80 },
            { type: "good", emoji: "🌧️", label: "¡Lluvia!", liters: 0 },
            { type: "good", emoji: "🌱", label: "¡Goteo!", liters: 0 }
        ];
        for (let i = 0; i < 9; i++) {
            const div = document.createElement("div");
            div.className = "pipe-hole";
            div.innerHTML = `<div class="emoji" style="opacity:0.25;">🔵</div>`;
            div.onclick = () => handleHoleClick(i);
            grid.appendChild(div);
            holes.push({ el: div, active: null, timeout: null });
        }
        function updateTankUI() {
            tankLevel = Math.max(0, Math.min(100, tankLevel));
            document.getElementById("tank-fill").style.width = tankLevel + "%";
            document.getElementById("tank-pct").innerText = Math.round(tankLevel);
            if (tankLevel <= 0 && gameActive) endGame(true);
        }
        function clearHole(i) {
            let h = holes[i];
            if (h.timeout) clearTimeout(h.timeout);
            h.active = null; h.el.className = "pipe-hole";
            h.el.innerHTML = `<div class="emoji" style="opacity:0.25;">🔵</div>`;
        }
        function spawnEvent() {
            if (!gameActive) return;
            let free = holes.map((h, i) => h.active === null ? i : -1).filter(i => i !== -1);
            if (free.length === 0) return;
            let idx = free[Math.floor(Math.random() * free.length)];
            let ev = EVENTS[Math.floor(Math.random() * EVENTS.length)];
            let h = holes[idx];
            h.active = ev; h.el.className = "pipe-hole " + ev.type;
            h.el.innerHTML = `<div class="emoji">${ev.emoji}</div><div class="tag">${ev.label}</div>`;
            h.timeout = setTimeout(() => {
                if (h.active && h.active.type === "leak") { tankLevel -= 6; updateTankUI(); }
                clearHole(idx);
            }, 1400);
        }
        function handleHoleClick(i) {
            if (!gameActive) return;
            let h = holes[i]; if (!h.active) return;
            if (h.active.type === "leak") {
                savedLiters += h.active.liters; tankLevel += 3;
                document.getElementById("saved").innerText = savedLiters; updateTankUI();
            } else {
                timeLeft = Math.max(0, timeLeft - 3);
                document.getElementById("time").innerText = timeLeft;
            }
            clearHole(i);
        }
        function startGame() {
            document.getElementById("start-overlay").classList.add("hidden");
            document.getElementById("end-overlay").classList.add("hidden");
            timeLeft = 30; savedLiters = 0; tankLevel = 100; gameActive = true;
            document.getElementById("time").innerText = timeLeft;
            document.getElementById("saved").innerText = savedLiters;
            updateTankUI(); holes.forEach((_, i) => clearHole(i));
            timerInterval = setInterval(() => { timeLeft--; document.getElementById("time").innerText = timeLeft; if (timeLeft <= 0) endGame(false); }, 1000);
            spawnInterval = setInterval(spawnEvent, 600);
            drainInterval = setInterval(() => {
                let leaks = holes.filter(h => h.active && h.active.type === "leak").length;
                if (leaks > 0) { tankLevel -= leaks * 1.3; updateTankUI(); }
            }, 350);
        }
        function endGame(empty) {
            gameActive = false; clearInterval(timerInterval); clearInterval(spawnInterval); clearInterval(drainInterval);
            holes.forEach((_, i) => clearHole(i));
            document.getElementById("final-liters").innerText = savedLiters;
            let people = Math.floor(savedLiters / 100), days = Math.floor(savedLiters / 2);
            document.getElementById("end-emoji").innerText = empty ? "🏜️⚠️" : "🎉💧";
            document.getElementById("end-title").innerText = empty ? "¡Se agotó el tanque!" : "¡Buen trabajo!";
            document.getElementById("impact-text").innerHTML = `🌍 Con <b>${savedLiters} litros</b> salvados cubres el consumo básico de <b>${people} persona(s)</b> por un día o bebida por <b>${days} días</b>.`;
            document.getElementById("end-overlay").classList.remove("hidden");
        }
        </script>
        </body>
        </html>
        """
        components.html(llave_html, height=520)

    # --- VISTA: JUEGO 3 (RESCATA EL RÍO) ---
    elif st.session_state.juego_activo == "rio":
        if st.button("⬅️ Volver al menú de juegos"):
            st.session_state.juego_activo = "menu"
            st.rerun()

        st.markdown("### 🌱 Rescata el Río (Limpieza y Purificación)")

        rio_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <style>
            * { box-sizing: border-box; font-family: 'Segoe UI', sans-serif; user-select: none; }
            body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
            #container {
                position: relative; width: 520px; background: #FFFFFF; border: 3px solid #64B5F6;
                border-radius: 20px; padding: 18px; box-shadow: 0 8px 20px rgba(2, 119, 189, 0.15);
            }
            #top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
            .stat-pill { background: #E1F5FE; color: #0277BD; padding: 6px 12px; border-radius: 14px; font-weight: 700; font-size: 14px; border: 1.5px solid #81D4FA; }
            #poll-wrapper { width: 100%; height: 20px; background: #ECEFF1; border-radius: 10px; overflow: hidden; border: 2px solid #90CAF9; margin-bottom: 14px; position: relative; }
            #poll-fill { width: 0%; height: 100%; background: linear-gradient(90deg, #66BB6A, #FFA726, #E53935); transition: width 0.2s ease; }
            #poll-label { position: absolute; inset: 0; display: flex; justify-content: center; align-items: center; font-size: 11px; font-weight: 800; color: #01579B; }
            #grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
            .river-cell {
                height: 105px; background: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%);
                border: 2px solid #A5D6A7; border-radius: 15px; display: flex; flex-direction: column;
                justify-content: center; align-items: center; cursor: pointer; position: relative;
            }
            .river-cell.dirty { background: #FFF3E0; border-color: #FFB74D; }
            .emoji { font-size: 38px; line-height: 1; }
            .tag { font-size: 10px; font-weight: 700; margin-top: 4px; padding: 2px 6px; border-radius: 6px; background: #FFE0B2; color: #E65100; }
            .overlay {
                position: absolute; inset: 0; background: rgba(255, 255, 255, 0.95);
                border-radius: 17px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 24px; text-align: center; z-index: 20;
            }
            .hidden { display: none !important; }
            .info-box { background: #E3F2FD; border: 2px solid #42A5F5; border-radius: 12px; padding: 12px; margin: 10px 0 16px 0; color: #0D47A1; font-size: 13.5px; line-height: 1.4; }
            .btn { background: linear-gradient(135deg, #29B6F6, #0288D1); color: white; border: none; padding: 10px 24px; font-size: 15px; font-weight: bold; border-radius: 25px; cursor: pointer; }
        </style>
        </head>
        <body>
        <div id="container">
            <div id="top-bar">
                <div class="stat-pill">⏱️ Tiempo: <span id="time">30</span>s</div>
                <div class="stat-pill">✨ Limpiados: <span id="cleaned">0</span></div>
            </div>
            <div id="poll-wrapper">
                <div id="poll-fill"></div>
                <div id="poll-label">Contaminación del Río: <span id="poll-pct">0</span>%</div>
            </div>
            <div id="grid"></div>
            <div id="start-overlay" class="overlay">
                <div style="font-size: 50px; margin-bottom: 6px;">🌱🌊</div>
                <h2 style="color: #01579B; margin: 0 0 8px 0;">¡Rescata el Río!</h2>
                <p style="color: #0277BD; font-size: 14px; margin-bottom: 16px;">Haz clic en la basura antes de que la contaminación llegue al 100%.</p>
                <button class="btn" onclick="startGame()">Comenzar Limpieza</button>
            </div>
            <div id="end-overlay" class="overlay hidden">
                <div id="end-emoji" style="font-size: 46px;">🌿🐟</div>
                <h2 id="end-title" style="color: #01579B; margin: 4px 0;">¡Río Purificado!</h2>
                <p style="color: #0277BD; font-weight: 700; font-size: 16px; margin: 4px 0;">Limpiaste <span id="final-cleaned">0</span> desechos</p>
                <div class="info-box" id="impact-text"></div>
                <button class="btn" onclick="startGame()">Jugar de nuevo</button>
            </div>
        </div>
        <script>
        const grid = document.getElementById("grid");
        let cells = [], timeLeft = 30, cleanedCount = 0, pollutionLevel = 0, gameActive = false, timerInterval, spawnInterval, pollInterval;
        const TRASH = [
            { emoji: "🛢️", label: "Químicos" },
            { emoji: "🛍️", label: "Plástico" },
            { emoji: "🔋", label: "Batería" },
            { emoji: "🥤", label: "Basura" }
        ];
        for (let i = 0; i < 9; i++) {
            const div = document.createElement("div");
            div.className = "river-cell";
            div.innerHTML = `<div class="emoji" style="opacity:0.3;">💧</div>`;
            div.onclick = () => handleCellClick(i);
            grid.appendChild(div);
            cells.push({ el: div, active: null, timeout: null });
        }
        function updatePollutionUI() {
            pollutionLevel = Math.max(0, Math.min(100, pollutionLevel));
            document.getElementById("poll-fill").style.width = pollutionLevel + "%";
            document.getElementById("poll-pct").innerText = Math.round(pollutionLevel);
            if (pollutionLevel >= 100 && gameActive) endGame(true);
        }
        function clearCell(i) {
            let c = cells[i];
            if (c.timeout) clearTimeout(c.timeout);
            c.active = null; c.el.className = "river-cell";
            c.el.innerHTML = `<div class="emoji" style="opacity:0.3;">💧</div>`;
        }
        function spawnTrash() {
            if (!gameActive) return;
            let free = cells.map((c, i) => c.active === null ? i : -1).filter(i => i !== -1);
            if (free.length === 0) return;
            let idx = free[Math.floor(Math.random() * free.length)];
            let item = TRASH[Math.floor(Math.random() * TRASH.length)];
            let c = cells[idx];
            c.active = item; c.el.className = "river-cell dirty";
            c.el.innerHTML = `<div class="emoji">${item.emoji}</div><div class="tag">${item.label}</div>`;
            c.timeout = setTimeout(() => {
                if (c.active) { pollutionLevel += 12; updatePollutionUI(); }
                clearCell(idx);
            }, 1500);
        }
        function handleCellClick(i) {
            if (!gameActive) return;
            let c = cells[i]; if (!c.active) return;
            cleanedCount++; pollutionLevel = Math.max(0, pollutionLevel - 8);
            document.getElementById("cleaned").innerText = cleanedCount;
            updatePollutionUI();
            clearCell(i);
        }
        function startGame() {
            document.getElementById("start-overlay").classList.add("hidden");
            document.getElementById("end-overlay").classList.add("hidden");
            timeLeft = 30; cleanedCount = 0; pollutionLevel = 0; gameActive = true;
            document.getElementById("time").innerText = timeLeft;
            document.getElementById("cleaned").innerText = cleanedCount;
            updatePollutionUI(); cells.forEach((_, i) => clearCell(i));
            timerInterval = setInterval(() => {
                timeLeft--; document.getElementById("time").innerText = timeLeft;
                if (timeLeft <= 0) endGame(false);
            }, 1000);
            spawnInterval = setInterval(spawnTrash, 550);
            pollInterval = setInterval(() => {
                let dirties = cells.filter(c => c.active !== null).length;
                if (dirties > 0) { pollutionLevel += dirties * 0.5; updatePollutionUI(); }
            }, 300);
        }
        function endGame(overload) {
            gameActive = false; clearInterval(timerInterval); clearInterval(spawnInterval); clearInterval(pollInterval);
            cells.forEach((_, i) => clearCell(i));
            document.getElementById("final-cleaned").innerText = cleanedCount;
            document.getElementById("end-emoji").innerText = overload ? "⚠️🌊" : "🌿🐟";
            document.getElementById("end-title").innerText = overload ? "¡El río colapsó!" : "¡Río Salvado!";
            document.getElementById("impact-text").innerHTML = `🌍 Mantener los ríos y humedales limpios protege los mantos acuíferos subterráneos de los cuales depende más del <b>50% del agua potable</b> del planeta.`;
            document.getElementById("end-overlay").classList.remove("hidden");
        }
        </script>
        </body>
        </html>
        """
        components.html(rio_html, height=520)

# =====================================================
# TAB 4: FUENTES DE INFORMACIÓN
# =====================================================
with tab4:
    st.subheader("8. Fuentes de información oficiales")

    st.write(
        "Para garantizar la veracidad del proyecto, los datos e "
        "indicadores se relacionan con las siguientes instituciones:"
    )

    st.markdown("""
    ### CONAGUA
    Comisión Nacional del Agua.

    Documento: Estadísticas del Agua en México / Atlas del Agua.

    [Consultar CONAGUA](https://www.gob.mx/conagua)

    ### Sistema de Información del Agua

    Institución: CONAGUA.

    [Consultar Sistema de Información del Agua](https://app.conagua.gob.mx/sistemasdeagua/)

    ### INEGI

    Instituto Nacional de Estadística y Geografía.

    Documento: Censos de población y estadísticas sobre servicios de agua potable y saneamiento.

    [Consultar INEGI](https://www.inegi.org.mx/)

    ### FAO

    Organización de las Naciones Unidas para la Alimentación y la Agricultura.

    Documento: Base de datos global de recursos hídricos (AQUASTAT).

    [Consultar FAO](https://www.fao.org/)
    """)

# =====================================================
# PIE DE PÁGINA GENERAL
# =====================================================

st.markdown("---")

st.title("💧 ¡Cada gota cuenta!")

st.write(
    "El cuidado del agua es una responsabilidad compartida. "
    "Conocer su disponibilidad, evitar el desperdicio y cambiar "
    "nuestros hábitos son pasos importantes para proteger este "
    "recurso indispensable."
)

st.success(
    "Gracias por participar y contribuir al cuidado del agua."
)
