import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os 

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Coffee Curve ☕",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# 🎨 Enhanced Professional Style
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #1a0d08 0%, #2d1810 25%, #1f1410 50%, #0f0a08 100%);
        color: #f9fafb;
    }
    
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .hero-section {
        text-align: center;
        padding: 2rem 1rem 1.5rem 1rem;
        background: linear-gradient(135deg, rgba(139, 69, 19, 0.15) 0%, rgba(101, 67, 33, 0.1) 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid rgba(184, 134, 11, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #d4a574, #8b4513, #d4a574);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .big-title {
        font-size: 3.5rem;
        font-weight: 900;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #f4e4c1 0%, #d4a574 50%, #8b4513 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
    }
    
    .subtitle {
        font-size: 1.15rem;
        color: #e5e7eb;
        margin-bottom: 1rem;
        font-weight: 300;
        line-height: 1.6;
    }
    
    .coffee-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 4px 8px rgba(139, 69, 19, 0.6));
    }
    
    .card {
        background: linear-gradient(135deg, rgba(30, 20, 15, 0.95) 0%, rgba(20, 15, 12, 0.98) 100%);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        border: 1px solid rgba(212, 165, 116, 0.25);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4a574, transparent);
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 50px rgba(139, 69, 19, 0.4);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        color: #d4a574;
        border-bottom: 2px solid rgba(212, 165, 116, 0.2);
        padding-bottom: 0.5rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, rgba(139, 69, 19, 0.15) 0%, rgba(101, 67, 33, 0.1) 100%);
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid rgba(212, 165, 116, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: scale(1.05);
        border-color: rgba(212, 165, 116, 0.5);
    }
    
    .footer-note {
        text-align: center;
        opacity: 0.7;
        margin-top: 1rem;
        font-size: 0.95rem;
        font-style: italic;
        color: #d4a574;
    }
    
    .author-section {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        background: linear-gradient(135deg, rgba(139, 69, 19, 0.1) 0%, rgba(101, 67, 33, 0.05) 100%);
        border-radius: 20px;
        border: 1px solid rgba(212, 165, 116, 0.15);
    }
    
    .author-photo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #d4a574;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.4);
    }
    
    .author-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #d4a574;
        margin: 0;
    }
    
    .author-label {
        font-size: 0.85rem;
        color: #e5e7eb;
        opacity: 0.7;
        margin-top: 0.2rem;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #8b4513, #d4a574);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0d08 0%, #2d1810 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #f4e4c1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HEADER WITH HERO SECTION
# -----------------------------
st.markdown(
    """
    <div class='hero-section'>
        <div class='coffee-icon'>☕</div>
        <h1 class='big-title'>The Coffee Addiction Curve</h1>
        <p class='subtitle'>Because our energy doesn't follow a straight line.<br>It moves with our habits, our moods... and our caffeine.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR – user input
# -----------------------------
st.sidebar.markdown("### ⚙️ Control Panel")
st.sidebar.markdown("---")

coffee_count = st.sidebar.slider(
    "☕ Number of coffees today",
    min_value=0,
    max_value=5,
    value=2,
    help="Adjust to see how coffee impacts your energy curve"
)

st.sidebar.markdown("---")
st.sidebar.caption("📅 **Assumption:** Coffees consumed at 8:00, 10:00, 14:00, 16:00 and 20:00.")
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** The optimal zone is typically 2-3 coffees per day for sustained productivity.")

# -----------------------------
# Data Generator
# -----------------------------
def generate_energy_data(num: int) -> pd.DataFrame:
    hours = ["6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00",
             "15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"]

    base = [10,20,30,35,30,28,26,22,20,18,16,14,12,10,8,6,5]
    energy = base.copy()

    mood = ["😴"] * len(hours)
    status = ["Low"] * len(hours)

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
# PLOTLY CURVE (Direct - No intro, no side images)
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📈 Daily Energy Curve</div>", unsafe_allow_html=True)

fig = go.Figure()

# Main energy curve with gradient effect
fig.add_trace(go.Scatter(
    x=df["Hour"],
    y=df["Energy"],
    mode="lines+markers+text",
    line=dict(width=4, color='#d4a574', shape='spline'),
    marker=dict(size=12, color='#8b4513', line=dict(width=2, color='#f4e4c1')),
    text=df["Mood"],
    textposition="top center",
    textfont=dict(size=16),
    name="Energy",
    hovertemplate="<b>%{x}</b><br>Energy: %{y}%<extra></extra>"
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
        marker=dict(size=22, symbol="star", color='#FFD700', line=dict(width=3, color='#8b4513')),
        text=[f"☕ #{i+1}" for i in range(len(coffee_hours))],
        textposition="bottom center",
        textfont=dict(size=12, color='#FFD700'),
        name="Coffee Moments",
        hovertemplate="<b>Coffee %{text}</b><br>Time: %{x}<br>Energy: %{y}%<extra></extra>"
    ))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0.3)',
    yaxis=dict(
        range=[0, 110],
        title="Energy Level (%)",
        gridcolor='rgba(212, 165, 116, 0.1)',
        tickfont=dict(color='#f4e4c1')
    ),
    xaxis=dict(
        title="Time of Day",
        gridcolor='rgba(212, 165, 116, 0.1)',
        tickfont=dict(color='#f4e4c1')
    ),
    height=500,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=40),
    font=dict(color='#f4e4c1')
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Stats (Enhanced)
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Key Performance Metrics</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("🔝 Peak Energy", f"{df['Energy'].max()}%")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("🔻 Minimum Level", f"{df['Energy'].min()}%")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("⚡ Average", f"{round(df['Energy'].mean(),1)}%")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Conclusion (Enhanced)
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🎯 Performance Analysis</div>", unsafe_allow_html=True)

if coffee_count == 0:
    message = "💀 **Zero Coffee Mode:** You look like an old laptop that needs to be plugged in. Energy at 10%. Pure survival instinct."
    emoji = "😴"
elif coffee_count == 1:
    message = "🚀 **First Coffee Boost:** The magic moment! Energy jumps from 😴 to 🚀 instantly. That's what we call the awakening."
    emoji = "🚀"
elif coffee_count == 2:
    message = "😎 **The Sweet Spot:** Not because you want to... Because your soul needs it. Peak performance achieved. This is where magic happens."
    emoji = "✨"
elif coffee_count == 3:
    message = "💥 **The Midday Warrior:** Three coffees in. You've survived the famous 2 p.m. crash. The curve is beautiful and powerful."
    emoji = "💥"
elif coffee_count == 4:
    message = "🔥 **Entering the Overcaffeinated Zone:** Energy 100% • Hands shaking • Heart doing TikTok dances • Brain: 'Let's reorganize the house at 9 p.m.'"
    emoji = "🔥"
else:
    message = "⚡ **Maximum Chaos Mode:** The curve is now a chaotic mountain range. You're not tired... you've transcended tiredness."
    emoji = "⚡"

st.markdown(f"### {emoji} {message}")
st.markdown("---")
st.markdown(
    """
    ### 💭 The Real Truth
    
    This curve is funny... but it shows something real:
    
    **Our energy doesn't follow a straight line.** It moves with our habits, our moods, and yes... our caffeine.
    
    We're all riding our own energy curves every day. The question is: *Are you aware of yours?*
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<p class='footer-note'>📌 Based on real coffee addiction and totally legitimate self-observation research ☕😂</p>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Author Section
# -----------------------------
st.markdown("<div class='author-section'>", unsafe_allow_html=True)

# Try to load profile photo, if it exists
st.markdown(
    """
    <p class='author-label'>MADE BY</p>
    <p class='author-name'>MOHAMED BOUSSOFFARA</p>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)