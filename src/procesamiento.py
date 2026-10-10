"""Lógica de negocio: descarga de precios y simulación de la inversión.

Este módulo no importa Streamlit a propósito, para poder probarlo o reutilizarlo
fuera de la app.
"""

from pathlib import Path

import pandas as pd
import yfinance as yf

RUTA_DATOS_EJEMPLO = Path(__file__).resolve().parent.parent / "data" / "datos_ejemplo.csv"

# ETFs que representan cada opción de renta variable.
ACCIONES = {
    "SPY (S&P 500)": "SPY",
    "QQQ (Nasdaq 100)": "QQQ",
    "IWM (Russell 2000)": "IWM",
}

# ETFs de bonos del Tesoro de EE.UU. según el plazo elegido.
BONOS = {
    2: "SHY",  # 1-3 años
    5: "IEI",  # 3-7 años
    10: "IEF",  # 7-10 años
    20: "TLT",  # 20+ años
}


def sumar_anios(fecha, cantidad):
    """Devuelve la misma fecha después de sumar una cantidad de años."""
    try:
        return fecha.replace(year=fecha.year + cantidad)
    except ValueError:
        # Convierte el 29 de febrero en 28 de febrero si hace falta.
        return fecha.replace(year=fecha.year + cantidad, day=28)


def descargar_precios(ticker, fecha_inicial, fecha_final):
    """Descarga de Yahoo Finance los precios de cierre diarios de un ticker.

    Devuelve una Serie de pandas (vacía si no hay datos para el período).
    """
    # auto_adjust=True tiene en cuenta dividendos y desdoblamientos.
    datos = yf.download(
        ticker,
        start=fecha_inicial,
        end=fecha_final,
        auto_adjust=True,
        progress=False,
        multi_level_index=False,
    )

    if datos.empty:
        return pd.Series(dtype=float, name=ticker)

    return datos["Close"].dropna().rename(ticker)


def cargar_precios_ejemplo(ticker, fecha_inicial, fecha_final):
    """Lee los precios de cierre mensuales guardados en data/datos_ejemplo.csv.

    Sirve para usar la app sin conexión o cuando Yahoo Finance no responde.
    """
    datos = pd.read_csv(RUTA_DATOS_EJEMPLO, index_col="Fecha", parse_dates=True)

    if ticker not in datos.columns:
        return pd.Series(dtype=float, name=ticker)

    return datos.loc[fecha_inicial:fecha_final, ticker].dropna()


def simular_inversion(precios, inversion_inicial):
    """Simula cómo crecería una inversión mes a mes a partir de una serie de precios.

    Devuelve una Serie de pandas con el capital acumulado en cada mes,
    o None si no hay datos suficientes.
    """
    if precios.empty:
        return None

    # Conservamos el último precio disponible de cada mes.
    precios_mensuales = precios.resample("ME").last().dropna()

    if len(precios_mensuales) < 2:
        return None

    capital_actual = inversion_inicial
    precio_anterior = float(precios.iloc[0])
    fechas = []
    capitales = []

    for fecha, precio in precios_mensuales.items():
        precio = float(precio)
        variacion_mensual = precio / precio_anterior - 1
        capital_actual += capital_actual * variacion_mensual
        fechas.append(fecha)
        capitales.append(capital_actual)
        precio_anterior = precio

    return pd.Series(capitales, index=fechas, name=precios.name)


def calcular_rentabilidad(capital, inversion_inicial):
    """Rentabilidad total de la simulación (0.25 equivale a un 25 %)."""
    return capital.iloc[-1] / inversion_inicial - 1


def construir_tabla_comparacion(capitales):
    """Une varias series de capital en una tabla, una columna por activo.

    Recibe un diccionario {nombre para mostrar: serie de capital}.
    """
    return pd.concat(
        [serie.rename(nombre) for nombre, serie in capitales.items()],
        axis=1,
    )
