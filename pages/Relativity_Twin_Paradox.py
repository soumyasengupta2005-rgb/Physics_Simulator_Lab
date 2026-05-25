import streamlit as st
import numpy as np
import time
import os

st.set_page_config(layout="wide")

# ---- LOAD CSS ----
def load_css():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    css_path = os.path.join(base_dir, "styles.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---- TITLE ----
st.markdown("<p class='page-title'>🚀 Twin Paradox</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Same journey. Different aging.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUT ----
col1, col2 = st.columns(2)

with col1:
    v = st.slider("Velocity (fraction of light speed)", 0.1, 0.99, 0.8)

with col2:
    t_total = st.slider("Total Earth Time (years)", 2, 20, 10)

# ---- PHYSICS ----
gamma = 1 / np.sqrt(1 - v**2)
t_half = t_total / 2

# ---- NEW: RELATIVITY INTENSITY ----
st.markdown(f"""
<div class='info-box'>
Relativity Intensity (γ): <b>{gamma:.2f}</b>
</div>
""", unsafe_allow_html=True)

# ---- UI ----
colA, colB = st.columns(2)
earth_box = colA.empty()
ship_box = colB.empty()

gap_box = st.empty()
distance_box = st.empty()
progress = st.progress(0)

start = st.button("Start Journey")

# ---- ANIMATION ----
if start:

    earth_time = 0
    ship_time = 0
    distance = 0

    steps = 80

    for i in range(steps):

        phase = i / steps
        dt = t_total / steps

        earth_time += dt
        ship_time += dt / gamma

        if i < steps / 2:
            distance += v * dt
        else:
            distance -= v * dt

        # ---- UPDATE UI ----
        earth_box.markdown(f"""
        <div class='stat-box'>
        <span class='stat-number'>{earth_time:.2f}</span>
        <div class='stat-label'>You (Earth) — years</div>
        </div>
        """, unsafe_allow_html=True)

        ship_box.markdown(f"""
        <div class='stat-box'>
        <span class='stat-number'>{ship_time:.2f}</span>
        <div class='stat-label'>Astronaut — years</div>
        </div>
        """, unsafe_allow_html=True)

        gap = earth_time - ship_time
        gap_box.markdown(f"""
        <div class='info-box'>
        Age Difference: <b>{gap:.2f} years</b>
        </div>
        """, unsafe_allow_html=True)

        distance_box.markdown(f"""
        <div class='info-box'>
        Distance from Earth: <b>{abs(distance):.2f} light-years</b>
        </div>
        """, unsafe_allow_html=True)

        progress.progress(phase)

        # ---- IMPROVED TURNAROUND ----
        if i == steps // 2:
            st.warning("🔄 TURNAROUND POINT — Motion changes frame")

        time.sleep(0.04)

    # ---- FINAL MOMENT ----
    st.markdown("<p class='section-label'>Reunion</p>", unsafe_allow_html=True)

    final_gap = earth_time - ship_time

    st.error("❗ They meet again… but not the same age.")

    # ---- NEW: STRONGER END IMPACT ----
    st.markdown(f"""
    <div class='info-box'>
    You aged <b>{earth_time:.2f} years</b><br>
    Astronaut aged <b>{ship_time:.2f} years</b><br><br>

    <span style="font-size:22px; color:#ff7f50;">
    Age Gap: {final_gap:.2f} years
    </span><br><br>

    👉 The astronaut is younger.<br><br>

    <b>This is not an illusion.</b><br>
    <b>This actually happens in relativity.</b><br>
    <b>This is the TWIN PARADOX.</b>
    </div>
    """, unsafe_allow_html=True)