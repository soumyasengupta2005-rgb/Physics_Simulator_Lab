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


st.markdown("<div style='padding-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("<p class='page-title'>Electric Field (3D)</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Place charges and visualize the resulting electric field in three dimensions.</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUTS ----
num_charges = st.slider("Number of Charges", 1, 5, 2)

charges = []
cols = st.columns(2)

for i in range(num_charges):
    with cols[i % 2]:
        q = st.slider(f"Charge {i+1}", -10.0, 10.0, float(5 if i % 2 == 0 else -5), step=0.1)
        x = st.slider(f"Position X{i+1}", -5.0, 5.0, float(i * 2 - 2), step=0.1)
        y = st.slider(f"Position Y{i+1}", -5.0, 5.0, 0.0, step=0.1)
        charges.append((q, x, y))

# ---- GRID ----
x = np.linspace(-6, 6, 25)
y = np.linspace(-6, 6, 25)
X, Y = np.meshgrid(x, y)

# ---- FIELD ----
Ex, Ey = np.zeros_like(X), np.zeros_like(Y)

for q, x0, y0 in charges:
    dx = X - x0
    dy = Y - y0
    r = np.sqrt(dx**2 + dy**2) + 1e-6
    Ex += q * dx / r**3
    Ey += q * dy / r**3

# ---- NORMALIZE ----
norm = np.sqrt(Ex**2 + Ey**2) + 1e-6
Ex_n = Ex / norm
Ey_n = Ey / norm

E_mag = np.sqrt(Ex**2 + Ey**2)

# ---- PLOT ----
fig = go.Figure()

fig.add_trace(go.Surface(
    x=X, y=Y, z=np.zeros_like(X),
    surfacecolor=E_mag,
    colorscale="Blues",
    showscale=False, opacity=0.5
))

step = 3
fig.add_trace(go.Cone(
    x=X[::step, ::step].flatten(),
    y=Y[::step, ::step].flatten(),
    z=np.zeros_like(X[::step, ::step].flatten()),
    u=Ex_n[::step, ::step].flatten(),
    v=Ey_n[::step, ::step].flatten(),
    w=np.zeros_like(Ex_n[::step, ::step].flatten()),
    sizemode="scaled", sizeref=0.5,
    showscale=False, colorscale="Blues"
))

for q, x0, y0 in charges:
    fig.add_trace(go.Scatter3d(
        x=[x0], y=[y0], z=[0],
        mode="markers+text",
        marker=dict(
            size=10,
            color="red" if q > 0 else "blue",
            line=dict(color="white", width=2)
        ),
        text=[f"{'+' if q > 0 else '-'}{abs(q):.1f}"],
        textposition="top center",
        showlegend=False
    ))
fig.update_layout(
    height=650,
    scene=dict(
        xaxis=dict(range=[-6, 6], gridcolor="rgba(56,163,209,0.08)",
                   backgroundcolor="rgba(10,22,36,0.8)"),
        yaxis=dict(range=[-6, 6], gridcolor="rgba(56,163,209,0.08)",
                   backgroundcolor="rgba(10,22,36,0.8)"),
        zaxis=dict(range=[-2, 2], gridcolor="rgba(56,163,209,0.08)",
                   backgroundcolor="rgba(5,10,16,0.9)"),
        camera=dict(eye=dict(x=1.6, y=1.6, z=1.2)),
        bgcolor="rgba(5,10,16,0)",
    ),
    paper_bgcolor="rgba(5,10,16,0)",
    font=dict(family="DM Sans, sans-serif", color="#7a9bb5"),
    margin=dict(l=0, r=0, t=20, b=0),
)

st.plotly_chart(fig, use_container_width=True)

# ---- INSIGHT ----
st.markdown("<p class='section-label'>Insight</p>", unsafe_allow_html=True)

if len(charges) == 1:
    insight = "Single charge creates a radial field."
elif any(q > 0 for q,_,_ in charges) and any(q < 0 for q,_,_ in charges):
    insight = "Mixed charges create dipole or complex field patterns."
else:
    insight = "Like charges create symmetric repulsion."

st.markdown(f"<div class='info-box'>{insight}</div>", unsafe_allow_html=True)

# ---- SAVE GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.imshow(E_mag, extent=[-6,6,-6,6], origin='lower', cmap='Blues')

for q, x0, y0 in charges:
    ax.scatter(x0, y0, c='red' if q > 0 else 'blue')

fig_mpl.savefig(img_buf, format="png")
img_buf.seek(0)
img_bytes = img_buf.getvalue()

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("Electric Field Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    table_data = [["Charge", "X", "Y"]]
    for q, x0, y0 in charges:
        table_data.append([f"{q:.2f}", f"{x0:.2f}", f"{y0:.2f}"])
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
    st.download_button("⬇ Download Graph", data=img_bytes, file_name="electric_field.png")

with col_dl2:
    st.download_button("⬇ Download Report (PDF)", data=pdf_bytes, file_name="electric_field_report.pdf")