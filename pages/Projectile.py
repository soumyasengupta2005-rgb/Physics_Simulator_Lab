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
st.markdown("<p class='page-title'>Projectile Motion</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Adjust velocity and angle — watch trajectories form in real time.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- MODES ----
compare = st.checkbox("Compare Mode")
show_explain = st.checkbox("Show Explanation")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    v1 = st.slider("Velocity 1 (m/s)", 10, 100, 50)
    theta1 = st.slider("Angle 1 (degrees)", 0, 90, 45)

with col2:
    if compare:
        v2 = st.slider("Velocity 2 (m/s)", 10, 100, 50)
        theta2 = st.slider("Angle 2 (degrees)", 0, 90, 30)

g = 9.8

# ---- PHYSICS FUNCTION ----
def compute(v, theta):
    theta = np.radians(theta)
    T = (2 * v * np.sin(theta)) / g
    t = np.linspace(0, T, 200)
    x = v * np.cos(theta) * t
    y = v * np.sin(theta) * t - 0.5 * g * t**2
    R = (v**2 * np.sin(2 * theta)) / g
    H = (v**2 * np.sin(theta)**2) / (2 * g)
    return x, y, T, R, H

x1, y1, T1, R1, H1 = compute(v1, theta1)

if compare:
    x2, y2, T2, R2, H2 = compute(v2, theta2)

# ---- ANIMATION (AUTO PLAY + RESET) ----
frames = []

for i in range(2, len(x1)):
    data = [
        go.Scatter(
            x=x1[:i],
            y=y1[:i],
            mode='lines',
            line=dict(color="#38a3d1", width=2.5),
            name='Trajectory 1'
        ),
        go.Scatter(
            x=[x1[i]],
            y=[y1[i]],
            mode='markers',
            marker=dict(size=10, color="white"),
            showlegend=False
        )
    ]

    if compare:
        data.append(go.Scatter(
            x=x2[:i],
            y=y2[:i],
            mode='lines',
            line=dict(color="#f0a05a", width=2.5),
            name='Trajectory 2'
        ))

        data.append(go.Scatter(
            x=[x2[i]],
            y=[y2[i]],
            mode='markers',
            marker=dict(size=10, color="white"),
            showlegend=False
        ))

    frames.append(go.Frame(data=data, name=str(i)))

# ---- INITIAL FIG ----
fig = go.Figure(
    data=frames[0].data,
    frames=frames
)

# ---- CONTROLS ----
fig.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 30, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [[frames[0].name], {
                    "mode": "immediate",
                    "frame": {"duration": 0}
                }]
            }
        ]
    }]
)
# ---- AXIS LOCK ----
x_max = max(x1) * 1.1
y_max = max(y1) * 1.1

if compare:
    x_max = max(x_max, max(x2) * 1.1)
    y_max = max(y_max, max(y2) * 1.1)

fig.update_layout(
    title="Projectile Motion",
    xaxis_title="Distance (m)",
    yaxis_title="Height (m)",
    showlegend=True,
    paper_bgcolor=PLOTLY_THEME["paper_bgcolor"],
    plot_bgcolor=PLOTLY_THEME["plot_bgcolor"],
    font=PLOTLY_THEME["font"],
    title_font=PLOTLY_THEME["title_font"],
    legend=PLOTLY_THEME["legend"],
    margin=PLOTLY_THEME["margin"],
    xaxis={**PLOTLY_THEME["xaxis"], "range": [0, x_max]},
    yaxis={**PLOTLY_THEME["yaxis"], "range": [0, y_max]},
)

st.plotly_chart(fig, use_container_width=True)

# ---- RESULTS ----
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Results</p>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.metric("Time of Flight", f"{T1:.2f} s")
    st.metric("Range", f"{R1:.2f} m")
    st.metric("Max Height", f"{H1:.2f} m")

if compare:
    with col4:
        st.metric("Time (T2)", f"{T2:.2f} s")
        st.metric("Range (T2)", f"{R2:.2f} m")
        st.metric("Max Height (T2)", f"{H2:.2f} m")

# ---- EXPLANATION ----
if show_explain:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Explanation</p>", unsafe_allow_html=True)

    if theta1 == 45:
        st.markdown("<div class='info-box'>Maximum range occurs at 45 degrees.</div>", unsafe_allow_html=True)
    elif theta1 > 45:
        st.markdown("<div class='info-box'>Higher angles increase height but reduce range.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>Lower angles increase range but reduce height.</div>", unsafe_allow_html=True)

    if compare:
        if R1 > R2:
            st.markdown("<div class='info-box'>Trajectory 1 travels farther.</div>", unsafe_allow_html=True)
        elif R2 > R1:
            st.markdown("<div class='info-box'>Trajectory 2 travels farther.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='info-box'>Both trajectories have equal range.</div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

# Trajectory 1
ax.plot(x1, y1, label="Trajectory 1 (v={}, θ={}°)".format(v1, theta1))

# Trajectory 2 (if compare)
if compare:
    ax.plot(x2, y2, label="Trajectory 2 (v={}, θ={}°)".format(v2, theta2))

# ---- LABELS ----
ax.set_title("Projectile Motion")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")

ax.legend()

fig_mpl.savefig(img_buf, format="png")
plt.close(fig_mpl)
img_buf.seek(0)

# ---- PDF REPORT ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Physics Simulation Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Metric", "Trajectory 1", "Trajectory 2" if compare else ""],
        ["Velocity", v1, v2 if compare else ""],
        ["Angle", theta1, theta2 if compare else ""],
        ["Time", f"{T1:.2f}", f"{T2:.2f}" if compare else ""],
        ["Range", f"{R1:.2f}", f"{R2:.2f}" if compare else ""],
        ["Height", f"{H1:.2f}", f"{H2:.2f}" if compare else ""],
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
col_dl1, col_dl2 = st.columns(2)
with col_dl1:
    st.download_button("⬇ Download Graph", img_buf, "graph.png")

with col_dl2:
    st.download_button("⬇ Download Report (PDF)", pdf, "report.pdf")