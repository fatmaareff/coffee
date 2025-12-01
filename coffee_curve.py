import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Coffee Curve ☕",
    page_icon="☕",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>☕ The Coffee Addiction Curve</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Visualisation interactive du niveau d'énergie selon ta consommation de café</p>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# SIDEBAR – user input
# -----------------------------
st.sidebar.title("⚙️ Paramètres")

coffee_count = st.sidebar.slider(
    "Nombre de cafés pris aujourd’hui",
    min_value=0,
    max_value=5,
    value=2
)

# -----------------------------
# Data Generator
# -----------------------------
def generate_energy_data(num):
    hours = ["6h","7h","8h","9h","10h","11h","12h","13h","14h","15h","16h","17h","18h","19h","20h","21h","22h"]

    base = [10,20,30,35,30,28,26,22,20,18,16,14,12,10,8,6,5]
    energy = base.copy()

    mood = ["😴"] * len(hours)
    status = ["Low"] * len(hours)

    # COFFEE EFFECTS
    if num >= 1:
        energy[2] = 85
        energy[3] = 95
        energy[4] = 80
        mood[3] = "🚀"
        status[3] = "1st Coffee Boost"

    if num >= 2:
        energy[8] = 60
        energy[9] = 90
        energy[10] = 85
        mood[9] = "😎"
        status[9] = "2nd Coffee Boost"

    if num >= 3:
        energy[12] = 92
        mood[12] = "💥"
        status[12] = "3rd Coffee Boost"

    if num >= 4:
        energy[14] = 95
        mood[14] = "🔥"
        status[14] = "Overcaffeinated"

    if num == 5:
        energy[15] = 98
        mood[15] = "⚡"
        status[15] = "MAX POWER"

    return pd.DataFrame({
        "Hour": hours,
        "Energy": energy,
        "Mood": mood,
        "Status": status
    })

df = generate_energy_data(coffee_count)

# -----------------------------
# PLOTLY CURVE
# -----------------------------
st.subheader("📈 Courbe d’énergie de la journée")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Hour"],
    y=df["Energy"],
    mode="lines+markers+text",
    line=dict(width=4),
    marker=dict(size=12),
    text=df["Mood"],
    textposition="top center",
    name="Energy"
))

fig.update_layout(
    yaxis=dict(range=[0, 110], title="Energy %"),
    xaxis=dict(title="Heure"),
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Stats
# -----------------------------
st.markdown("## 📊 Statistiques")

col1, col2, col3 = st.columns(3)

col1.metric("🔝 Peak Energy", f"{df['Energy'].max()}%")
col2.metric("🔻 Minimum", f"{df['Energy'].min()}%")
col3.metric("⚡ Moyenne", f"{round(df['Energy'].mean(),1)}%")

# -----------------------------
# Interpretation
# -----------------------------
st.markdown("## 🎯 Conclusion")

if coffee_count == 0:
    st.error("💀 Sans café : Mode ZOMBIE.")
elif coffee_count == 1:
    st.warning("😴 Avec 1 café : survie minimale.")
elif coffee_count == 2:
    st.success("✨ Avec 2 cafés : performance optimale.")
elif coffee_count == 3:
    st.info("⚠️ Avec 3 cafés : très énergique… limite tremblant.")
else:
    st.error("🚨 Trop de cafés : cœur = brrrrrrr ⚡🔥")

st.markdown("<p style='text-align:center; opacity:0.6;'>📌 Basé sur des faits scientifiques totalement inventés 😂</p>", unsafe_allow_html=True)
