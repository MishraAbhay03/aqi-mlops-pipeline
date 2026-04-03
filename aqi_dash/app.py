import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from google.cloud import bigquery
import pandas as pd

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

PROJECT = "stalwart-seat-484411-v0"
DATASET = "aqi_mlops"
client = bigquery.Client()

# ---------------- BigQuery ----------------
def get_current(city):
    query = f"""
    SELECT *
    FROM `{PROJECT}.{DATASET}.dashboard_data`
    WHERE city='{city}'
    ORDER BY timestamp DESC
    LIMIT 1
    """
    return client.query(query).to_dataframe()

def get_forecast(city):
    query = f"""
    SELECT timestamp, aqi
    FROM `{PROJECT}.{DATASET}.forecast`
    WHERE city='{city}'
    ORDER BY timestamp
    """
    return client.query(query).to_dataframe()

# ---------------- Safe Value ----------------
def safe(val):
    if val is None:
        return 0
    if pd.isna(val):
        return 0
    return float(val)

# ---------------- AQI Color ----------------
def aqi_color(aqi):
    if aqi <= 50: return "#00e400"
    elif aqi <= 100: return "#ffff00"
    elif aqi <= 200: return "#ff7e00"
    elif aqi <= 300: return "#ff0000"
    return "#8f3f97"

# ---------------- India Map ----------------
def india_map():
    cities = {
        "Delhi": (28.61, 77.23),
        "Mumbai": (19.07, 72.87),
        "Bangalore": (12.97, 77.59),
        "Chennai": (13.08, 80.27),
        "Hyderabad": (17.38, 78.48),
        "Kolkata": (22.57, 88.36),
        "Pune": (18.52, 73.85),
        "Ahmedabad": (23.02, 72.57),
        "Jaipur": (26.91, 75.79),
        "Lucknow": (26.85, 80.95),
    }

    fig = go.Figure(go.Scattermapbox(
        lat=[v[0] for v in cities.values()],
        lon=[v[1] for v in cities.values()],
        text=list(cities.keys()),
        mode="markers",
        marker=dict(size=14, color="cyan")
    ))

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox_zoom=3.8,
        mapbox_center={"lat": 22.5, "lon": 80},
        paper_bgcolor="#06142b",
        margin=dict(l=0,r=0,t=0,b=0)
    )

    return fig

# ---------------- Card ----------------
def card(title, value, unit="", color="#0b2a4a"):
    return html.Div([
        html.Div(title, style={"fontSize": "14px", "opacity": "0.7"}),
        html.H2(f"{value} {unit}", style={"margin": "5px"})
    ], style={
        "background": color,
        "padding": "18px",
        "borderRadius": "12px",
        "textAlign": "center",
        "flex": "1",
        "boxShadow": "0px 4px 12px rgba(0,0,0,0.4)",
        "border": "1px solid rgba(255,255,255,0.05)"
    })

# ---------------- Layout Function (IMPORTANT FOR CLOUD RUN) ----------------
def serve_layout():
    return html.Div(style={
        "backgroundColor": "#06142b",
        "color": "white",
        "padding": "20px",
        "fontFamily": "Segoe UI"
    }, children=[

        html.H1("Air Quality Monitoring Dashboard",
                style={"textAlign": "center", "marginBottom": "20px"}),

        html.H2(id="title", style={"textAlign": "center"}),

        dcc.Store(id="selected-city", data="Delhi"),

        html.Div(id="kpi-row", style={
            "display": "flex",
            "gap": "15px",
            "marginBottom": "20px"
        }),

        html.Div(style={"display": "flex", "gap": "20px"}, children=[

            html.Div([
                html.H3("India Map"),
                dcc.Graph(id="map", figure=india_map())
            ], style={"width": "30%"}),

            html.Div([
                html.H3("AQI Forecast Trend"),
                dcc.Graph(id="trend")
            ], style={"width": "40%"}),

            html.Div(id="pollutant-panel", style={"width": "30%"})
        ])
    ])

app.layout = serve_layout

# ---------------- Map Click ----------------
@app.callback(
    Output("selected-city", "data"),
    Input("map", "clickData"),
    prevent_initial_call=True
)
def select_city(clickData):
    return clickData["points"][0]["text"]

# ---------------- Update Dashboard ----------------
@app.callback(
    Output("title", "children"),
    Output("kpi-row", "children"),
    Output("pollutant-panel", "children"),
    Output("trend", "figure"),
    Input("selected-city", "data")
)
def update(city):

    df = get_current(city)
    if df.empty:
        return "No Data", [], [], go.Figure()

    aqi = safe(df["aqi"].iloc[0])
    pm25 = safe(df["pm25"].iloc[0])
    temp = safe(df["temperature"].iloc[0])
    humidity = safe(df["humidity"].iloc[0])
    wind = safe(df["wind_speed"].iloc[0])

    forecast_df = get_forecast(city)
    avg_aqi = forecast_df["aqi"].mean()
    max_aqi = forecast_df["aqi"].max()

    kpis = [
        card("AQI", round(aqi,1), "", aqi_color(aqi)),
        card("PM2.5", round(pm25,1), "µg/m³"),
        card("Temperature", round(temp,1), "°C"),
        card("Humidity", round(humidity,1), "%"),
        card("Wind", round(wind,1), "km/h"),
        card("Avg Forecast AQI", round(avg_aqi,1)),
        card("Max Forecast AQI", round(max_aqi,1))
    ]

    pollutants_panel = html.Div([
        html.H3("Current Pollutant Levels"),
        card("PM10", round(safe(df["pm10"].iloc[0]),1), "µg/m³"),
        card("NO₂", round(safe(df["no2"].iloc[0]),1), "µg/m³"),
        card("SO₂", round(safe(df["so2"].iloc[0]),1), "µg/m³"),
        card("CO", round(safe(df["co"].iloc[0]),1), "mg/m³"),
        card("O₃", round(safe(df["o3"].iloc[0]),1), "µg/m³"),
    ], style={"display": "flex","flexDirection": "column","gap": "15px"})

    fig = go.Figure()
    if not forecast_df.empty:
        fig.add_trace(go.Scatter(
            x=forecast_df["timestamp"],
            y=forecast_df["aqi"],
            line=dict(width=3, color="cyan")
        ))

    fig.update_layout(
        paper_bgcolor="#06142b",
        plot_bgcolor="#06142b",
        font=dict(color="white"),
        title="AQI Forecast Trend",
        xaxis_title="Time",
        yaxis_title="AQI"
    )

    return f"{city} AQI Dashboard", kpis, pollutants_panel, fig

# ---------------- Run ----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)