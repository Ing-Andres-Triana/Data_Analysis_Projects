import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard de Ventas", page_icon="📈", layout="wide")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig", parse_dates=["fecha"])
    df["anio"] = df["fecha"].dt.year
    df["roi"] = df["ventas_millones"] / df["publicidad_millones"]
    return df


df = load_data("01_ventas_mensuales.csv")

st.title("📈 Dashboard de ventas y publicidad")
st.caption("Cifras en millones")

# ---------- Filtros ----------
st.sidebar.header("Filtros")
anios = st.sidebar.multiselect(
    "Año", sorted(df["anio"].unique()), default=sorted(df["anio"].unique())
)
f = df[df["anio"].isin(anios)]

if f.empty:
    st.warning("Selecciona al menos un año.")
    st.stop()

# ---------- KPIs ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ventas totales", f"{f['ventas_millones'].sum():,.0f}")
c2.metric("Publicidad total", f"{f['publicidad_millones'].sum():,.1f}")
c3.metric("Ventas promedio / mes", f"{f['ventas_millones'].mean():,.1f}")
c4.metric("Ventas por $1 de publicidad", f"{f['roi'].mean():.1f}")

# Crecimiento interanual (si hay ambos años seleccionados)
if {2024, 2025}.issubset(set(anios)):
    v24 = df[df["anio"] == 2024]["ventas_millones"].sum()
    v25 = df[df["anio"] == 2025]["ventas_millones"].sum()
    st.info(f"Crecimiento de ventas 2025 vs 2024: **{(v25 / v24 - 1) * 100:.1f}%**")

# ---------- Gráficos ----------
left, right = st.columns(2)

with left:
    st.subheader("Ventas mensuales")
    fig = px.line(f, x="fecha", y="ventas_millones", markers=True,
                  labels={"fecha": "", "ventas_millones": "Ventas (M)"})
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Publicidad mensual")
    fig = px.bar(f, x="fecha", y="publicidad_millones",
                 labels={"fecha": "", "publicidad_millones": "Publicidad (M)"})
    st.plotly_chart(fig, width="stretch")

st.subheader("¿Más publicidad = más ventas?")
fig = px.scatter(f, x="publicidad_millones", y="ventas_millones",
                 color=f["anio"].astype(str), trendline="ols",
                 labels={"publicidad_millones": "Publicidad (M)",
                         "ventas_millones": "Ventas (M)", "color": "Año"})
st.plotly_chart(fig, width="stretch")

with st.expander("Ver datos"):
    st.dataframe(f.drop(columns=["anio"]), width="stretch")
    st.download_button("Descargar CSV", f.to_csv(index=False).encode("utf-8"),
                       "ventas_filtradas.csv", "text/csv")
