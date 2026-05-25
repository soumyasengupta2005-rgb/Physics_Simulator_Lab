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

# ---- PLOTLY THEME ----
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(5,10,16,0)",
    plot_bgcolor="rgba(10,22,36,0.6)",
    font=dict(color="#7a9bb5"),
)

# ---- TITLE ----
st.markdown("<p class='page-title'>Damped Harmonic Oscillator</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Explore damping regimes and motion behavior.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    m = st.slider("Mass (m)", 0.5, 10.0, 2.0)
    k = st.slider("Spring Constant (k)", 0.5, 20.0, 5.0)

with col2:
    b = st.slider("Damping Coefficient (b)", 0.0, 20.0, 1.0)
    A = st.slider("Amplitude (A)", 0.5, 5.0, 2.0)

# ---- TOGGLE ----
compare_modes = st.checkbox("Compare All Damping Regimes")

# ---- TIME ----
t = np.linspace(0, 20, 800)

# ---- PHYSICS ----
gamma = b / (2 * m)
omega0 = np.sqrt(k / m)
b_critical = np.sqrt(4 * m * k)

# ---- MAIN CURVE ----
if b**2 < 4*m*k:
    omega = np.sqrt(omega0**2 - gamma**2)
    x_main = A * np.exp(-gamma * t) * np.cos(omega * t)
    regime = "Underdamped → Oscillatory motion"

elif abs(b**2 - 4*m*k) < 0.01:
    x_main = A * np.exp(-gamma * t)
    regime = "Critical damping → Fastest return"

else:
    x_main = A * np.exp(-gamma * t)
    regime = "Overdamped → Slow return"

# ---- COMPARISON CURVES ----
if compare_modes:
    b_u = 0.5 * b_critical
    gamma_u = b_u / (2 * m)
    omega_u = np.sqrt(omega0**2 - gamma_u**2)
    x_under = A * np.exp(-gamma_u * t) * np.cos(omega_u * t)

    gamma_c = b_critical / (2 * m)
    x_critical = A * np.exp(-gamma_c * t)

    b_o = 2 * b_critical
    gamma_o = b_o / (2 * m)
    x_over = A * np.exp(-gamma_o * t)

# ---- PLOT ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t, y=x_main,
    name="Current System",
    line=dict(color="#38a3d1", width=3)
))

if compare_modes:
    fig.add_trace(go.Scatter(x=t, y=x_under, name="Underdamped", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=t, y=x_critical, name="Critical", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=t, y=x_over, name="Overdamped", line=dict(dash="dot")))

fig.update_layout(
    title="Displacement vs Time",
    xaxis_title="Time",
    yaxis_title="Displacement",
    **PLOTLY_THEME
)

st.plotly_chart(fig, use_container_width=True)

# ---- EXPLANATION ----
st.markdown("<p class='section-label'>Regime</p>", unsafe_allow_html=True)
st.markdown(f"<div class='info-box'>{regime}</div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()
ax.plot(t, x_main)
fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Oscillator Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Parameter", "Value"],
        ["Mass", m],
        ["k", k],
        ["b", b],
    ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

# ---- SPACING FIX ----
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ---- DOWNLOAD BUTTONS ----
col1, col2 = st.columns(2)

with col1:
    st.download_button("⬇ Download Graph", img_buf, "oscillator.png")

with col2:
    st.download_button("⬇ Download Report (PDF)", pdf, "oscillator.pdf")