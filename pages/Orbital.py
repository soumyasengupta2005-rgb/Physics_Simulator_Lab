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
st.markdown("<p class='page-title'>Orbital Motion</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Simulate motion under gravity</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    M = st.slider("Mass (M)", 10.0, 1000.0, 200.0)
    r = st.slider("Initial Distance", 1.0, 10.0, 5.0)

with col2:
    v = st.slider("Initial Velocity", 0.1, 20.0, 6.3)
    steps = st.slider("Simulation Steps", 1000, 6000, 3000)

G = 1.0
dt = 0.002

# ---- INITIAL CONDITIONS ----
x, y = r, 0
vx, vy = 0, v

xs, ys = [], []

# ---- VELOCITY VERLET ----
for _ in range(steps):
    dist = np.sqrt(x**2 + y**2)
    if dist == 0:
        break

    ax1 = -G * M * x / dist**3
    ay1 = -G * M * y / dist**3

    x += vx * dt + 0.5 * ax1 * dt**2
    y += vy * dt + 0.5 * ay1 * dt**2

    dist_new = np.sqrt(x**2 + y**2)

    ax2 = -G * M * x / dist_new**3
    ay2 = -G * M * y / dist_new**3

    vx += 0.5 * (ax1 + ax2) * dt
    vy += 0.5 * (ay1 + ay2) * dt

    xs.append(x)
    ys.append(y)

# ---- SAFETY ----
if len(xs) < 10:
    st.warning("Simulation too short.")
    st.stop()

# ---- DOWNSAMPLE FOR FAST ANIMATION ----
max_frames = 250
step_skip = max(1, len(xs) // max_frames)

xs_anim = xs[::step_skip]
ys_anim = ys[::step_skip]

# ---- FRAMES ----
frames = []
for i in range(2, len(xs_anim)):
    frames.append(go.Frame(
        name=str(i),
        data=[
            go.Scatter(x=xs_anim[:i], y=ys_anim[:i]),
            go.Scatter(x=[xs_anim[i]], y=[ys_anim[i]])
        ]
    ))

# ---- FIGURE ----
fig = go.Figure(
    data=[
        go.Scatter(
            x=[xs_anim[0]], y=[ys_anim[0]],
            mode="lines",
            line=dict(color="#38a3d1", width=2),
            name="Orbit"
        ),
        go.Scatter(
            x=[xs_anim[0]], y=[ys_anim[0]],
            mode="markers",
            marker=dict(size=10, color="#7ec8e3"),
            name="Particle"
        ),
        go.Scatter(
            x=[0], y=[0],
            mode="markers",
            marker=dict(size=14, color="#f0c05a"),
            name="Central Body"
        )
    ],
    frames=frames
)

# ---- AXIS ----
limit = max(10, max(np.abs(xs)) * 1.2)

fig.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 25, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [
                    [frames[0].name if frames else None],
                    {
                        "frame": {"duration": 0, "redraw": True},
                        "mode": "immediate"
                    }
                ]
            }
        ]
    }],
    xaxis=dict(range=[-limit, limit], scaleanchor="y"),
    yaxis=dict(range=[-limit, limit]),
    plot_bgcolor="rgba(10,22,36,0.6)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7a9bb5"),
    showlegend=True,
    title="Orbital Motion (Animated)"
)

st.plotly_chart(fig, use_container_width=True)

# ---- INSIGHT ----
v_orbit = np.sqrt(G * M / r)

st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

if v < v_orbit * 0.85:
    insight = "Velocity too low → spirals inward."
elif abs(v - v_orbit) < 0.5:
    insight = "Velocity near ideal → stable orbit."
else:
    insight = "Velocity too high → escape trajectory."

st.markdown(f"<div class='info-box'>{insight}</div>", unsafe_allow_html=True)

# ---- STATIC GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(xs, ys, label="Orbit")
ax.scatter(0, 0, label="Central Body")
ax.set_aspect("equal")
ax.legend()

fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Orbital Motion Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Parameter", "Value"],
        ["Mass", f"{M:.2f}"],
        ["Distance", f"{r:.2f}"],
        ["Velocity", f"{v:.2f}"],
        ["Orbital Velocity", f"{v_orbit:.2f}"],
    ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

col1, col2 = st.columns(2)

with col1:
    st.download_button("Download Graph", img_buf, "orbit.png")

with col2:
    st.download_button("Download Report (PDF)", pdf, "orbit_report.pdf")