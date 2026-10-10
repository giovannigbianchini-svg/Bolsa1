# Bolsa1

Aplicación de Streamlit que simula cómo habría evolucionado una inversión en un ETF de renta variable (SPY, QQQ o IWM) frente a un ETF de bonos del Tesoro de EE.UU. (SHY, IEI, IEF o TLT), usando precios históricos de Yahoo Finance.

## Estructura

```
Bolsa1/
├── .streamlit/
│   └── config.toml        # Tema visual y opciones del servidor
├── data/
│   └── datos_ejemplo.csv  # Cierres mensuales ajustados (2010-2026) para el modo sin conexión
├── src/
│   ├── __init__.py
│   ├── procesamiento.py   # Descarga de precios y simulación de la inversión
│   └── graficos.py        # Gráficos de Plotly
├── app.py                 # Interfaz de Streamlit (punto de entrada)
├── requirements.txt
└── README.md
```

## Ejecutar en local

Desde la carpeta `Bolsa1`:

```
pip install -r requirements.txt
streamlit run app.py
```

La app se abre en http://localhost:8501.

## Publicar en Streamlit Cloud

1. Sube el contenido de esta carpeta a un repositorio de GitHub, de modo que `app.py` y `requirements.txt` queden en la raíz del repositorio.
2. En https://share.streamlit.io elige **Create app**, selecciona el repositorio y la rama, y escribe `app.py` como *Main file path*.
3. Pulsa **Deploy**. Streamlit Cloud instala las dependencias de `requirements.txt` automáticamente.

## Uso

1. Indica la inversión inicial, la fecha inicial y el número de años.
2. Elige el activo de renta variable y el plazo del bono.
3. Pulsa **Calcular** para ver el capital final, la evolución mensual y la rentabilidad total de ambos activos.

Si Yahoo Finance no responde (a veces limita las peticiones que llegan desde servidores en la nube), marca **Usar datos de ejemplo (sin conexión)**. Ese modo usa los cierres mensuales de `data/datos_ejemplo.csv`, por lo que el resultado puede diferir ligeramente del calculado con precios diarios.
