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
        borderwidth=1, font=dict(color="#7a9bb5"),
    ),
    margin=dict(l=40, r=20, t=50, b=40),
)

# ---- TITLE ----
st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<p class='page-title'>PV Diagram Comparison</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Compare thermodynamic processes and understand work done by a gas.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    P1 = st.slider("Initial Pressure", 1.0, 10.0, 5.0)
    V1 = st.slider("Initial Volume", 1.0, 10.0, 3.0)

with col2:
    gamma = st.slider("Gamma (Adiabatic)", 1.1, 1.7, 1.4)

# ---- PROCESS SELECTION ----
col3, col4 = st.columns(2)

with col3:
    process1 = st.selectbox("Process 1", ["Isothermal", "Adiabatic", "Isobaric", "Isochoric"])

with col4:
    process2 = st.selectbox("Process 2", ["Isothermal", "Adiabatic", "Isobaric", "Isochoric"], index=1)

# ---- VOLUME ----
V_max = st.slider("Final Volume", V1 + 0.5, 20.0, V1 * 2)
V = np.linspace(V1, V_max, 400)

# ---- PROCESS FUNCTION ----
def compute_process(process, V, P1, V1, gamma):
    if process == "Isothermal":
        k = P1 * V1
        P = k / V
        work = k * np.log(V[-1] / V1)
    elif process == "Adiabatic":
        k = P1 * (V1 ** gamma)
        P = k / (V ** gamma)
        work = (P1 * V1 - P[-1] * V[-1]) / (gamma - 1)
    elif process == "Isobaric":
        P = np.full_like(V, P1)
        work = P1 * (V[-1] - V1)
    else:
        V = np.full_like(V, V1)
        P = np.linspace(P1, P1 * 3, len(V))
        work = 0
    return V, P, work

# ---- COMPUTE ----
V1_plot, P1_plot, work1 = compute_process(process1, V, P1, V1, gamma)
V2_plot, P2_plot, work2 = compute_process(process2, V, P1, V1, gamma)

# ---- PLOT ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=V1_plot, y=P1_plot, name=process1,
    line=dict(color="#38a3d1", width=3),
))
fig.add_trace(go.Scatter(
    x=V2_plot, y=P2_plot, name=process2,
    line=dict(color="#f0a05a", width=3, dash="dash"),
))

fig.update_layout(
    title="Pressure vs Volume",
    xaxis_title="Volume",
    yaxis_title="Pressure",
    **PLOTLY_THEME,
)

st.plotly_chart(fig, use_container_width=True)

# ---- PROCESS DETAILS ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Process Details</p>", unsafe_allow_html=True)

colA, colB = st.columns(2)

with colA:
    st.markdown(f"<div class='info-box'><b>{process1}</b><br>Final Volume: {V1_plot[-1]:.2f} &nbsp;·&nbsp; ΔV: {(V1_plot[-1] - V1):.2f} &nbsp;·&nbsp; Work: {work1:.2f}</div>", unsafe_allow_html=True)

with colB:
    st.markdown(f"<div class='info-box'><b>{process2}</b><br>Final Volume: {V2_plot[-1]:.2f} &nbsp;·&nbsp; ΔV: {(V2_plot[-1] - V1):.2f} &nbsp;·&nbsp; Work: {work2:.2f}</div>", unsafe_allow_html=True)

# ---- EQUATIONS ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Key Equations</p>", unsafe_allow_html=True)

def get_eq(p):
    return {
        "Isothermal": r"PV = \text{constant}",
        "Adiabatic":  r"PV^\gamma = \text{constant}",
        "Isobaric":   r"P = \text{constant}",
        "Isochoric":  r"V = \text{constant}",
    }[p]

colC, colD = st.columns(2)

with colC:
    st.latex(get_eq(process1))

with colD:
    st.latex(get_eq(process2))

# ---- INSIGHT ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

if process1 == process2:
    insight = "Both processes are identical, so curves overlap."
elif "Adiabatic" in [process1, process2] and "Isothermal" in [process1, process2]:
    insight = "Adiabatic is steeper because no heat exchange occurs."
else:
    insight = "Different thermodynamic constraints create different curve behavior."

st.markdown(f"<div class='info-box'>{insight}</div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()
ax.plot(V1_plot, P1_plot, label=process1)
ax.plot(V2_plot, P2_plot, label=process2)
ax.legend()
fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)
img_bytes = img_buf.getvalue()

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("PV Diagram Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    table_data = [
        ["Parameter", "Value"],
        ["Initial Pressure", f"{P1:.2f}"],
        ["Initial Volume", f"{V1:.2f}"],
        ["Final Volume", f"{V_max:.2f}"],
        ["Gamma", f"{gamma:.2f}"],
        ["Process 1", process1],
        ["Process 2", process2],
        ["Work 1", f"{work1:.2f}"],
        ["Work 2", f"{work2:.2f}"],
    ]
    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))
    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))
    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()
pdf_bytes = pdf.getvalue()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
colE, colF = st.columns(2)

with colE:
    st.download_button("⬇ Download Graph", data=img_bytes, file_name="pv_graph.png", mime="image/png")

with colF:
    st.download_button("⬇ Download Report (PDF)", data=pdf_bytes, file_name="pv_report.pdf", mime="application/pdf")