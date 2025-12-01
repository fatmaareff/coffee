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
# 🎨 Simple & clean style
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
    "<p class='subtitle'>Interactive visualization of your energy level throughout the day, based on how much coffee you drink.</p>",
    unsafe_allow_html=True
)
st.markdown("<div class='gradient-bar'></div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR – user input
# -----------------------------
st.sidebar.title("⚙️ Settings")

coffee_count = st.sidebar.slider(
    "Number of coffees today",
    min_value=0,
    max_value=5,
    value=2
)

st.sidebar.caption("Assumption: coffees at 8:00, 10:00, 14:00, 16:00 and 20:00.")

# -----------------------------
# Data Generator
# -----------------------------
def generate_energy_data(num: int) -> pd.DataFrame:
    hours = ["6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00",
             "15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"]

    # Baseline energy curve (no coffee)
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

# Coffee times (for highlighting on the curve)
def get_coffee_hours(num: int):
    lst = []
    if num >= 1: lst.append("8:00")
    if num >= 2: lst.append("10:00")
    if num >= 3: lst.append("14:00")
    if num >= 4: lst.append("16:00")
    if num >= 5: lst.append("20:00")
    return lst

coffee_hours = get_coffee_hours(coffee_count)

# -----------------------------
# INTRO
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 Introduction</div>", unsafe_allow_html=True)
st.markdown(
    """
    This curve represents **E(t)**, your theoretical energy level over the day:
    
    - a natural baseline that rises in the morning and slowly decreases in the evening;  
    - each ☕ adds a **temporary boost** at the time you drink it;  
    - the more coffee you drink, the higher (and more chaotic) the curve becomes 😅.
    """
)
if coffee_hours:
    st.markdown(f"Today, we assume you had your coffees at: **{', '.join(coffee_hours)}**.")
else:
    st.markdown("Today, you had no coffee: your curve depends only on your natural energy 😴.")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PLOTLY CURVE
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📈 Daily Energy Curve</div>", unsafe_allow_html=True)

fig = go.Figure()

# Main energy curve
fig.add_trace(go.Scatter(
    x=df["Hour"],
    y=df["Energy"],
    mode="lines+markers+text",
    line=dict(width=4),
    marker=dict(size=10),
    text=df["Mood"],
    textposition="top center",
    name="Energy"
))

# Highlight coffee moments
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
        name="Coffees",
        hovertemplate="Coffee %{text}<br>Time: %{x}<br>Energy: %{y}%<extra></extra>"
    ))

fig.update_layout(
    template="plotly_dark",
    yaxis=dict(range=[0, 110], title="Energy (%)"),
    xaxis=dict(title="Time of day"),
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
st.markdown("<div class='section-title'>📊 Key Statistics</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🔝 Peak energy", f"{df['Energy'].max()}%")
col2.metric("🔻 Minimum", f"{df['Energy'].min()}%")
col3.metric("⚡ Average", f"{round(df['Energy'].mean(),1)}%")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Conclusion
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🎯 Conclusion</div>", unsafe_allow_html=True)

if coffee_count == 0:
    message = "💀 No coffee: pure zombie mode, but at least your heart is calm."
elif coffee_count == 1:
    message = "😴 With 1 coffee: basic survival mode. It works, but avoid heavy math."
elif coffee_count == 2:
    message = "✨ With 2 coffees: **optimal performance zone**. Your brain runs in HD."
elif coffee_count == 3:
    message = "⚠️ With 3 coffees: very energetic… productive, but slightly shaking."
else:
    message = "🚨 Many coffees: **heart = brrrrr ⚡🔥**. Your E(t) is maxed out, drink water tomorrow."

st.write(message)
st.markdown(
    "<p class='footer-note'>📌 Based on totally fake science… but emotionally very accurate 😂</p>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)


