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
st.markdown("<p class='page-title'>🔥 Carnot Engine</p>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>The most efficient heat engine</p>", unsafe_allow_html=True)
st.markdown("<div class='title-divider'></div>", unsafe_allow_html=True)

# ---- INPUT ----
col1, col2 = st.columns(2)

with col1:
    Th = st.slider("Hot Reservoir Temperature (K)", 300, 1000, 600)

with col2:
    Tc = st.slider("Cold Reservoir Temperature (K)", 100, 500, 300)

# ---- EFFICIENCY ----
efficiency = 1 - (Tc / Th)

st.markdown(f"""
<div class='info-box'>
Efficiency: <b>{efficiency*100:.2f}%</b>
</div>
""", unsafe_allow_html=True)

# ---- PV DATA ----
V1, V2 = 1, 3

V_iso1 = np.linspace(V1, V2, 50)
P_iso1 = Th / V_iso1

V_adiabatic1 = np.linspace(V2, V2*1.5, 50)
P_adiabatic1 = P_iso1[-1] * (V_iso1[-1]/V_adiabatic1)**1.4

V_iso2 = np.linspace(V2*1.5, V1*1.5, 50)
P_iso2 = Tc / V_iso2

V_adiabatic2 = np.linspace(V1*1.5, V1, 50)
P_adiabatic2 = P_iso2[-1] * (V_iso2[-1]/V_adiabatic2)**1.4

V_path = np.concatenate([V_iso1, V_adiabatic1, V_iso2, V_adiabatic2])
P_path = np.concatenate([P_iso1, P_adiabatic1, P_iso2, P_adiabatic2])

# ---- ANIMATION FRAMES ----
frames = []
for i in range(5, len(V_path)):
    frames.append(go.Frame(
        name=str(i),
        data=[
            go.Scatter(
                x=V_path[:i],
                y=P_path[:i],
                mode="lines",
                line=dict(color="#38a3d1", width=3)
            ),
            go.Scatter(
                x=[V_path[i]],
                y=[P_path[i]],
                mode="markers",
                marker=dict(size=10, color="white")
            )
        ]
    ))

# ---- FIGURE ----
fig = go.Figure(
    data=frames[0].data,  # 🔥 FIXED RESET ISSUE
    frames=frames
)

# ---- ADD FULL CYCLE + WORK AREA ----
fig.add_trace(go.Scatter(
    x=V_path,
    y=P_path,
    fill="toself",
    fillcolor="rgba(255,127,80,0.15)",
    line=dict(color="#38a3d1", width=2),
    name="Work Done"
))

# ---- HEAT FLOW ANNOTATIONS ----
fig.update_layout(
    annotations=[
        dict(x=V2, y=max(P_iso1), text="Qh (Heat In)", showarrow=True, arrowhead=2, font=dict(color="orange")),
        dict(x=V1*1.4, y=min(P_iso2), text="Qc (Heat Out)", showarrow=True, arrowhead=2, font=dict(color="cyan"))
    ]
)

# ---- LAYOUT ----
fig.update_layout(
    title="Carnot Cycle (P–V Diagram)",
    xaxis_title="Volume",
    yaxis_title="Pressure",
    plot_bgcolor="rgba(10,22,36,0.8)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#7ec8e3"),
    showlegend=False,
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "▶ Play",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 40, "redraw": True},
                    "fromcurrent": True
                }]
            },
            {
                "label": "Reset",
                "method": "animate",
                "args": [
                    [frames[0].name],
                    {"mode": "immediate", "frame": {"duration": 0}}
                ]
            }
        ]
    }]
)

st.plotly_chart(fig, use_container_width=True)

# ---- INSIGHTS ----
st.markdown("<p class='section-label'>Insights</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='info-box'>
• Efficiency depends ONLY on temperatures<br>
• Higher Th → better engine<br>
• Lower Tc → better engine<br><br>

• Area inside loop = <b>Work done</b><br>
• Qh → heat absorbed<br>
• Qc → heat rejected<br><br>

👉 No engine can be more efficient than Carnot.
</div>
""", unsafe_allow_html=True)

# ---- STATIC GRAPH ----
img_buf = io.BytesIO()
fig_mpl, ax = plt.subplots()

ax.plot(V_path, P_path)
ax.fill(V_path, P_path, alpha=0.2)

ax.set_title("Carnot Cycle")
ax.set_xlabel("Volume")
ax.set_ylabel("Pressure")

fig_mpl.savefig(img_buf, format="png")
plt.close(fig_mpl)
img_buf.seek(0)

# ---- PDF ----
def create_pdf():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Carnot Engine Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Hot Temperature", f"{Th} K"],
        ["Cold Temperature", f"{Tc} K"],
        ["Efficiency", f"{efficiency*100:.2f}%"]
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
    st.download_button("Download Graph", img_buf, "carnot_cycle.png")

with col2:
    st.download_button("Download Report (PDF)", pdf, "carnot_report.pdf")