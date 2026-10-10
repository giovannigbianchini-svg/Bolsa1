"""Gráficos de Plotly que muestra la app."""

import pandas as pd
import plotly.express as px

# Un color fijo por tipo de activo, en el orden de las columnas de la tabla.
COLORES = ["#2a78d6", "#eda100"]


def grafico_evolucion(tabla_comparacion: pd.DataFrame):
    """Líneas con la evolución del capital de cada activo a lo largo del tiempo."""
    datos = tabla_comparacion.rename_axis("Fecha").reset_index().melt(
        id_vars="Fecha", var_name="Activo", value_name="Capital"
    )
    fig = px.line(
        datos, x="Fecha", y="Capital", color="Activo",
        color_discrete_sequence=COLORES,
    )
    fig.update_traces(hovertemplate="%{x|%b %Y}<br>$ %{y:,.2f}")
    fig.update_layout(
        legend_title=None,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        xaxis_title=None,
        yaxis_title="Capital",
        yaxis_tickprefix="$ ",
        yaxis_tickformat=",.0f",
        margin=dict(t=40),
    )
    return fig


def grafico_rentabilidad(rentabilidades: dict):
    """Barras con la rentabilidad total de cada activo.

    Recibe un diccionario {nombre para mostrar: rentabilidad}.
    """
    datos = pd.DataFrame(
        {
            "Activo": list(rentabilidades.keys()),
            "Rentabilidad total": list(rentabilidades.values()),
        }
    )
    fig = px.bar(
        datos, x="Activo", y="Rentabilidad total", color="Activo",
        color_discrete_sequence=COLORES, text_auto=".2%",
    )
    fig.update_traces(hovertemplate="%{x}<br>%{y:.2%}<extra></extra>")
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_tickformat=".0%",
        margin=dict(t=40),
    )
    return fig
