# Bolsa1 — Simulación histórica de una inversión
# Ejecutar con: streamlit run app.py

from datetime import datetime

import streamlit as st

from src.graficos import grafico_evolucion, grafico_rentabilidad
from src.procesamiento import (
    ACCIONES,
    BONOS,
    calcular_rentabilidad,
    cargar_precios_ejemplo,
    construir_tabla_comparacion,
    descargar_precios,
    simular_inversion,
    sumar_anios,
)

st.set_page_config(page_title="Bolsa1 — Simulación de inversión", page_icon="📈")


# La caché evita volver a descargar los mismos precios en cada interacción.
@st.cache_data(ttl=3600, show_spinner=False)
def obtener_precios(ticker, fecha_inicial, fecha_final, usar_ejemplo):
    if usar_ejemplo:
        return cargar_precios_ejemplo(ticker, fecha_inicial, fecha_final)
    return descargar_precios(ticker, fecha_inicial, fecha_final)


st.title("Simulación histórica de una inversión")

# En Streamlit, en vez de usar input(), usamos widgets para pedir los datos.
inversion_inicial = st.number_input("Inversión inicial", min_value=0.0, value=1000.0)
fecha_inicial_widget = st.date_input("Fecha inicial", value=datetime(2015, 1, 1))
numero_de_anios = st.number_input("Número de años", min_value=1, value=5, step=1)

nombre_accion = st.selectbox("Activo de renta variable", ACCIONES.keys())
plazo_bono = st.selectbox("Plazo del bono del Tesoro (años)", BONOS.keys())

usar_ejemplo = st.checkbox(
    "Usar datos de ejemplo (sin conexión)",
    help="Usa los precios mensuales guardados en data/datos_ejemplo.csv "
    "en lugar de descargarlos de Yahoo Finance.",
)

ticker_accion = ACCIONES[nombre_accion]
ticker_bono = BONOS[plazo_bono]
nombre_bono = f"Bono del Tesoro {plazo_bono} años"

# El botón evita que el cálculo se dispare mientras el usuario todavía está
# eligiendo los valores.
if st.button("Calcular"):

    fecha_inicial = datetime.combine(fecha_inicial_widget, datetime.min.time())
    fecha_final = sumar_anios(fecha_inicial, numero_de_anios)

    if inversion_inicial <= 0 or numero_de_anios <= 0:
        st.error("La inversión y el número de años deben ser mayores que cero.")
        st.stop()

    with st.spinner(f"Obteniendo precios históricos de {ticker_accion} y {ticker_bono}..."):
        try:
            precios_accion = obtener_precios(ticker_accion, fecha_inicial, fecha_final, usar_ejemplo)
            precios_bono = obtener_precios(ticker_bono, fecha_inicial, fecha_final, usar_ejemplo)
        except Exception as error:
            st.error(
                f"No se pudieron obtener los precios: {error}\n\n"
                "Prueba de nuevo o marca «Usar datos de ejemplo»."
            )
            st.stop()

    capital_accion = simular_inversion(precios_accion, inversion_inicial)
    capital_bonos = simular_inversion(precios_bono, inversion_inicial)

    if capital_accion is None:
        st.error(f"No se encontraron datos de {ticker_accion} para el período indicado.")
        st.stop()

    if capital_bonos is None:
        st.error(f"No se encontraron datos del bono del Tesoro ({ticker_bono}) para el período indicado.")
        st.stop()

    rentabilidad_accion = calcular_rentabilidad(capital_accion, inversion_inicial)
    rentabilidad_bonos = calcular_rentabilidad(capital_bonos, inversion_inicial)

    st.subheader("Resultados")

    columna1, columna2 = st.columns(2)
    columna1.metric(
        f"Capital final: {nombre_accion}",
        f"$ {capital_accion.iloc[-1]:,.2f}",
        f"{rentabilidad_accion:.2%}",
    )
    columna2.metric(
        f"Capital final: {nombre_bono}",
        f"$ {capital_bonos.iloc[-1]:,.2f}",
        f"{rentabilidad_bonos:.2%}",
    )

    st.subheader("Evolución del capital a lo largo del tiempo")
    tabla_comparacion = construir_tabla_comparacion(
        {nombre_accion: capital_accion, nombre_bono: capital_bonos}
    )
    st.plotly_chart(grafico_evolucion(tabla_comparacion), width="stretch")

    st.subheader("Rentabilidad total comparada")
    st.plotly_chart(
        grafico_rentabilidad(
            {nombre_accion: rentabilidad_accion, nombre_bono: rentabilidad_bonos}
        ),
        width="stretch",
    )

    st.subheader("Detalle mensual")
    st.dataframe(tabla_comparacion.style.format("$ {:,.2f}"), width="stretch")
