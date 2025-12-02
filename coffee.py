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
        <h1 class='big-title'>My Daily Energy Curve</h1>
        <p class='subtitle'>A data-driven analysis of how caffeine impacts my productivity throughout the day</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Data Generator - Fixed 2 coffees at 7:30 and 14:00
# -----------------------------
def generate_energy_data() -> pd.DataFrame:
    hours = ["6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30", "10:00", "10:30",
             "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", 
             "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", 
             "20:00", "20:30", "21:00", "21:30", "22:00"]

    # Realistic energy curve with 2 coffees - second coffee less effective
    energy = [
        12,  # 6:00 - Just waking up
        15,  # 6:30 - Getting up
        20,  # 7:00 - Morning routine
        25,  # 7:30 - ☕ FIRST COFFEE
        45,  # 8:00 - Coffee kicking in
        70,  # 8:30 - Rising energy
        85,  # 9:00 - Peak productivity
        82,  # 9:30 - Sustained high
        78,  # 10:00 - Still good
        72,  # 10:30 - Gradual decline
        68,  # 11:00 - Mid-morning
        65,  # 11:30 - Pre-lunch
        60,  # 12:00 - Lunch time
        55,  # 12:30 - Post-lunch dip starting
        48,  # 13:00 - Afternoon slump
        42,  # 13:30 - Energy low
        38,  # 14:00 - ☕ SECOND COFFEE
        50,  # 14:30 - Coffee effect starting (less boost)
        62,  # 15:00 - Energy rising (lower than morning)
        68,  # 15:30 - Second peak (significantly lower)
        70,  # 16:00 - Afternoon peak (max 70% vs 85%)
        67,  # 16:30 - Slight decline
        63,  # 17:00 - Gradual decline
        58,  # 17:30 - Energy dropping
        52,  # 18:00 - End of workday
        45,  # 18:30 - Evening transition
        38,  # 19:00 - Relaxing
        32,  # 19:30 - Winding down
        28,  # 20:00 - Evening
        24,  # 20:30 - Getting tired
        20,  # 21:00 - Preparing for bed
        17,  # 21:30 - Very tired
        15   # 22:00 - Ready to sleep
    ]

    # Minimal markers - professional presentation
    mood = [""] * len(energy)
    
    # Only mark coffee moments
    mood[3] = "☕"   # 7:30 - First coffee
    mood[16] = "☕"  # 14:00 - Second coffee

    return pd.DataFrame({
        "Hour": hours,
        "Energy": energy,
        "Mood": mood
    })

df = generate_energy_data()

# Coffee moments
coffee_hours = ["7:30", "14:00"]

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
    line=dict(width=4, color='#d4a574', shape='spline'),
    marker=dict(size=10, color='#8b4513', line=dict(width=2, color='#f4e4c1')),
    text=df["Mood"],
    textposition="top center",
    textfont=dict(size=14),
    name="Energy Level",
    hovertemplate="<b>%{x}</b><br>Energy: %{y}%<extra></extra>"
))

# Highlight coffee moments
coffee_y = [df.loc[df["Hour"] == h, "Energy"].values[0] for h in coffee_hours]
fig.add_trace(go.Scatter(
    x=coffee_hours,
    y=coffee_y,
    mode="markers+text",
    marker=dict(size=24, symbol="star", color='#FFD700', line=dict(width=3, color='#8b4513')),
    text=["☕ Morning", "☕ Afternoon"],
    textposition="bottom center",
    textfont=dict(size=13, color='#FFD700', family='Poppins'),
    name="Coffee Moments",
    hovertemplate="<b>%{text}</b><br>Time: %{x}<br>Energy: %{y}%<extra></extra>"
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0.3)',
    yaxis=dict(
        range=[0, 100],
        title="Energy Level (%)",
        gridcolor='rgba(212, 165, 116, 0.1)',
        tickfont=dict(color='#f4e4c1', size=12)
    ),
    xaxis=dict(
        title="Time of Day",
        gridcolor='rgba(212, 165, 116, 0.1)',
        tickfont=dict(color='#f4e4c1', size=11),
        tickangle=-45
    ),
    height=550,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=80),
    font=dict(color='#f4e4c1', family='Poppins'),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Stats
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Key Performance Metrics</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("🔝 Peak Energy", f"{df['Energy'].max()}%")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("⚡ Average", f"{round(df['Energy'].mean(),1)}%")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("☕ Daily Coffees", "2")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("⏰ Coffee Times", "7:30 & 14:00")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Analysis
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🎯 Key Insights</div>", unsafe_allow_html=True)

st.markdown(
    """
    ### ☕ The Two-Coffee Strategy
    
    My daily routine follows a scientifically-backed approach to caffeine consumption:
    
    **Morning Coffee (7:30 AM):**
    - Consumed 30-60 minutes after waking up (avoiding cortisol spike)
    - Creates a strong energy boost from ~25% to 85% by 9:00 AM
    - Sustains high productivity through the entire morning
    
    **Afternoon Coffee (14:00):**
    - Strategically timed to combat the post-lunch energy dip
    - Prevents the typical 2 PM crash
    - **Lower effectiveness due to caffeine tolerance** - reaches only 70% vs morning's 85%
    - More modest boost reflects biological reality of afternoon caffeine response
    - Consumed early enough to avoid sleep disruption
    
    ### 📈 Performance Pattern
    
    This two-coffee approach creates **two distinct productivity peaks** with realistic expectations:
    - **Morning Peak (9:00-10:00):** 82-85% energy - ideal for deep, focused work
    - **Afternoon Peak (16:00):** 70% energy - suitable for lighter tasks and collaboration
    
    The curve demonstrates sustainable energy management, showing the natural decline in caffeine effectiveness throughout the day without the crashes that come from overcaffeination.
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Author Section
# -----------------------------
st.markdown("<div class='author-section'>", unsafe_allow_html=True)

st.markdown(
    """
    <p class='author-label'>PRESENTED BY</p>
    <p class='author-name'>MOHAMED BOUSSOFFARA</p>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

