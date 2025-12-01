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

# -----------------------------
# 🎨 Style simple & propre
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #431407 0, #1f2937 40%, #020617 100%);
        color: #f9fafb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    .big-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.05rem;
        color: #e5e7ebcc;
        margin-bottom: 0.3rem;
    }
    .gradient-bar {
        height: 4px;
        max-width: 230px;
        margin: 0.6rem auto 1.4rem auto;
        border-radius: 999px;
        background: linear-gradient(90deg, #fbbf24, #fb7185, #a855f7);
    }
    .card {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 18px;
        padding: 1.3rem 1.6rem;
        border: 1px solid rgba(148, 163, 184, 0.4);
        box-shadow: 0 18px 38px rgba(15, 23, 42, 0.85);
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .footer-note {
        text-align: center;
        opacity: 0.6;
        margin-top: 0.7rem;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1 class='big-title'>THE COFFEE ADDICTION CURVE</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Visualisation interactive de ton niveau d'énergie en fonction de ta dose quotidienne de café.</p>",
    unsafe_allow_html=True
)
st.markdown("<div class='gradient-bar'></div>", unsafe_allow_html=True)

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

st.sidebar.caption("Hypothèse : 1er café à 8h, puis 10h, 14h, 16h et 20h.")

# -----------------------------
# Data Generator
# -----------------------------
def generate_energy_data(num: int) -> pd.DataFrame:
    hours = ["6h","7h","8h","9h","10h","11h","12h","13h","14h",
             "15h","16h","17h","18h","19h","20h","21h","22h"]

    base = [10,20,30,35,30,28,26,22,20,18,16,14,12,10,8,6,5]
    energy = base.copy()

    mood = ["😴"] * len(hours)
    status = ["Low"] * len(hours)

    # COFFEE EFFECTS (ta logique d'origine)
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

# Heures “théoriques” des cafés (juste pour l’affichage sur la courbe)
def get_coffee_hours(num: int):
    lst = []
    if num >= 1: lst.append("8h")
    if num >= 2: lst.append("10h")
    if num >= 3: lst.append("14h")
    if num >= 4: lst.append("16h")
    if num >= 5: lst.append("20h")
    return lst

coffee_hours = get_coffee_hours(coffee_count)

# -----------------------------
# INTRO
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 Introduction</div>", unsafe_allow_html=True)
st.markdown(
    """
    Cette courbe représente **E(t)**, ton niveau d'énergie supposé tout au long de la journée :
    
    - une base d’énergie qui monte le matin puis redescend doucement le soir ;  
    - chaque ☕ ajoute un **boost temporaire** au moment où tu le bois ;  
    - plus tu bois de cafés, plus la courbe grimpe… mais pas forcément de façon très saine 😅.
    """
)
if coffee_hours:
    st.markdown(f"Aujourd’hui, on suppose que tu as bu tes cafés vers : **{', '.join(coffee_hours)}**.")
else:
    st.markdown("Aujourd’hui, aucun café : ta courbe repose uniquement sur ton énergie naturelle 😴.")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PLOTLY CURVE
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📈 Courbe d’énergie de la journée</div>", unsafe_allow_html=True)

fig = go.Figure()

# Courbe principale
fig.add_trace(go.Scatter(
    x=df["Hour"],
    y=df["Energy"],
    mode="lines+markers+text",
    line=dict(width=4),
    marker=dict(size=10),
    text=df["Mood"],
    textposition="top center",
    name="Énergie"
))

# Points spéciaux pour montrer quand les cafés sont pris
if coffee_hours:
    coffee_y = [
        df.loc[df["Hour"] == h, "Energy"].values[0]
        for h in coffee_hours
    ]
    fig.add_trace(go.Scatter(
        x=coffee_hours,
        y=coffee_y,
        mode="markers+text",
        marker=dict(size=18, symbol="star", line=dict(width=2, color="white")),
        text=[f"☕ #{i+1}" for i in range(len(coffee_hours))],
        textposition="bottom center",
        name="Cafés",
        hovertemplate="Café %{text}<br>Heure : %{x}<br>Énergie : %{y}%<extra></extra>"
    ))

fig.update_layout(
    template="plotly_dark",
    yaxis=dict(range=[0, 110], title="Énergie (%)"),
    xaxis=dict(title="Heure"),
    height=480,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=10, b=40)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Stats
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Statistiques</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🔝 Pic d’énergie", f"{df['Energy'].max()}%")
col2.metric("🔻 Minimum", f"{df['Energy'].min()}%")
col3.metric("⚡ Moyenne", f"{round(df['Energy'].mean(),1)}%")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Conclusion
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🎯 Conclusion</div>", unsafe_allow_html=True)

if coffee_count == 0:
    message = "💀 Sans café : **mode zombie**, mais tu prouves que la volonté existe encore."
elif coffee_count == 1:
    message = "😴 Avec 1 café : **survie minimale**. Ça passe, mais évite les gros calculs."
elif coffee_count == 2:
    message = "✨ Avec 2 cafés : **zone de performance optimale**. Ton cerveau tourne en HD."
elif coffee_count == 3:
    message = "⚠️ Avec 3 cafés : **très énergique**… productif·ve mais légèrement tremblant."
else:
    message = "🚨 Beaucoup de cafés : **cœur = brrrrrrr ⚡🔥**. Ta courbe E(t) est au max, pense à l’eau demain."

st.write(message)
st.markdown(
    "<p class='footer-note'>📌 Basé sur des faits scientifiques totalement inventés… mais émotionnellement vrais 😂</p>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

