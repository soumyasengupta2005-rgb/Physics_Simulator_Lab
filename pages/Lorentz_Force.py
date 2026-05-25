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

# ---- HEADER ----
st.markdown("<p class='page-title'>Lorentz Force Simulation</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Motion of a charged particle in a magnetic field</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- CONTROLS ----
col1, col2, col3 = st.columns(3)

with col1:
    q = st.slider("Charge (q)", -5.0, 5.0, 1.0)

with col2:
    v = st.slider("Velocity (v)", 0.5, 5.0, 2.0)

with col3:
    B = st.slider("Magnetic Field (B)", 0.0, 5.0, 1.0)

show_vectors = st.checkbox("Show vectors", value=True)

# ---- PHYSICS ----
m = 1

if B != 0 and q != 0:
    omega = (q * B) / m
    r = v / abs(omega)
else:
    omega = 0
    r = 0

# ---- METRICS ----
colA, colB = st.columns(2)

with colA:
    st.metric("Radius (r)", f"{r:.2f}")

with colB:
    st.metric("Angular Velocity (ω)", f"{omega:.2f}")

direction = "Clockwise" if omega < 0 else "Anticlockwise"

st.markdown(f"""
<div class='info-box'>
Direction of motion: <b>{direction}</b>
</div>
""", unsafe_allow_html=True)

# ---- SAMPLING ----
scale = min(5, max(1, abs(omega)))
num_points = int(150 * scale)

theta_max = 4 * np.pi
t_max = theta_max / (abs(omega) + 1e-6)

t_vals = np.linspace(0, t_max, num_points)

# ---- ANIMATION ----
frames = []
x_path = []
y_path = []

for i, t in enumerate(t_vals):

    if B == 0 or q == 0:
        x = v * t
        y = 0
        vx, vy = v, 0
    else:
        x = r * np.cos(omega * t)
        y = r * np.sin(omega * t)

        vx = -r * omega * np.sin(omega * t)
        vy = r * omega * np.cos(omega * t)

    fx = -vy
    fy = vx

    scale_v = max(v, 1)

    vx_n = vx / scale_v
    vy_n = vy / scale_v
    fx_n = fx / scale_v
    fy_n = fy / scale_v

    x_path.append(x)
    y_path.append(y)

    frame_data = [
        go.Scatter(x=x_path.copy(), y=y_path.copy()),
        go.Scatter(x=[x], y=[y])
    ]

    if show_vectors:
        frame_data.extend([
            go.Scatter(x=[x, x + vx_n], y=[y, y + vy_n]),
            go.Scatter(x=[x, x + fx_n], y=[y, y + fy_n])
        ])

    frames.append(go.Frame(
        name=str(i),
        data=frame_data
    ))

# ---- FIGURE ----
base_traces = [
    go.Scatter(x=[0], y=[0], mode="lines", line=dict(color="#38a3d1", width=2)),
    go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=10, color="red"))
]

if show_vectors:
    base_traces.extend([
        go.Scatter(x=[0, 0], y=[0, 0], mode="lines", line=dict(color="white", width=2)),
        go.Scatter(x=[0, 0], y=[0, 0], mode="lines", line=dict(color="red", width=2))
    ])

fig = go.Figure(data=base_traces, frames=frames)

limit = max(10, r * 1.2)
frame_duration = max(20, 200 / scale)

fig.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": frame_duration, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [
                    ["0"],
                    {
                        "frame": {"duration": 0, "redraw": True},
                        "mode": "immediate"
                    }
                ]
            }
        ]
    }],
    xaxis=dict(range=[-limit, limit]),
    yaxis=dict(range=[-limit, limit]),
    plot_bgcolor="rgba(10,22,36,0.6)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7a9bb5"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ---- LEGEND ----
st.markdown("""
<div style='color:#7ec8e3; font-size:13px'>
<b>Legend:</b><br>
<span style='color:white'>White → Velocity</span><br>
<span style='color:red'>Red → Magnetic Force</span>
</div>
""", unsafe_allow_html=True)

# ---- INSIGHT ----
st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

if B == 0:
    insight = "No magnetic field → straight line motion."
elif q == 0:
    insight = "No charge → no magnetic force."
else:
    insight = "Magnetic force is perpendicular to velocity → circular motion."

st.markdown(f"<div class='info-box'>{insight}</div>", unsafe_allow_html=True)

# ---- STATIC GRAPH ----
t_static = np.linspace(0, t_max, 400)

if B == 0 or q == 0:
    x_static = v * t_static
    y_static = np.zeros_like(t_static)
else:
    x_static = r * np.cos(omega * t_static)
    y_static = r * np.sin(omega * t_static)

img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(x_static, y_static, label="Path")
ax.scatter(x_static[-1], y_static[-1], color="red", label="Final Position")

ax.set_title("Lorentz Motion")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()

fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Lorentz Force Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Parameter", "Value"],
        ["Charge (q)", f"{q:.2f}"],
        ["Velocity (v)", f"{v:.2f}"],
        ["Magnetic Field (B)", f"{B:.2f}"],
        ["Radius", f"{r:.2f}"],
        ["Angular Velocity", f"{omega:.2f}"],
    ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

# ✅ SAME STRUCTURE AS ORBITAL
col1, col2 = st.columns(2)

with col1:
    st.download_button("Download Graph", img_buf, "lorentz.png")

with col2:
    st.download_button("Download Report (PDF)", pdf, "lorentz_report.pdf")