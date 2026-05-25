import streamlit as st
import numpy as np
import plotly.graph_objects as go
import io
import matplotlib.pyplot as plt
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

st.set_page_config(layout="wide")

# ---- LOAD CSS ----
def load_css():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    css_path = os.path.join(base_dir, "styles.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(5,10,16,0)",
    plot_bgcolor="rgba(10,22,36,0.6)",
    font=dict(family="DM Sans, sans-serif", color="#7a9bb5"),
    title_font=dict(family="Syne, sans-serif", color="#d6eaf8", size=18),
    xaxis=dict(
        gridcolor="rgba(56,163,209,0.08)",
        zerolinecolor="rgba(56,163,209,0.15)",
        tickfont=dict(color="#3a5f7a"),
        title_font=dict(color="#5a7f99"),
    ),
    yaxis=dict(
        gridcolor="rgba(56,163,209,0.08)",
        zerolinecolor="rgba(56,163,209,0.15)",
        tickfont=dict(color="#3a5f7a"),
        title_font=dict(color="#5a7f99"),
    ),
    legend=dict(
        bgcolor="rgba(8,18,30,0.8)",
        bordercolor="rgba(56,163,209,0.2)",
        borderwidth=1,
        font=dict(color="#7a9bb5"),
    ),
    margin=dict(l=40, r=20, t=50, b=40),
)

# ---- TITLE ----
st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<p class='page-title'>Maxwell–Boltzmann Distribution</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Compare how particle speeds are distributed in gases at different temperatures.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- MODE ----
compare = st.checkbox("Compare Two Gases")

# ---- VISUAL TOGGLE ----
show_shading = st.checkbox("Show Shading", value=True)

# ---- GAS PRESETS ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Gas Selection</p>", unsafe_allow_html=True)

gas_options = {
    "Custom": None,
    "Helium (He)": 4.0,
    "Nitrogen (N₂)": 28.0,
    "Oxygen (O₂)": 32.0,
    "Argon (Ar)": 40.0
}

col_g1, col_g2 = st.columns(2)

with col_g1:
    gas1 = st.selectbox("Gas 1", list(gas_options.keys()))

with col_g2:
    if compare:
        gas2 = st.selectbox("Gas 2", list(gas_options.keys()))

# ---- CONSTANT ----
k = 1.38e-23

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    T1 = st.slider("Temperature 1 (K)", 100, 1000, 300)

    if gas1 != "Custom":
        m1 = gas_options[gas1] * 1.6605
        st.markdown(f"<p style='font-size:13px; color:#3a5f7a;'>Mass 1: {m1:.2f} ×10⁻²⁶ kg</p>", unsafe_allow_html=True)
    else:
        m1 = st.slider("Mass 1 (×1e-26 kg)", 1.0, 50.0, 4.65)

with col2:
    if compare:
        T2 = st.slider("Temperature 2 (K)", 100, 1000, 600)

        if gas2 != "Custom":
            m2 = gas_options[gas2] * 1.6605
            st.markdown(f"<p style='font-size:13px; color:#3a5f7a;'>Mass 2: {m2:.2f} ×10⁻²⁶ kg</p>", unsafe_allow_html=True)
        else:
            m2 = st.slider("Mass 2 (×1e-26 kg)", 1.0, 50.0, 2.0)

# Convert to kg
m1 *= 1e-26
if compare:
    m2 *= 1e-26

# ---- SPEED RANGE ----
v = np.linspace(0, 2000, 500)

# ---- GAS 1 ----
f1 = 4 * np.pi * (m1 / (2 * np.pi * k * T1))**(3/2) * v**2 * np.exp(-m1 * v**2 / (2 * k * T1))

v_mp1 = np.sqrt(2 * k * T1 / m1)
v_mean1 = np.sqrt(8 * k * T1 / (np.pi * m1))
v_rms1 = np.sqrt(3 * k * T1 / m1)

# ---- PLOT ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=v,
    y=f1,
    name="Gas 1",
    line=dict(color="#38a3d1", width=2.5),
    fill='tozeroy' if show_shading else None,
    fillcolor="rgba(56,163,209,0.1)",
    opacity=0.9,
))

# ---- GAS 2 ----
if compare:
    f2 = 4 * np.pi * (m2 / (2 * np.pi * k * T2))**(3/2) * v**2 * np.exp(-m2 * v**2 / (2 * k * T2))

    v_mp2 = np.sqrt(2 * k * T2 / m2)
    v_mean2 = np.sqrt(8 * k * T2 / (np.pi * m2))
    v_rms2 = np.sqrt(3 * k * T2 / m2)

    fig.add_trace(go.Scatter(
        x=v,
        y=f2,
        name="Gas 2",
        line=dict(color="#f0a05a", width=2.5),
        fill='tozeroy' if show_shading else None,
        fillcolor="rgba(240,160,90,0.08)",
        opacity=0.9,
    ))

fig.update_layout(
    title="Speed Distribution",
    xaxis_title="Speed (m/s)",
    yaxis_title="Probability Density",
    legend_title="Gases",
    **PLOTLY_THEME,
)

st.plotly_chart(fig, use_container_width=True)

# ---- EXPLANATION ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Explanation</p>", unsafe_allow_html=True)

st.markdown(f"<div class='info-box'><b>Gas 1</b><br>Most Probable: {v_mp1:.2f} m/s &nbsp;·&nbsp; Mean: {v_mean1:.2f} m/s &nbsp;·&nbsp; RMS: {v_rms1:.2f} m/s</div>", unsafe_allow_html=True)

if compare:
    st.markdown(f"<div class='info-box'><b>Gas 2</b><br>Most Probable: {v_mp2:.2f} m/s &nbsp;·&nbsp; Mean: {v_mean2:.2f} m/s &nbsp;·&nbsp; RMS: {v_rms2:.2f} m/s</div>", unsafe_allow_html=True)

# ---- KEY RELATION ----
st.markdown("<p class='section-label' style='margin-top:20px;'>Key Relation</p>", unsafe_allow_html=True)
st.markdown("<div class='relation-box'><b>v<sub>mp</sub> &lt; v<sub>mean</sub> &lt; v<sub>rms</sub></b></div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(v, f1, label="Gas 1")

if compare:
    ax.plot(v, f2, label="Gas 2")

ax.legend()
ax.set_xlabel("Speed (m/s)")
ax.set_ylabel("Probability Density")
ax.set_title("Maxwell Distribution")

fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.download_button("⬇ Download Graph", img_buf, "maxwell.png")

# ---- PDF REPORT ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Maxwell-Boltzmann Distribution Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    if compare:
        table_data = [
            ["Parameter", "Gas 1", "Gas 2"],
            ["Temperature (K)", T1, T2],
            ["Mass (kg)", f"{m1:.2e}", f"{m2:.2e}"],
            ["v_mp", f"{v_mp1:.2f}", f"{v_mp2:.2f}"],
            ["v_mean", f"{v_mean1:.2f}", f"{v_mean2:.2f}"],
            ["v_rms", f"{v_rms1:.2f}", f"{v_rms2:.2f}"],
        ]
    else:
        table_data = [
            ["Parameter", "Value"],
            ["Temperature (K)", T1],
            ["Mass (kg)", f"{m1:.2e}"],
            ["v_mp", f"{v_mp1:.2f}"],
            ["v_mean", f"{v_mean1:.2f}"],
            ["v_rms", f"{v_rms1:.2f}"],
        ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    img_buf.seek(0)
    img = Image(img_buf, width=400, height=250)
    elements.append(img)

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

with col_btn2:
    st.download_button("⬇ Download Report (PDF)", pdf, "maxwell_report.pdf")