import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os
import io
import matplotlib.pyplot as plt

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
st.markdown("<p class='page-title'>Fourier Series</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Build complex waves from simple sine functions.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
col1, col2 = st.columns(2)

with col1:
    N = st.slider("Number of Terms", 1, 25, 7)

with col2:
    speed = st.slider("Animation Speed", 50, 400, 180)

wave_type = st.selectbox("Wave Type", ["Square", "Sawtooth", "Triangle"])
show_components = st.checkbox("Show Individual Waves")

# ---- DOMAIN ----
x = np.linspace(-np.pi, np.pi, 500)

# ---- TARGET FUNCTIONS ----
if wave_type == "Square":
    y_true = np.sign(np.sin(x))
elif wave_type == "Sawtooth":
    y_true = x / np.pi
elif wave_type == "Triangle":
    y_true = (8 / np.pi**2) * np.sum([
    ((-1)**(n-1) / ((2*n-1)**2)) * np.sin((2*n-1) * x)
    for n in range(1, 50)
    ], axis=0)

# ---- FOURIER SERIES ----
def fourier_series(x, n_terms):
    y = np.zeros_like(x)
    components = []

    for n in range(1, n_terms + 1):
        if wave_type == "Square":
            k = 2*n - 1
            term = (4 / (np.pi * k)) * np.sin(k * x)

        elif wave_type == "Sawtooth":
            k = n
            term = (2 / np.pi) * ((-1)**(n+1) / k) * np.sin(k * x)

        elif wave_type == "Triangle":
            k = 2*n - 1
            term = (8 / (np.pi**2)) * ((-1)**(n-1) / (k**2)) * np.sin(k * x)

        y += term
        components.append(term)

    return y, components

# ---- ANIMATION ----
frames = []

for i in range(1, N + 1):
    y_approx, comps = fourier_series(x, i)

    data = []

    # ---- MAIN APPROXIMATION ----
    data.append(go.Scatter(
        x=x,
        y=y_approx,
        mode="lines",
        line=dict(color="#38a3d1", width=3),
        name="Approximation"
    ))

    # ---- TARGET ----
    data.append(go.Scatter(
        x=x,
        y=y_true,
        mode="lines",
        line=dict(color="#f0a05a", dash="dash"),
        name="Target"
    ))

    # ---- COMPONENTS ----
    if show_components:
        for c in comps:
            data.append(go.Scatter(
                x=x,
                y=c,
                mode="lines",
                line=dict(width=1),
                opacity=0.3,
                showlegend=False
            ))

    frames.append(go.Frame(data=data, name=str(i)))

# ---- FIG ----
fig = go.Figure(
    data=frames[0].data,
    frames=frames
)

# ---- DISCONTINUITY LINE ----
fig.add_vline(x=0, line_dash="dot", line_color="white", opacity=0.3)

fig.update_layout(
    title=f"{wave_type} Wave Approximation",
    xaxis_title="x",
    yaxis_title="f(x)",
    plot_bgcolor="rgba(10,22,36,0.8)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7ec8e3"),
    showlegend=True,
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": speed, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [["1"], {
                    "mode": "immediate",
                    "frame": {"duration": 0}
                }]
            }
        ]
    }]
)

st.plotly_chart(fig, use_container_width=True)

# ---- INSIGHT ----
st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='info-box'>
• {wave_type} wave built from sine waves<br>
• More terms → better approximation<br>
• Overshoot near jumps = <b>Gibbs phenomenon</b><br><br>

👉 You're literally watching frequency components combine
</div>
""", unsafe_allow_html=True)

# ---- STATIC GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

y_final, _ = fourier_series(x, N)

ax.plot(x, y_final, label=f"Approximation (N={N})")
ax.plot(x, y_true, linestyle="--", label="Target")

ax.set_title(f"{wave_type} Wave Fourier Approximation")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
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

    # ---- TITLE ----
    elements.append(Paragraph("Fourier Series Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # ---- TABLE ----
    table_data = [
        ["Parameter", "Value"],
        ["Wave Type", wave_type],
        ["Number of Terms", N],
    ]

    elements.append(Table(table_data))
    elements.append(Spacer(1, 20))

    # ---- FORMULA SECTION ----
    elements.append(Paragraph("Fourier Series Formula Used:", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if wave_type == "Square":
        formula = "f(x) = (4/π) [ sin(x) + (1/3)sin(3x) + (1/5)sin(5x) + ... ]"

    elif wave_type == "Sawtooth":
        formula = "f(x) = (2/π) [ sin(x) - (1/2)sin(2x) + (1/3)sin(3x) - ... ]"

    elif wave_type == "Triangle":
        formula = "f(x) = (8/π²) [ sin(x) - (1/9)sin(3x) + (1/25)sin(5x) - ... ]"

    elements.append(Paragraph(formula, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # ---- IMAGE ----
    img_buf.seek(0)
    elements.append(Image(img_buf, width=400, height=250))

    doc.build(elements)
    buf.seek(0)
    return buf

pdf = create_pdf()

# ---- DOWNLOAD ----
col1, col2 = st.columns(2)

with col1:
    st.download_button("Download Graph", img_buf, "fourier_graph.png")

with col2:
    st.download_button("Download Report (PDF)", pdf, "fourier_report.pdf")