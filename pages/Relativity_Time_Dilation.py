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
st.markdown("<p class='page-title'>⏳ Time Dilation Lab</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Why moving clocks run slower</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- CONTROLS ----
col1, col2 = st.columns(2)

with col1:
    v = st.slider("Velocity (fraction of speed of light)", 0.0, 0.99, 0.8)

with col2:
    duration = st.slider("Simulation Duration", 5, 20, 10)

# ---- PHYSICS ----
gamma = 1 / np.sqrt(1 - v**2)

st.metric("Lorentz Factor (γ)", f"{gamma:.2f}")

# ---- STORY ----
st.markdown("""
<div class='info-box'>
You are on Earth. Your friend is moving at high speed.<br>
We use a <b>light clock</b> to measure time.<br><br>
Watch what happens 👇
</div>
""", unsafe_allow_html=True)

# ---- LIGHT CLOCK ANIMATION ----
frames = []
t_vals = np.linspace(0, duration, 80)

for i, t in enumerate(t_vals):

    # stationary light (simple up-down)
    y_static = np.sin(2 * np.pi * t)

    # moving light (slower oscillation)
    y_moving = np.sin(2 * np.pi * t / gamma)
    x_moving = v * t

    frames.append(go.Frame(
        name=str(i),
        data=[
            # YOUR CLOCK (left)
            go.Scatter(x=[-2, -2], y=[-1, 1], mode="lines",
                       line=dict(color="#38a3d1", width=4)),
            go.Scatter(x=[-2], y=[y_static], mode="markers",
                       marker=dict(size=10, color="white")),

            # ASTRONAUT CLOCK (moving right)
            go.Scatter(x=[x_moving, x_moving], y=[-1, 1], mode="lines",
                       line=dict(color="#ff7f50", width=4)),
            go.Scatter(x=[x_moving], y=[y_moving], mode="markers",
                       marker=dict(size=10, color="yellow")),
        ]
    ))

# ---- FIGURE ----
fig = go.Figure(
    data=[
        go.Scatter(x=[-2, -2], y=[-1, 1], mode="lines", name="You (Earth)"),
        go.Scatter(x=[-2], y=[0], mode="markers"),

        go.Scatter(x=[0, 0], y=[-1, 1], mode="lines", name="Astronaut"),
        go.Scatter(x=[0], y=[0], mode="markers"),
    ],
    frames=frames
)

fig.update_layout(
    title="Light Clock: The Reason Behind Time Dilation",
    xaxis=dict(range=[-5, 10], visible=False),
    yaxis=dict(range=[-2, 2], visible=False),
    plot_bgcolor="rgba(10,22,36,0.8)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7ec8e3"),
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 60, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [
                    ["0"],
                    {"mode": "immediate"}
                ]
            }
        ]
    }]
)

st.plotly_chart(fig, use_container_width=True)

# ---- EXPLANATION ----
st.markdown("<p class='section-label'>What’s happening?</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='info-box'>
Light always moves at the same speed.<br><br>

But for the moving astronaut:<br>
👉 The light travels a <b>longer diagonal path</b><br>
👉 Same speed + longer distance = more time<br><br>

So the clock ticks slower.<br><br>

<b>γ = {gamma:.2f}</b> → time slows by this factor.
</div>
""", unsafe_allow_html=True)

# ---- STATIC GRAPH ----
t_vals = np.linspace(0, duration, 200)
earth_time = t_vals
ship_time = t_vals / gamma

img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(earth_time, earth_time, label="Earth Time")
ax.plot(earth_time, ship_time, label="Astronaut Time")

ax.set_title("Time Dilation Graph")
ax.legend()

fig_mpl.savefig(img_buf, format="png")
plt.close(fig_mpl)
img_buf.seek(0)

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Time Dilation Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Velocity", f"{v:.2f}c"],
        ["Gamma", f"{gamma:.2f}"],
        ["Duration", f"{duration} s"],
    ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

# ---- DOWNLOAD ----
col1, col2 = st.columns(2)

with col1:
    st.download_button("Download Graph", img_buf, "time_dilation.png")

with col2:
    st.download_button("Download Report (PDF)", pdf, "time_dilation_report.pdf")