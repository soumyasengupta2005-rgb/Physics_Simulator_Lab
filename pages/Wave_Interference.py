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

# ---- TITLE ----
st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<p class='page-title'>Wave Interference</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Visualize how waves combine to form interference patterns.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- CONTROLS ----
col1, col2 = st.columns(2)

with col1:
    A1 = st.slider("Amplitude 1", 0.5, 5.0, 2.0)
    f1 = st.slider("Frequency 1", 0.5, 5.0, 1.0)

with col2:
    A2 = st.slider("Amplitude 2", 0.5, 5.0, 2.0)
    f2 = st.slider("Frequency 2", 0.5, 5.0, 1.5)

phase = st.slider("Phase Difference", 0.0, 2*np.pi, 0.0)

# ---- PRESETS ----
preset = st.selectbox("Preset", ["Custom", "Constructive", "Destructive", "Beats"])

if preset == "Constructive":
    phase = 0
elif preset == "Destructive":
    phase = np.pi
elif preset == "Beats":
    f1, f2 = 1.0, 1.1

# ---- SPEED CONTROL ----
speed = st.slider("Animation Speed", 20, 150, 80)

# ---- SPACE ----
x = np.linspace(0, 10, 200)

# ---- INITIAL ----
y1 = A1 * np.sin(2 * np.pi * f1 * x)
y2 = A2 * np.sin(2 * np.pi * f2 * x + phase)
y = y1 + y2

# ---- ANIMATION FRAMES ----
frames = []
t_vals = np.linspace(0, 8, 50)

for t in t_vals:
    y1_t = A1 * np.sin(2 * np.pi * f1 * (x - t))
    y2_t = A2 * np.sin(2 * np.pi * f2 * (x - t) + phase)
    y_t = y1_t + y2_t

    frames.append(go.Frame(
        data=[
            go.Scattergl(x=x, y=y1_t),
            go.Scattergl(x=x, y=y2_t),
            go.Scattergl(x=x, y=y_t),
        ]
    ))

# ---- FIGURE ----
fig = go.Figure(
    data=[
        go.Scattergl(x=x, y=y1, name="Wave 1",
                     line=dict(color="#38a3d1", width=2, dash="dot")),
        go.Scattergl(x=x, y=y2, name="Wave 2",
                     line=dict(color="#f0a05a", width=2, dash="dot")),
        go.Scattergl(x=x, y=y, name="Resultant",
                     line=dict(color="#a3e6b0", width=3)),
    ],
    frames=frames,
)

fig.update_layout(
    autosize=True,
    updatemenus=[{
        "type": "buttons",
        "bgcolor": "rgba(10,22,36,0.9)",
        "bordercolor": "rgba(56,163,209,0.3)",
        "font": {"color": "#7ec8e3", "family": "DM Sans"},
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": speed, "redraw": True},
                    "transition": {"duration": speed/2, "easing": "linear"},
                    "fromcurrent": True,
                    "mode": "immediate",
                }],
            },
            {
                "label": "⏸ Pause",
                "method": "animate",
                "args": [[None], {
                    "frame": {"duration": 0},
                    "mode": "immediate",
                }],
            },
        ],
    }],
    xaxis_title="Position",
    yaxis_title="Amplitude",
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
    plot_bgcolor="rgba(10,22,36,0.6)",
    paper_bgcolor="rgba(5,10,16,0)",
    font=dict(family="DM Sans, sans-serif", color="#7a9bb5"),
    margin=dict(l=40, r=20, t=50, b=40),
)

st.plotly_chart(fig, use_container_width=True)

# ---- INSIGHT ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

if abs(phase) < 0.1:
    insight = "Constructive interference: waves reinforce each other."
elif abs(phase - np.pi) < 0.1:
    insight = "Destructive interference: waves cancel each other."
else:
    insight = "Partial interference depending on phase."

st.markdown(f"<div class='info-box'>{insight}</div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(x, y1, label="Wave 1")
ax.plot(x, y2, label="Wave 2")
ax.plot(x, y, label="Resultant", linewidth=2.5)
ax.set_title("Wave Interference")
ax.set_xlabel("Position")
ax.set_ylabel("Amplitude")
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
    elements.append(Paragraph("Wave Interference Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    table_data = [
        ["Parameter", "Value"],
        ["Amplitude 1", f"{A1:.2f}"],
        ["Amplitude 2", f"{A2:.2f}"],
        ["Frequency 1", f"{f1:.2f}"],
        ["Frequency 2", f"{f2:.2f}"],
        ["Phase Difference", f"{phase:.2f}"],
    ]
    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Insight: {insight}", styles["Normal"]))
    elements.append(Spacer(1, 20))
    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))
    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()
pdf_bytes = pdf.getvalue()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
col_dl1, col_dl2 = st.columns(2)

with col_dl1:
    st.download_button("⬇ Download Graph", data=img_bytes, file_name="wave.png")

with col_dl2:
    st.download_button("⬇ Download Report (PDF)", data=pdf_bytes, file_name="wave_report.pdf")