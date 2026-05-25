import streamlit as st

st.set_page_config(layout="wide", page_title="Physics Playground")

# ---- GLOBAL STYLES ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0d1b2a 0%, #050a10 60%);
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: rgba(8,18,30,0.95) !important;
    border-right: 1px solid rgba(56,163,209,0.1);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(48px, 7vw, 88px); font-weight: 800;
    line-height: 1.05; letter-spacing: -2px; text-align: center;
    background: linear-gradient(135deg, #e8f4fd 30%, #7ec8e3 65%, #38a3d1 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 18px 0;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif; font-weight: 300;
    font-size: 18px; color: #7a9bb5; text-align: center;
    letter-spacing: 0.3px; margin: 0 auto 8px; max-width: 480px;
}
.accent-line {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, #38a3d1, transparent);
    margin: 22px auto 48px; border-radius: 2px;
}
.section-label {
    font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 500;
    letter-spacing: 3px; text-transform: uppercase;
    color: #38a3d1; margin-bottom: 10px;
}
.section-heading {
    font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 700;
    color: #d6eaf8; margin: 0 0 32px 0; letter-spacing: -0.5px;
}
.sim-card {
    border-radius: 16px 16px 0 0;
    padding: 28px 24px 20px;
    background: linear-gradient(145deg, rgba(22,42,60,0.9), rgba(8,20,34,0.95));
    border: 1px solid rgba(56,163,209,0.15);
    border-bottom: none;
    position: relative; overflow: hidden;
    transition: border-color 0.3s ease;
}
.sim-card:hover { border-color: rgba(56,163,209,0.45); }
.sim-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #38a3d1, transparent);
    opacity: 0.6;
}
.card-icon { font-size: 28px; margin-bottom: 14px; display: block; }
.card-title {
    font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700;
    color: #d6eaf8; margin: 0 0 8px 0; letter-spacing: -0.2px;
}
.card-desc {
    font-family: 'DM Sans', sans-serif; font-size: 13px;
    color: #5a7f99; margin: 0; line-height: 1.55;
}
div[data-testid="stButton"] button {
    width: 100% !important;

    background: rgba(56, 163, 209, 0.08) !important;
    border: 1px solid rgba(56, 163, 209, 0.35) !important;
    border-radius: 10px !important;

    margin-top: 8px !important;               

    color: #7ec8e3 !important;

    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;

    letter-spacing: 0.5px !important;
    text-transform: none !important;

    padding: 12px 0 !important;
}

div[data-testid="stButton"] button:hover {
    background: rgba(56, 163, 209, 0.18) !important;
    border-color: rgba(56, 163, 209, 0.6) !important;
    color: #e8f4fd !important;
}
.stat-box {
    text-align: center; padding: 20px 10px; border-radius: 12px;
    background: rgba(14,30,46,0.7); border: 1px solid rgba(56,163,209,0.1);
}
.stat-number {
    font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800;
    color: #38a3d1; display: block; letter-spacing: -1px;
}
.stat-label {
    font-family: 'DM Sans', sans-serif; font-size: 12px; color: #4a6a82;
    letter-spacing: 1px; text-transform: uppercase; margin-top: 4px;
}
.feature-item {
    display: flex; align-items: flex-start; gap: 12px; padding: 12px 0;
    border-bottom: 1px solid rgba(56,163,209,0.07);
    font-family: 'DM Sans', sans-serif; font-size: 15px;
    color: #7a9bb5; line-height: 1.5;
}
.feature-item:last-child { border-bottom: none; }
.feature-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #38a3d1; margin-top: 8px; flex-shrink: 0;
}
.footer {
    text-align: center; font-family: 'DM Sans', sans-serif;
    font-size: 13px; color: #2e4d63; padding: 28px 0 12px; letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)


# ---- HERO ----
st.markdown("<div style='padding: 64px 0 0;'></div>", unsafe_allow_html=True)
st.markdown("""
<h1 class='hero-title'>Physics Playground</h1>
<p class='hero-sub'>Learn physics visually. Experiment freely. Understand deeply.</p>
<div class='accent-line'></div>
""", unsafe_allow_html=True)


# ---- STATS ROW ----
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown("<div class='stat-box'><span class='stat-number'>12</span><div class='stat-label'>Simulations</div></div>", unsafe_allow_html=True)
with s2:
    st.markdown("<div class='stat-box'><span class='stat-number'>∞</span><div class='stat-label'>Parameter combos</div></div>", unsafe_allow_html=True)
with s3:
    st.markdown("<div class='stat-box'><span class='stat-number'>2D/3D</span><div class='stat-label'>Live visualization</div></div>", unsafe_allow_html=True)
with s4:
    st.markdown("<div class='stat-box'><span class='stat-number'>PDF</span><div class='stat-label'>Report export</div></div>", unsafe_allow_html=True)

st.markdown("<div style='padding: 48px 0 0;'></div>", unsafe_allow_html=True)


# ---- SIMULATIONS HEADING ----
st.markdown("""
<p class='section-label'>Simulations</p>
<h2 class='section-heading'>Pick a module to explore</h2>
""", unsafe_allow_html=True)


# ---- SIMULATION CARDS ----
def sim_card(icon, title, desc):
    return f"""<div class='sim-card'>
        <span class='card-icon'>{icon}</span>
        <p class='card-title'>{title}</p>
        <p class='card-desc'>{desc}</p>
    </div>"""

cards = [
    ("🎯", "Projectile Motion",
     "Adjust velocity and angle, compare trajectories, and watch physics unfold in real time.",
     "pages/Projectile.py"),
    ("🪐", "Orbital Motion",
     "Simulate gravitational systems and explore stable orbits vs. escape velocities.",
     "pages/Orbital.py"),
    ("〰️", "Wave Interference",
     "Tune frequency, amplitude, and phase to observe constructive interference and beats.",
     "pages/Wave_Interference.py"),
    ("⚗️", "Maxwell Distribution",
     "Compare how gas particles distribute across speeds at different temperatures.",
     "pages/Maxwell.py"),
    ("🌡️", "PV Diagrams",
     "Compare thermodynamic processes and understand work done by a gas.",
     "pages/PV_Graphs_Thermodynamics.py"),
    ("⚡", "Electric Field",
     "Place charges and visualize the resulting 3D electric field.",
     "pages/Electric_Field.py"),
    ("🧲", "Magnetic Field Motion",
     "Visualize how charged particles move under magnetic forces in real time.",
     "pages/Lorentz_Force.py"),
    ("🌀", "Oscillators",
     "Explore damped, underdamped and overdamped harmonic motion.",
     "pages/Oscillators.py"),
    ("🔥", "Carnot Engine",
     "Visualize heat, work, and engine efficiency.",
     "pages/Carnot_Engine.py"),
    ("⏳", "Time Dilation",
     "See how motion slows the passage of time.",
     "pages/Relativity_Time_Dilation.py"),
    ("🚀", "Twin Paradox",
     "Travel fast, return younger than Earth.",
     "pages/Relativity_Twin_Paradox.py"),
    ("∿", "Fourier Series",
    "Build complex waves from simple sine functions.",
    "pages/Fourier_Series.py"),
]

col1, col2, col3 = st.columns(3, gap="medium")
col4, col5, col6 = st.columns(3, gap="medium")
col7, col8, col9 = st.columns(3, gap="medium")
col10, col11, col12 = st.columns(3, gap="medium")

for col, (icon, title, desc, page) in zip([col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12], cards):
    with col:
        st.markdown(sim_card(icon, title, desc), unsafe_allow_html=True)
        if st.button("Explore →", key=f"nav_{title}", help=f"Go to {title}"):
            st.switch_page(page)

st.markdown("<div style='padding: 52px 0 0;'></div>", unsafe_allow_html=True)


# ---- FEATURES SECTION ----
st.markdown("""
<p class='section-label'>Features</p>
<h2 class='section-heading'>What you can do</h2>
""", unsafe_allow_html=True)

colA, colB = st.columns(2, gap="large")

features_left = [
    "Adjust parameters interactively with live sliders",
    "Compare two physical systems side by side",
    "Visualize complex concepts in 2D and 3D",
]
features_right = [
    "Generate publication-quality graphs instantly",
    "Download full PDF simulation reports",
    "Build physical intuition without memorizing formulas",
]

def render_features(items):
    html = ""
    for item in items:
        html += f"<div class='feature-item'><div class='feature-dot'></div><span>{item}</span></div>"
    return html

with colA:
    st.markdown(render_features(features_left), unsafe_allow_html=True)
with colB:
    st.markdown(render_features(features_right), unsafe_allow_html=True)


# ---- FOOTER ----
st.markdown("<div style='padding: 48px 0 0;'></div>", unsafe_allow_html=True)

# ---- HOVER FIX ----
st.markdown("""
<style>
.contact-btn {
    display:flex;
    align-items:center;
    gap:8px;
    padding:10px 16px;
    background:#1f3b57;
    border-radius:8px;
    color:white !important;         
    font-weight:500;
    text-decoration:none !important;
    transition: all 0.25s ease;
}

a.contact-btn,
a.contact-btn:visited,
a.contact-btn:hover,
a.contact-btn:active {
    color: white !important;
    text-decoration: none !important;
}

.contact-btn:hover {
    background:#2a5275;
    transform: translateY(-2px);
}
.contact-container {
    display:flex;
    justify-content:center;
    gap:20px;
}
</style>
""", unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("<div class='footer'>Built to make physics intuitive and interactive.</div>", unsafe_allow_html=True)

st.markdown("---")

# ---- ABOUT ----
st.markdown("""
<div style="
    background: rgba(10,22,36,0.6);
    padding: 18px;
    border-radius: 12px;
    color: #cfe8ff;
">

<h3 style="color:#7ec8e3;">About the Author</h3>

<p>
Hi, I'm <b>Soumya</b><br><br>

I'm a physics student who enjoys turning complex ideas into interactive simulations.<br>
This project is built to make physics something you can <b>see and feel</b>, not just memorize.<br><br>

I also enjoy building apps — feel free to check out my GitHub.<br>
Hope you found this useful, and feel free to reach out.<br>
Peace and will be back with more updates.
</p>

</div>
""", unsafe_allow_html=True)

# ---- CONTACT ----
st.markdown("""
<div style="
    background: rgba(10,22,36,0.6);
    padding: 18px;
    border-radius: 12px;
    color: #cfe8ff;
    margin-top: 15px;
">

<h4 style="color:#7ec8e3;">Connect</h4>

<p>
Got an idea? Found a bug? Want to collaborate?
</p>

<div class="contact-container">

<!-- EMAIL -->
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=soumya.ckd2005@gmail.com" target="_blank" class="contact-btn">
    <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
        <path d="M2 4h20v16H2V4zm10 7L4 6v12h16V6l-8 5z"/>
    </svg>
    Email
</a>

<!-- LINKEDIN -->
<a href="https://www.linkedin.com/in/soumya-sengupta-a8346633a" target="_blank" class="contact-btn">
    <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
        <path d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1 4.98 2.12 4.98 3.5zM0 8h5v16H0V8zm7.5 0h4.8v2.2h.1c.7-1.3 2.3-2.7 4.7-2.7 5 0 5.9 3.3 5.9 7.6V24h-5v-7.9c0-1.9 0-4.3-2.6-4.3s-3 2-3 4.2V24h-5V8z"/>
    </svg>
    LinkedIn
</a>

<!-- GITHUB -->
<a href="https://github.com/soumyasengupta2005-rgb" target="_blank" class="contact-btn">
    <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.43 9.8 8.2 11.38.6.1.82-.26.82-.58 0-.28-.01-1.02-.02-2-3.34.73-4.04-1.6-4.04-1.6-.55-1.4-1.35-1.78-1.35-1.78-1.1-.75.08-.73.08-.73 1.22.09 1.86 1.25 1.86 1.25 1.08 1.85 2.83 1.32 3.52 1 .1-.79.42-1.32.76-1.62-2.66-.3-5.47-1.34-5.47-5.96 0-1.32.47-2.4 1.25-3.25-.13-.3-.54-1.5.12-3.13 0 0 1-.32 3.3 1.24a11.5 11.5 0 0 1 6 0C17.8 6.8 18.8 7.12 18.8 7.12c.66 1.63.25 2.83.12 3.13.78.85 1.25 1.93 1.25 3.25 0 4.63-2.81 5.66-5.49 5.96.43.37.82 1.1.82 2.22 0 1.6-.01 2.9-.01 3.3 0 .32.22.7.82.58A12.01 12.01 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
    </svg>
    GitHub
</a>

</div>

</div>
""", unsafe_allow_html=True)