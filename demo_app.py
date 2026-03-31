import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WaveFlow System – ControlFlow Demo",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# BRAND COLORS
# ─────────────────────────────────────────────
ORANGE_START = "#fbb040"
ORANGE_END   = "#f15a29"
BLUE_START   = "#00bdf2"
BLUE_END     = "#0075a1"
DARK_BG      = "#0a1628"
CARD_BG      = "#0f2040"
TEXT_LIGHT   = "#e8f4fd"
TEXT_MUTED   = "#7fb3d3"

# ─────────────────────────────────────────────
# CSS STYLING
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* Global */
html, body, [class*="css"] {{
    font-family: 'Exo 2', sans-serif;
    background-color: {DARK_BG};
    color: {TEXT_LIGHT};
}}

.stApp {{
    background: linear-gradient(135deg, {DARK_BG} 0%, #0d1f3c 50%, #0a1628 100%);
    padding: 0 2rem !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1f3c 0%, {DARK_BG} 100%);
    border-right: 1px solid rgba(0,189,242,0.2);
}}

[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {{
    color: {TEXT_LIGHT} !important;
    font-family: 'Exo 2', sans-serif !important;
}}

/* Headers */
h1, h2, h3 {{
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
}}

/* Etykiety suwaków */
.stSlider label, 
.stSlider label p {{
    font-size: 1.05rem !important;
}}

.stSlider p {{
    font-size: 1.05rem !important;
}}


/* Etykiety i tekst selectbox */
.stSelectbox label,
.stSelectbox label p,
.stSelectbox div[data-baseweb="select"] span {{
    font-size: 1.05rem !important;
}}

/* Etykiety i tekst number input */
.stNumberInput label,
.stNumberInput label p,
.stNumberInput input {{
    font-size: 1.1rem !important;
}}

button [data-testid="stMarkdownContainer"] p {{
    font-size: 1.1rem !important;
}}

/* Metric cards */
.metric-card {{
    background: linear-gradient(135deg, {CARD_BG} 0%, #162848 100%);
    border: 1px solid rgba(0,189,242,0.25);
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}}

.metric-value {{
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, {ORANGE_START}, {ORANGE_END});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Exo 2', sans-serif;
}}

.metric-value-blue {{
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, {BLUE_START}, {BLUE_END});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Exo 2', sans-serif;
}}

.metric-label {{
    font-size: 1rem;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}}

/* Section header */
.section-header {{
    background: linear-gradient(90deg, rgba(0,189,242,0.15) 0%, transparent 100%);
    border-left: 3px solid {BLUE_START};
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 20px;
}}

.section-header h2 {{
    margin: 0 !important;
    font-size: 1.3rem !important;
    color: {TEXT_LIGHT} !important;
}}

/* Insight box */
.insight-box {{
    background: linear-gradient(135deg, rgba(251,176,64,0.1) 0%, rgba(241,90,41,0.1) 100%);
    border: 1px solid rgba(251,176,64,0.3);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 1.1rem;
}}

.insight-box-blue {{
    background: linear-gradient(135deg, rgba(0,189,242,0.1) 0%, rgba(0,117,161,0.1) 100%);
    border: 1px solid rgba(0,189,242,0.3);
    border-radius: 10px;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 1.1rem;
}}

/* Pump indicator */
.pump-on {{
    display: inline-block;
    background: linear-gradient(135deg, {ORANGE_START}, {ORANGE_END});
    color: white;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 700;
    font-size: 1.1rem;
    margin: 4px;
    font-family: 'JetBrains Mono', monospace;
}}

.pump-off {{
    display: inline-block;
    background: rgba(255,255,255,0.08);
    color: {TEXT_MUTED};
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 700;
    font-size: 1.1rem;
    margin: 4px;
    border: 1px solid rgba(255,255,255,0.1);
    font-family: 'JetBrains Mono', monospace;
}}

/* StSelectbox */
.stSelectbox > div > div {{
    background-color: {CARD_BG} !important;
    border-color: rgba(0,189,242,0.3) !important;
    color: {TEXT_LIGHT} !important;
    font-size: 1.1rem !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background-color: {CARD_BG};
    border-radius: 10px;
    padding: 4px;
}}

.stTabs [data-baseweb="tab"] {{
    color: {TEXT_MUTED} !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding-left: 32px !important;
    padding-right: 32px !important;
    min-width: 220px !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ORANGE_START}, {ORANGE_END}) !important;
    color: white !important;
    border-radius: 8px !important;
    font-size: 1.5rem !important;
}}

/* Sliders */
.stSlider [data-testid="stTickBar"] {{
    color: {TEXT_MUTED};
}}

/* Divider */
.wave-divider {{
    height: 2px;
    background: linear-gradient(90deg, transparent, {BLUE_START}, {ORANGE_START}, {ORANGE_END}, transparent);
    margin: 24px 0;
    border-radius: 2px;
}}

/* Hero */
.hero-title {{
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, {BLUE_START} 0%, {ORANGE_START} 50%, {ORANGE_END} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 8px;
}}

.hero-sub {{
    font-size: 1.2rem;
    color: {TEXT_MUTED};
    font-weight: 300;
    letter-spacing: 0.05em;
}}

/* Table styling */
.comparison-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Exo 2', sans-serif;
}}
.comparison-table th {{
    background: linear-gradient(90deg, {BLUE_END}, {BLUE_START});
    color: white;
    padding: 10px 16px;
    text-align: center;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
.comparison-table td {{
    padding: 10px 16px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: {TEXT_LIGHT};
    font-size: 1.1rem;
}}
.comparison-table tr:nth-child(even) td {{
    background: rgba(255,255,255,0.03);
}}
.highlight-orange {{
    background: linear-gradient(90deg, {ORANGE_START}, {ORANGE_END});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
T = {
    "PL": {
        "nav_home": "🏠 Strona główna",
        "nav_data": "⚙️ Dane instalacji",
        "nav_analysis": "📊 Analiza obecna",
        "btn_analysis": "Analiza obecna",
        "nav_single": "🔵 Jedna pompa",
        "nav_cascade": "🔷 Kaskada pomp",
        "nav_roi": "💰 ROI",
        "hero_title": "ControlFlow",
        "hero_sub": "Inteligentne sterowanie maszynami przepływowymi",
        "hero_desc": "Optymalizacja energii w czasie rzeczywistym – pompy, sprężarki, wentylatory.",
        "start_btn": "▶ Rozpocznij demo",
        "industry": "Branża",
        "pump_power": "Moc pompy [kW]",
        "num_pumps": "Liczba pomp",
        "hours": "Godziny pracy [h/dzień]",
        "energy_price": "Cena energii [PLN/kWh]",
        "control_mode": "Obecny tryb sterowania",
        "setpoint_mode": "Tryb setpointu",
        "setpoint_Q": "Stały przepływ Q",
        "setpoint_H": "Stałe ciśnienie H",
        "industries": ["Wodociągi", "Przemysł", "HVAC", "Ścieki", "Spożywczy"],
        "control_modes": ["On/Off", "Stałe obroty", "Falownik + PID"],
        "current_efficiency": "Sprawność aktualna",
        "max_efficiency": "Możliwe maximum",
        "loss": "Straty energetyczne",
        "current_op": "Twój punkt pracy",
        "bep": "BEP (optimum)",
        "flow": "Przepływ Q [m³/h]",
        "head": "Ciśnienie H [bar]",
        "power": "Moc [kW]",
        "efficiency_curve": "Krzywa sprawności η(Q)",
        "qh_curve": "Krzywa Q-H",
        "daily_profile": "Profil dobowy",
        "without_ml": "Klasyczne<br>sterowanie",
        "with_ml": "Sterowanie<br>z ControlFlow",
        "savings_day": "Oszczędność dziś",
        "savings_month": "Oszczędność / miesiąc",
        "savings_year": "Oszczędność / rok",
        "payback": "Czas zwrotu",
        "investment": "Koszt wdrożenia",
        "active_pumps": "Aktywne pompy",
        "ml_decision": "Decyzja ML",
        "q_total": "Przepływ całkowity Q [m³/h]",
        "h_setpoint": "Setpoint ciśnienia H [bar]",
        "animate": "▶ Animuj dobę",
        "stop": "⏹ Stop",
        "pumps_label": "Pompa",
        "roi_title": "Zwrot z inwestycji",
        "cumulative": "Skumulowane koszty [PLN]",
        "years": "Lata",
        "month": "mies.",
        "year": "rok",
        "efficiency": "Sprawność η",
        "avg_power": "Moc średnia",
        "monthly_cost": "Koszt miesięczny",
        "yearly_cost": "Koszt roczny",
        "single_pump_tab1": "Stały przepływ Q",
        "single_pump_tab2": "Stałe ciśnienie H",
        "explanation_Q": "ML optymalizuje punkt pracy przy zadanym Q – pompa zawsze pracuje blisko BEP",
        "explanation_H": "ML optymalizuje setpoint ciśnienia – PID realizuje cel, ML minimalizuje koszty",
        "ml_checked": "ML sprawdził kombinacje:",
        "selected": "← wybrano",
        "all_day": "Pełna doba (24h)",
        "language": "🌐 Język / Language",
    },
    "EN": {
        "nav_home": "🏠 Home",
        "nav_data": "⚙️ Installation Data",
        "nav_analysis": "📊 Current Analysis",
        "btn_analysis": "Current Analysis",
        "nav_single": "🔵 Single Pump",
        "nav_cascade": "🔷 Pump Cascade",
        "nav_roi": "💰 ROI",
        "hero_title": "ControlFlow",
        "hero_sub": "Intelligent control of fluid machinery",
        "hero_desc": "Real-time energy optimization – pumps, compressors, fans.",
        "start_btn": "▶ Start demo",
        "industry": "Industry",
        "pump_power": "Pump power [kW]",
        "num_pumps": "Number of pumps",
        "hours": "Operating hours [h/day]",
        "energy_price": "Energy price [PLN/kWh]",
        "control_mode": "Current control mode",
        "setpoint_mode": "Setpoint mode",
        "setpoint_Q": "Constant flow Q",
        "setpoint_H": "Constant pressure H",
        "industries": ["Water supply", "Industry", "HVAC", "Wastewater", "Food processing"],
        "control_modes": ["On/Off", "Fixed speed", "Inverter + PID"],
        "current_efficiency": "Current efficiency",
        "max_efficiency": "Possible maximum",
        "loss": "Energy loss",
        "current_op": "Your operating point",
        "bep": "BEP (optimum)",
        "flow": "Flow Q [m³/h]",
        "head": "Pressure H [bar]",
        "power": "Power [kW]",
        "efficiency_curve": "Efficiency curve η(Q)",
        "qh_curve": "Q-H Curve",
        "daily_profile": "Daily profile",
        "without_ml": "Classic system control",
        "with_ml": "Pomps control with ControlFlow",
        "savings_day": "Savings today",
        "savings_month": "Savings / month",
        "savings_year": "Savings / year",
        "payback": "Payback period",
        "investment": "Implementation cost",
        "active_pumps": "Active pumps",
        "ml_decision": "ML Decision",
        "q_total": "Total flow Q [m³/h]",
        "h_setpoint": "Pressure setpoint H [bar]",
        "animate": "▶ Animate day",
        "stop": "⏹ Stop",
        "pumps_label": "Pump",
        "roi_title": "Return on Investment",
        "cumulative": "Cumulative costs [PLN]",
        "years": "Years",
        "month": "mo.",
        "year": "yr",
        "efficiency": "Efficiency η",
        "avg_power": "Average power",
        "monthly_cost": "Monthly cost",
        "yearly_cost": "Yearly cost",
        "single_pump_tab1": "Constant flow Q",
        "single_pump_tab2": "Constant pressure H",
        "explanation_Q": "ML optimizes the operating point at given Q – pump always works near BEP",
        "explanation_H": "ML optimizes the pressure setpoint – PID executes the target, ML minimizes costs",
        "ml_checked": "ML checked combinations:",
        "selected": "← selected",
        "all_day": "Full day (24h)",
        "language": "🌐 Język / Language",
    }
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "PL"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "hours_value" not in st.session_state:
    st.session_state["hours_value"] = 24
if "hours_slider" not in st.session_state:
    st.session_state["hours_slider"] = 24
if "q_nom" not in st.session_state:
    st.session_state["q_nom"] = 80.0
# if "h_nom_bar" not in st.session_state:
#     st.session_state["h_nom_bar"] = 4.0

def t(key):
    return T[st.session_state.lang][key]

# ─────────────────────────────────────────────
# PHYSICS ENGINE
# ─────────────────────────────────────────────
def efficiency_curve(Q, Q_bep=50, eta_max=0.78):
    """Parabolic efficiency curve centered at BEP, scaled with Q_bep"""
    coeff = (eta_max - 0.25) / (Q_bep ** 2)
    eta = eta_max - coeff * (Q - Q_bep)**2
    return np.clip(eta, 0.01, eta_max)  # min 1% - brak sztucznego cięcia

def qh_curve(Q, n_ratio=1.0, H_nom=40, Q_max=80):
    """Q-H curve scaled by speed ratio, H=0 exactly at Q_max"""
    H = (H_nom * n_ratio**2) * (1 - (Q / (Q_max * n_ratio))**2)
       
    return np.maximum(H, 0)

def power_kw(Q, H, eta, rho=1000):
    """Hydraulic power in kW, H in meters"""
    return (rho * 9.81 * (Q / 3600) * H) / (eta * 1000)

def m_to_bar(H_m):
    """Convert meters of water to bar"""
    return H_m * 1000 * 9.81 / 100000

def bar_to_m(H_bar):
    """Convert bar to meters of water"""
    return H_bar * 100000 / (1000 * 9.81)

def find_optimal_n(Q_demand, H_setpoint=None, Q_bep=50, eta_max=0.78):
    """Find optimal speed ratio for ML"""
    best_n, best_eta = 0.4, 0.3
    for n in np.arange(0.4, 1.01, 0.05):
        Q_at_n = Q_demand
        eta = efficiency_curve(Q_at_n / n, Q_bep, eta_max) * (0.85 + 0.15 * n)
        if eta > best_eta:
            best_eta = eta
            best_n = n
    return best_n, best_eta

def baseline_efficiency(Q, control_mode, Q_bep=50, eta_max=0.78):
    """Efficiency for baseline control"""
    if control_mode == 0:  # On/Off
        return efficiency_curve(Q, Q_bep, eta_max) * 0.75
    elif control_mode == 1:  # Fixed speed
        return efficiency_curve(Q, Q_bep, eta_max) * 0.82
    else:  # PID without ML
        return efficiency_curve(Q, Q_bep, eta_max) * 0.91

# ─────────────────────────────────────────────
# DAILY PROFILES
# ─────────────────────────────────────────────
# Profile dobowe [% Q_max] dla każdej branży, 24 wartości (każda = 1h)
# Wartości 0 = pompa nie pracuje
PROFILES = {
    "PL": {
        # Wodociągi: ciągła praca, dwa szczyty (7-9 rano, 17-21 wieczór), minimum w nocy
        "Wodociągi":  [22,19,16,14,15,22,55,82,91,88,84,86,90,87,83,80,84,92,95,88,72,55,40,28],
        # Przemysł: dwie zmiany (6:00-22:00), przerwy obiadowe widoczne, noc = 0
        "Przemysł":   [0,0,0,0,0,0,65,88,95,92,90,75,70,78,92,95,90,85,60,0,0,0,0,0],
        # HVAC biurowiec: praca 6:00-22:00, szczyt w południe, noc minimum
        "HVAC":       [15,12,10,10,12,20,45,68,82,88,92,95,95,93,90,88,85,78,65,52,40,32,22,18],
        # Ścieki komunalne: dwa wyraźne szczyty (7-9, 18-21), minimum w nocy
        "Ścieki":     [28,22,18,15,16,25,62,82,80,72,68,65,68,66,65,68,72,85,88,78,62,50,40,32],
        # Spożywczy: jedna zmiana (6:00-18:00), przed i po = 0
        "Spożywczy":  [0,0,0,0,0,0,55,82,90,95,95,92,88,90,92,90,80,0,0,0,0,0,0,0],
    },
    "EN": {
        "Water supply":     [22,19,16,14,15,22,55,82,91,88,84,86,90,87,83,80,84,92,95,88,72,55,40,28],
        "Industry":         [0,0,0,0,0,0,65,88,95,92,90,75,70,78,92,95,90,85,60,0,0,0,0,0],
        "HVAC":             [15,12,10,10,12,20,45,68,82,88,92,95,95,93,90,88,85,78,65,52,40,32,22,18],
        "Wastewater":       [28,22,18,15,16,25,62,82,80,72,68,65,68,66,65,68,72,85,88,78,62,50,40,32],
        "Food processing":  [0,0,0,0,0,0,55,82,90,95,95,92,88,90,92,90,80,0,0,0,0,0,0,0],
    }
}

# Krzywe Q-H per branża – realistyczne parametry
# Q_default, H_default = nominalne wartości jednej pompy przy BEP
# Q_max_range, H_max_range = maksymalne zakresy suwaków
BRANCH_CURVES = {
    "Wodociągi":       {"eta_max": 0.82, "Q_default": 80,  "H_default": 4.0, "Q_max_range": 200, "H_max_range": 8.0},
    "Przemysł":        {"eta_max": 0.78, "Q_default": 40,  "H_default": 6.0, "Q_max_range": 200, "H_max_range": 12.0},
    "HVAC":            {"eta_max": 0.72, "Q_default": 40,  "H_default": 2.0, "Q_max_range": 150, "H_max_range": 5.0},
    "Ścieki":          {"eta_max": 0.70, "Q_default": 60,  "H_default": 3.0, "Q_max_range": 200, "H_max_range": 6.0},
    "Spożywczy":       {"eta_max": 0.75, "Q_default": 30,  "H_default": 5.0, "Q_max_range": 100, "H_max_range": 10.0},
    "Water supply":    {"eta_max": 0.82, "Q_default": 80,  "H_default": 4.0, "Q_max_range": 200, "H_max_range": 8.0},
    "Industry":        {"eta_max": 0.78, "Q_default": 40,  "H_default": 6.0, "Q_max_range": 200, "H_max_range": 12.0},
    "Wastewater":      {"eta_max": 0.70, "Q_default": 60,  "H_default": 3.0, "Q_max_range": 200, "H_max_range": 6.0},
    "Food processing": {"eta_max": 0.75, "Q_default": 30,  "H_default": 5.0, "Q_max_range": 100, "H_max_range": 10.0},
}

_TARIFF_RAW = [0.45,0.45,0.45,0.45,0.45,0.45,0.95,0.95,0.95,0.95,0.95,0.95,
               0.70,0.70,0.70,0.70,0.95,0.95,0.95,0.95,0.95,0.70,0.45,0.45]
TARIFF = [x / np.mean(_TARIFF_RAW) for x in _TARIFF_RAW]

# ─────────────────────────────────────────────
# LOGO HELPER
# ─────────────────────────────────────────────
def get_logo_b64():
    #logo_path = Path("C:/Users/Jakub/Desktop/PompML/logo.png")
    logo_path = Path("logo.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    logo_b64 = get_logo_b64()
    if logo_b64:
        st.markdown(f"""
        <div style="text-align:center; padding: 16px 0 8px 0;">
            <img src="data:image/png;base64,{logo_b64}" style="width:85%; filter: brightness(1.1);">
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    lang = st.radio(t("language"), ["PL", "EN"],
                    index=0 if st.session_state.lang == "PL" else 1,
                    horizontal=True)
    st.session_state.lang = lang

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    pages = [
        ("home",     t("nav_home")),
        ("data",     t("nav_data")),
        ("analysis", t("nav_analysis")),
        ("single",   t("nav_single")),
        ("cascade",  t("nav_cascade")),
        ("roi",      t("nav_roi")),
    ]
    for key, label in pages:
        active = st.session_state.page == key
        if st.button(label, key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; color:{TEXT_MUTED}; font-size:0.75rem;">
        ControlFlow Demo v1.0<br>WaveFlow System Solutions 4.X<br>eBigData
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPER: GET SESSION PARAMS
# ─────────────────────────────────────────────
def get_params():
    num_pumps    = st.session_state.get("num_pumps", 4)
    hours        = st.session_state.get("hours", 16)
    energy_price = st.session_state.get("energy_price", 0.80)
    control_mode = st.session_state.get("control_mode", 2)
    lang_key     = st.session_state.lang
    industry     = st.session_state.get("industry", t("industries")[0])
    profile_map  = PROFILES[lang_key]
    profile_raw  = profile_map.get(industry, list(profile_map.values())[0])
    curve        = BRANCH_CURVES.get(industry, {"eta_max": 0.78, "Q_default": 50, "H_default": 4.0, "Q_max_range": 300, "H_max_range": 10.0})
    eta_max      = curve.get("eta_max", 0.78)
    # Q_max i H_nom z suwaków klienta
    q_nom        = st.session_state.get("q_nom", curve["Q_default"])
    h_nom_bar    = st.session_state.get("h_nom_bar", curve["H_default"])
    # Q_nom = przepływ nominalny jednej pompy (podany przez klienta)
    # Q_bep = Q_nom (klient pracuje w okolicach punktu optymalnego)
    # Q_max = Q_nom * 1.3 (granica krzywej Q-H, trochę powyżej Q_nom)
    Q_bep        = float(q_nom)
    Q_max        = float(q_nom) * 1.3
    H_nom        = float(h_nom_bar) * 10.197   # bar → metry
    # Profil dobowy skaluje się z Q_nom × num_pumps – cała instalacja
    Q_total_max  = Q_bep * num_pumps
    Q_profile    = np.array([q * Q_total_max / 100 for q in profile_raw])
    # Moc nominalna z fizyki
    pump_power   = round((1000 * 9.81 * (Q_max/3600) * H_nom) / (eta_max * 1000), 1)
    return pump_power, num_pumps, hours, energy_price, control_mode, Q_profile, Q_max, Q_bep, eta_max, H_nom

# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
if st.session_state.page == "home":
    col_logo, col_text = st.columns([1, 2])
    with col_logo:
        if logo_b64:
            st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; height:200px;">
                <img src="data:image/png;base64,{logo_b64}" style="width:90%; filter: drop-shadow(0 0 20px rgba(0,189,242,0.4));">
            </div>
            """, unsafe_allow_html=True)
    with col_text:
        st.markdown(f"""
        <div style="padding: 20px 0;">
            <div class="hero-title">{t('hero_title')}</div>
            <div style="font-size:1.4rem; color:{TEXT_MUTED}; font-weight:300; margin-bottom:12px;">
                {t('hero_sub')}
            </div>
            <div style="font-size:1.05rem; color:{TEXT_LIGHT}; line-height:1.7;">
                {t('hero_desc')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("5–35%", "Oszczędność energii" if lang=="PL" else "Energy savings", ORANGE_START),
        ("1–2h", "Czas kalibracji" if lang=="PL" else "Calibration time", BLUE_START),
        ("ML + PID", "Architektura" if lang=="PL" else "Architecture", ORANGE_END),
        ("Każda branża" if lang=="PL" else "Every industry", "Skalowalność" if lang=="PL" else "Scalability", BLUE_END),
    ]
    for col, (val, lbl, clr) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.8rem; font-weight:800; color:{clr};">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px; margin-top:8px;">
        <div class="insight-box-blue">
            <b style="color:{BLUE_START};">🔵 Regulator PID</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"Utrzymuje zadane ciśnienie lub przepływ." if lang=="PL" else "Maintains the required pressure or flow."}
            </span>
        </div>
        <div class="insight-box">
            <b style="color:{ORANGE_START};">🟠 Model ML</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"Optymalizuje punkt pracy maszyny. Minimalizuje zużycie energii." if lang=="PL" else "Optimizes the machine operating point. Minimizes energy consumption."}
            </span>
        </div>
        <div class="insight-box-blue">
            <b style="color:{BLUE_START};">⚡ Razem</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"PID realizuje cel. ML sprawia że ten cel kosztuje jak najmniej." if lang=="PL" else "PID executes the target. ML makes sure that target costs as little as possible."}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t("start_btn"), use_container_width=True, type="primary"):
        st.session_state.page = "data"
        st.rerun()

# ─────────────────────────────────────────────
# PAGE: DATA INPUT
# ─────────────────────────────────────────────
elif st.session_state.page == "data":
    st.markdown(f'<div class="section-header"><h2> {t("nav_data")}</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        industry_list = t("industries")
        # Zachowaj wybraną branżę między zakładkami
        _saved_industry = st.session_state.get("industry", industry_list[0])
        _saved_idx = industry_list.index(_saved_industry) if _saved_industry in industry_list else 0
        industry = st.selectbox(t("industry"), industry_list, index=_saved_idx, key="industry_select")
        # Gdy zmienia się branża – przelicz godziny i wymuś rerun
        _profile_map = PROFILES[st.session_state.lang]
        _profile_raw = _profile_map.get(industry, list(_profile_map.values())[0])
        hours_from_profile = max(sum(1 for q in _profile_raw if q > 0), 1)
        if st.session_state.get("industry") != industry:
            st.session_state["hours_value"] = hours_from_profile
            st.session_state["hours_slider"] = hours_from_profile
            _cp = BRANCH_CURVES.get(industry, {"Q_default": 50, "H_default": 4.0})
            st.session_state["q_nom_slider"] = float(_cp["Q_default"])
            st.session_state["h_nom_slider"] = float(_cp["H_default"])
            st.session_state["q_nom"] = float(_cp["Q_default"])
            st.session_state["h_nom_bar"] = float(_cp["H_default"])
            # Reset dependent sliders
            for key in ["q_single", "q_total_slider", "h_single", "h_cascade"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.industry = industry
            st.rerun()
        st.session_state.industry = industry

        _curve_p = BRANCH_CURVES.get(industry, {"Q_default": 50, "H_default": 4.0, "Q_max_range": 300, "H_max_range": 10.0})
        # Reset Q_nom and H_nom when industry changes
        if st.session_state.get("industry") != industry:
            st.session_state["q_nom_slider"] = float(_curve_p["Q_default"])
            st.session_state["h_nom_slider"] = float(_curve_p["H_default"])
        _q_default = float(st.session_state.get("q_nom_slider", _curve_p["Q_default"]))
        _h_default = float(st.session_state.get("h_nom_slider", _curve_p["H_default"]))
         # Q_nom max = max Q z profilu dobowego
        _profile_map_q = PROFILES[st.session_state.lang]
        _profile_raw_q = _profile_map_q.get(industry, list(_profile_map_q.values())[0])
        _q_profile_max = float(max(_profile_raw_q)) * float(_curve_p["Q_max_range"]) / 100
        _q_slider_max = min(float(_curve_p["Q_max_range"]), _q_profile_max)
        _q_default = min(float(st.session_state.get("q_nom", _curve_p["Q_default"])), _q_slider_max)
        q_nom = st.slider("Q nom – przepływ jednej pompy [m³/h]" if lang=="PL" else "Q nom – flow per pump [m³/h]",
                          5.0, _q_slider_max, _q_default, 5.0, key="q_nom_slider")
        st.session_state["q_nom"] = float(q_nom)
        _h_default_cur = float(st.session_state.get("h_nom_bar", _curve_p["H_default"]))
        _h_default_cur = min(_h_default_cur, float(_curve_p["H_max_range"]))
        h_nom_bar = st.slider("H nom – ciśnienie nominalne [bar]" if lang=="PL" else "H nom – nominal pressure [bar]",
                              0.5, float(_curve_p["H_max_range"]), _h_default_cur, 0.5, key="h_nom_slider")
        st.session_state["h_nom_bar"] = float(h_nom_bar)

        _prev_num_pumps = st.session_state.get("num_pumps", 4)
        num_pumps = st.slider(t("num_pumps"), 1, 8, _prev_num_pumps, key="num_pumps_slider")
        st.session_state.num_pumps = num_pumps
        # Reset cascade slider when num_pumps changes
        if _prev_num_pumps != num_pumps:
            if "q_total_slider" in st.session_state:
                del st.session_state["q_total_slider"]

    with col2:
        # Godziny pracy – wartość z session_state (resetowana przy zmianie branży)
        hours_val = st.session_state.get("hours_value", hours_from_profile)
        hours = st.slider(t("hours"), 1, 24, int(hours_val), key="hours_slider")
        st.session_state.hours = hours
        st.session_state["hours_value"] = hours

        energy_price = st.number_input(t("energy_price"), 0.1, 5.0, 0.80, 0.05)
        st.session_state.energy_price = energy_price

        current_mode = st.session_state.get("control_mode", 2)
        control_idx = st.selectbox(
            t("control_mode"),
            t("control_modes"),
            index=current_mode,
            key="control_mode_select"
        )
        st.session_state.control_mode = t("control_modes").index(control_idx)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    # Show loaded profile preview
    lang_key = st.session_state.lang
    profile_map = PROFILES[lang_key]
    profile_raw = profile_map.get(industry, list(profile_map.values())[0])
    _q_prev = st.session_state.get("q_nom", BRANCH_CURVES.get(industry, {"Q_default": 50})["Q_default"])
    _num_prev = st.session_state.get("num_pumps", 3)
    Q_max = float(_q_prev) * _num_prev  # profil = Q_nom × liczba pomp
    Q_profile = [q * Q_max / 100 for q in profile_raw]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(24)), y=Q_profile,
        fill='tozeroy',
        fillcolor=f'rgba(0,189,242,0.15)',
        line=dict(color=BLUE_START, width=2),
        name=t("daily_profile")
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_LIGHT, family='Exo 2'),
        xaxis=dict(title="Godzina [h]" if lang=="PL" else "Hour [h]",
                   gridcolor='rgba(255,255,255,0.06)', tickvals=list(range(0,24,3))),
        yaxis=dict(title=t("flow"), gridcolor='rgba(255,255,255,0.06)'),
        height=280,
        margin=dict(t=20, b=40, l=60, r=20),
        showlegend=False
    )
    
    fig.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    fig.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    fig.update_layout(
    title=dict(text="Profil dobowy przepływu" if lang=="PL" else "Daily flow profile",
               font=dict(color=TEXT_LIGHT, size=16)))
    
    st.plotly_chart(fig, use_container_width=True)
    
    tariff_prices = [t_val * energy_price for t_val in TARIFF]

    fig_tariff = go.Figure()
    fig_tariff.add_trace(go.Scatter(
        x=list(range(24)),
        y=tariff_prices,
        fill='tozeroy',
        fillcolor='rgba(251,176,64,0.15)',
        line=dict(color=ORANGE_START, width=2),
        name="Taryfa" if lang == "PL" else "Tariff"
    ))
    fig_tariff.add_hline(
        y=energy_price,
        line_dash="dash",
        line_color=TEXT_MUTED,
        line_width=1,
        annotation_text=f"{'Średnia' if lang=='PL' else 'Average'}: {energy_price:.2f} PLN/kWh",
        annotation_font_color=TEXT_MUTED
    )
    fig_tariff.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_LIGHT, family='Exo 2',size=14),
        xaxis=dict(title="Godzina [h]" if lang == "PL" else "Hour [h]",
                   gridcolor='rgba(255,255,255,0.06)', tickvals=list(range(0, 24, 3))),
        yaxis=dict(title="PLN/kWh", gridcolor='rgba(255,255,255,0.06)'),
        height=220,
        margin=dict(t=20, b=40, l=60, r=20),
        showlegend=False,
    )
    
    fig_tariff.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    fig_tariff.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    
    fig_tariff.update_layout(
    title=dict(text="Rozkład cen energii w ciągu doby" if lang=="PL" else "Energy price distribution over the day",
               font=dict(color=TEXT_LIGHT, size=16)))
    
    st.plotly_chart(fig_tariff, use_container_width=True)  
    
    if st.button("▶ " + t("btn_analysis"), use_container_width=True, type="primary"):
        st.session_state.page = "analysis"
        st.rerun()

# ─────────────────────────────────────────────
# PAGE: CURRENT ANALYSIS
# ─────────────────────────────────────────────
elif st.session_state.page == "analysis":
    pump_power, num_pumps, hours, energy_price, control_mode, Q_profile, Q_max, Q_bep, eta_max, H_nom = get_params()

    st.markdown(f'<div class="section-header"><h2> {t("nav_analysis")}</h2></div>', unsafe_allow_html=True)

    Q_vals = np.linspace(Q_max * 0.1, Q_max, 200)
    eta_vals = efficiency_curve(Q_vals, Q_bep, eta_max)

    # avg_Q per pompa – profil całkowity / num_pumps
    Q_working = [q for q in Q_profile if q > Q_max * 0.02]
    avg_Q = np.mean(Q_working) / num_pumps if Q_working else Q_max * 0.5
    avg_Q = min(avg_Q, Q_max)
    st.session_state["avg_Q_one"] = avg_Q
    
    eta_current = baseline_efficiency(avg_Q, control_mode, Q_bep, eta_max)
    eta_ml = efficiency_curve(avg_Q, Q_bep, eta_max) * 0.97

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value-blue">{eta_current*100:.0f}%</div>
            <div class="metric-label">{t('current_efficiency')}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{eta_ml*100:.0f}%</div>
            <div class="metric-label">{t('max_efficiency')}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        loss_pct = round(eta_ml * 100) - round(eta_current * 100)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{loss_pct:.0f}%</div>
            <div class="metric-label">{t('loss')}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        fig_eta = go.Figure()
        fig_eta.add_trace(go.Scatter(
            x=Q_vals, y=eta_vals * 100,
            mode='lines', name='η(Q)',
            line=dict(color=BLUE_START, width=3),
            fill='tozeroy', fillcolor='rgba(0,189,242,0.08)'
        ))
        fig_eta.add_vline(x=Q_bep, line_dash="dash",
                          line_color=ORANGE_START, line_width=2)
        fig_eta.add_vline(x=avg_Q, line_dash="dot",
                          line_color="#ff4444", line_width=2)
        fig_eta.add_annotation(x=Q_bep, y=eta_max*100+2,
                                text=f"BEP ({eta_max*100:.0f}%)",
                                font=dict(color=ORANGE_START, size=14), showarrow=False)
        fig_eta.add_annotation(x=avg_Q, y=eta_current*100-5,
                                text=f"{t('current_op')}<br>η={eta_current*100:.0f}%",
                                font=dict(color="#ff6666", size=14), showarrow=False)
        fig_eta.update_layout(
            title=dict(text=t("efficiency_curve"), font=dict(color=TEXT_LIGHT, size=16)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_LIGHT, family='Exo 2'),
            xaxis=dict(title=t("flow"), gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(title="η [%]", gridcolor='rgba(255,255,255,0.06)'),
            height=300, margin=dict(t=40, b=40, l=60, r=20), showlegend=False
        )
        
        fig_eta.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        fig_eta.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        
        st.plotly_chart(fig_eta, use_container_width=True)        

    with col_right:
        H_vals = qh_curve(Q_vals, H_nom=H_nom, Q_max=Q_max)
        fig_qh = go.Figure()
        fig_qh.add_trace(go.Scatter(
            x=Q_vals, y=[m_to_bar(h) for h in H_vals],
            mode='lines', name='Q-H',
            line=dict(color=ORANGE_START, width=3)
        ))
        fig_qh.add_scatter(
            x=[avg_Q], y=[m_to_bar(qh_curve(np.array([avg_Q]), H_nom=H_nom, Q_max=Q_max)[0])],
            mode='markers',
            marker=dict(color="#ff4444", size=12, symbol='circle'),
            name=t("current_op")  # avg_Q per pompa
        )
        
        fig_qh.add_hline(
            y=m_to_bar(2.0),
            line_dash="dash",
            line_color="#ff4444",
            line_width=1,
            annotation_text=f"{m_to_bar(2.0):.2f} bar",
            annotation_font_color="#ff4444",
            annotation_position="left",
            annotation_font_size=14
            
        )        
        
        fig_qh.update_layout(
            title=dict(text=t("qh_curve"), font=dict(color=TEXT_LIGHT, size=16)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_LIGHT, family='Exo 2',size=16),
            xaxis=dict(title=t("flow"), gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(title="H [bar]", gridcolor='rgba(255,255,255,0.06)'),
            height=300, margin=dict(t=40, b=40, l=60, r=20), showlegend=False
        )
        
        fig_qh.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        fig_qh.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        
        st.plotly_chart(fig_qh, use_container_width=True)

    # Daily power analysis
    P_baseline = []
    P_ml_list = []
    
    for Q in Q_profile:
        if Q < Q_max * 0.02:
            P_baseline.append(0)
            P_ml_list.append(0)
            continue
        Qp = min(Q / num_pumps, Q_max)
        Qp = max(Qp, Q_max * 0.02)
        eta_b = baseline_efficiency(Qp, control_mode, Q_bep, eta_max)
        H_b = max(qh_curve(np.array([Qp]), H_nom=H_nom, Q_max=Q_max)[0], 2.0)
        P_b = power_kw(Qp, H_b, eta_b)
        P_baseline.append(P_b * num_pumps)
        _, eta_m = find_optimal_n(Qp, Q_bep=Q_bep, eta_max=eta_max)
        P_m = power_kw(Qp, H_b, eta_m)
        P_ml_list.append(P_m * num_pumps)

    fig_power = go.Figure()
    fig_power.add_trace(go.Scatter(
        x=list(range(24)), y=P_baseline,
        name=t("without_ml"),
        line=dict(color=BLUE_START, width=2, dash='dot'),
        fill='tozeroy', fillcolor='rgba(0,189,242,0.08)'
    ))
    fig_power.add_trace(go.Scatter(
        x=list(range(24)), y=P_ml_list,
        name=t("with_ml"),
        line=dict(color=ORANGE_START, width=3),
        fill='tozeroy', fillcolor='rgba(251,176,64,0.12)'
    ))
    fig_power.update_layout(
        title=dict(text="Dobowy profil mocy układu pomp [kW]" if lang=="PL" else "Daily power profile of pump system [kW]",
                   font=dict(color=TEXT_LIGHT, size=16)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_LIGHT, family='Exo 2'),
        xaxis=dict(title="Godzina [h]" if lang=="PL" else "Hour [h]",
                   gridcolor='rgba(255,255,255,0.06)', tickvals=list(range(0,24,3))),
        yaxis=dict(title=t("power"), gridcolor='rgba(255,255,255,0.06)'),
        height=300, margin=dict(t=40, b=40, l=60, r=80),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT))
    )
    
    fig_power.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    fig_power.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                            title_font=dict(size=14, color=TEXT_LIGHT))
    
    st.plotly_chart(fig_power, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE: SINGLE PUMP
# ─────────────────────────────────────────────
elif st.session_state.page == "single":
    pump_power, num_pumps, hours, energy_price, control_mode, Q_profile, Q_max, Q_bep, eta_max, H_nom = get_params()

    st.markdown(f'<div class="section-header"><h2> {t("nav_single")}</h2></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs([f"◆ {t('single_pump_tab1')}", f"◆ {t('single_pump_tab2')}"])

    # ── TAB 1: Constant Q ──
    with tab1:
        st.markdown(f'<div class="insight-box-blue">{t("explanation_Q")}</div>', unsafe_allow_html=True)

        _curve_q = BRANCH_CURVES.get(st.session_state.get("industry", t("industries")[0]),
                                      {"Q_max_range": 300})
        _q_single_max = float(_curve_q["Q_max_range"])
        _q_sel_default = float(st.session_state.get("q_nom", Q_max))
        _q_sel_default = min(_q_sel_default, _q_single_max)
        Q_sel = st.slider(t("flow"), float(Q_max*0.1), float(Q_max),
                  _q_sel_default, float(Q_max*0.05), key="q_single")
        #st.session_state["q_nom"] = float(Q_sel)

        H_sel = max(qh_curve(np.array([Q_sel]), H_nom=H_nom, Q_max=Q_max)[0], 2.0)

        eta_base = baseline_efficiency(Q_sel, control_mode, Q_bep, eta_max)
        P_base = power_kw(Q_sel, H_sel, eta_base)

        _, eta_ml_val = find_optimal_n(Q_sel, Q_bep=Q_bep, eta_max=eta_max)
        P_ml_val = power_kw(Q_sel, H_sel, eta_ml_val)

        saving_kw = P_base - P_ml_val
        saving_pct = saving_kw / P_base * 100
        
        #st.markdown(f'<div class="section-header"><h2>🔍 {"Analiza punktu pracy" if lang=="PL" else "Operating point analysis"}</h2></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            (f"{eta_base*100:.1f}%", t("current_efficiency"), "blue"),
            (f"{eta_ml_val*100:.1f}%", t("max_efficiency"), "orange"),
            (f"{P_base:.1f} kW", t("without_ml"), "blue"),
            (f"{P_ml_val:.1f} kW", t("with_ml"), "orange"),
        ]
        for col, (val, lbl, typ) in zip([c1,c2,c3,c4], metrics):
            with col:
                cls = "metric-value" if typ == "orange" else "metric-value-blue"
                st.markdown(f'<div class="metric-card"><div class="{cls}">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

        # Daily simulation
        P_base_day, P_ml_day, cost_base_day, cost_ml_day = [], [], [], []
        for i, Q in enumerate(Q_profile):
            if Q < Q_max * 0.02:  # pompa nie pracuje
                P_base_day.append(0)
                P_ml_day.append(0)
                cost_base_day.append(0)
                cost_ml_day.append(0)
                continue
            # Jedna pompa – Q per pompa = Q_total / num_pumps
            Q_one = min(Q / num_pumps, Q_max)
            Q_one = max(Q_one, Q_max * 0.02)
            H = max(qh_curve(np.array([Q_one]), H_nom=H_nom, Q_max=Q_max)[0], 2.0)
            eb = baseline_efficiency(Q_one, control_mode, Q_bep, eta_max)
            pb = power_kw(Q_one, H, eb)
            _, em = find_optimal_n(Q_one, Q_bep=Q_bep, eta_max=eta_max)
            pm = power_kw(Q_one, H, em)
            tariff = TARIFF[i] * energy_price
            P_base_day.append(pb)
            P_ml_day.append(pm)
            cost_base_day.append(pb * tariff)
            cost_ml_day.append(pm * tariff)

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.08,
                            subplot_titles=[t("power"), t("daily_profile")])

        fig.add_trace(go.Scatter(x=list(range(24)), y=P_base_day,
                                 name=t("without_ml"), line=dict(color=BLUE_START, width=2, dash='dot'),
                                 showlegend=True), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(range(24)), y=P_ml_day,
                                 name=t("with_ml"), line=dict(color=ORANGE_START, width=3),
                                 fill='tozeroy', fillcolor='rgba(251,176,64,0.1)',
                                 showlegend=True), row=1, col=1)
            
        Q_profile_one = [q / num_pumps if q >= Q_max * 0.02 else 0 for q in Q_profile]
        fig.add_trace(go.Scatter(x=list(range(24)), y=Q_profile_one,
                                 name=t("flow"), line=dict(color=BLUE_END, width=2),
                                 fill='tozeroy', fillcolor='rgba(0,117,161,0.15)',
                                 showlegend=False), row=2, col=1)

        fig.update_layout(
            title=dict(text="Porównanie mocy i profilu dobowego" if lang=="PL" else "Power and daily profile comparison",
                       font=dict(color=TEXT_LIGHT, size=16)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_LIGHT, family='Exo 2'),
            height=420, margin=dict(t=50, b=40, l=60, r=80),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT)),
        )
        fig.update_yaxes(title_text=t("power"), row=1, col=1)
        fig.update_yaxes(title_text=t("flow"), row=2, col=1)
        fig.update_xaxes(title_text="Godzina [h]" if lang=="PL" else "Hour [h]", row=2, col=1)
        for ax in ['xaxis', 'xaxis2', 'yaxis', 'yaxis2']:
            fig.update_layout(**{ax: dict(gridcolor='rgba(255,255,255,0.06)', color=TEXT_LIGHT)})
        fig.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        fig.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))            
        
        st.plotly_chart(fig, use_container_width=True)

        # Summary metrics
        # total_base = sum(cost_base_day)
        # total_ml = sum(cost_ml_day)
        # saving_day = total_base - total_ml
        
        saving_kw = P_base - P_ml_val
        tariff_avg = np.mean(TARIFF) * energy_price
        saving_day = saving_kw * tariff_avg * hours

        c1, c2, c3 = st.columns(3)
        for col, (val, lbl) in zip([c1,c2,c3], [
            (f"{saving_day:.2f} PLN", t("savings_day")),
            (f"{saving_day*30:.0f} PLN", t("savings_month")),
            (f"{saving_day*365:.0f} PLN", t("savings_year")),
        ]):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    # ── TAB 2: Constant H ──
    with tab2:
        st.markdown(f'<div class="insight-box-blue">{t("explanation_H")}</div>', unsafe_allow_html=True)

        _curve_h_s = BRANCH_CURVES.get(st.session_state.get("industry", t("industries")[0]),
                                        {"H_max_range": 10.0})
        _h_single_max = float(_curve_h_s["H_max_range"])
        
        _h_pump_max = float(st.session_state.get("h_nom_bar", _h_single_max))
        avg_Q_one = float(st.session_state.get("avg_Q_one", Q_bep))
        avg_Q_one = min(avg_Q_one, Q_max)
        _h_default_operating = m_to_bar(qh_curve(np.array([avg_Q_one]), H_nom=H_nom, Q_max=Q_max)[0])
        _h_default_operating = min(max(_h_default_operating, 0.1), _h_pump_max)
                          
       
        H_setpoint_bar = st.slider(t("h_setpoint"), 0.1, _h_pump_max, _h_default_operating, 0.1, key="h_single")
        H_setpoint = bar_to_m(H_setpoint_bar)

        # At given H setpoint, find Q from Q-H curve
        Q_vals_test = np.linspace(1, Q_max, 500)
        H_vals_test = qh_curve(Q_vals_test, H_nom=H_nom, Q_max=Q_max)
        idx = np.argmin(np.abs(H_vals_test - H_setpoint))
        Q_at_H = Q_vals_test[idx]

        eta_base_h = baseline_efficiency(Q_at_H, control_mode, Q_bep, eta_max)
        P_base_h = power_kw(Q_at_H, H_setpoint, eta_base_h)
        _, eta_ml_h = find_optimal_n(Q_at_H, H_setpoint, Q_bep, eta_max)
        P_ml_h = power_kw(Q_at_H, H_setpoint, eta_ml_h)
        saving_h = P_base_h - P_ml_h

        c1, c2, c3, c4 = st.columns(4)
        for col, (val, lbl, typ) in zip([c1,c2,c3,c4], [
            (f"{H_setpoint:.1f} bar", "Setpoint H", "blue"),
            (f"{Q_at_H:.1f} m³/h", "Q aktualne" if lang=="PL" else "Current Q", "blue"),
            (f"{P_base_h:.1f} kW", t("without_ml"), "blue"),
            (f"{P_ml_h:.1f} kW", t("with_ml"), "orange"),
        ]):
            with col:
                cls = "metric-value" if typ == "orange" else "metric-value-blue"
                st.markdown(f'<div class="metric-card"><div class="{cls}">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

        # Show Q-H curve with setpoint line
        fig_h = go.Figure()
        fig_h.add_trace(go.Scatter(
            x=Q_vals_test, y=[m_to_bar(h) for h in H_vals_test],
            name='Q-H', line=dict(color=BLUE_START, width=3)
        ))
        fig_h.add_hline(y=H_setpoint_bar, line_dash="dash",
                        line_color=ORANGE_START, line_width=2,
                        annotation_text=f"H setpoint = {H_setpoint_bar:.1f} bar",
                        annotation_font_color=ORANGE_START,
                        annotation_font_size=14)
        fig_h.add_scatter(x=[Q_at_H], y=[H_setpoint_bar],
                          mode='markers',
                          marker=dict(color=ORANGE_END, size=14, symbol='star'),
                          name="Punkt pracy" if lang=="PL" else "Operating point")

        # Simulate daily with constant H
        P_base_h_day, P_ml_h_day = [], []
        
        for i, Q in enumerate(Q_profile):
            if Q < Q_max * 0.02:
                P_base_h_day.append(0)
                P_ml_h_day.append(0)
                continue
            Qp_h = min(Q / num_pumps, Q_max)
            Qp_h = max(Qp_h, Q_max * 0.02)
            # Bez ML - stały setpoint
            eb = baseline_efficiency(Qp_h, control_mode, Q_bep, eta_max)
            pb = power_kw(Qp_h, H_setpoint, eb)
            # Z ML - obniżony setpoint proporcjonalnie do zapotrzebowania
            Q_ratio = Q / (Q_bep * num_pumps)
            H_ml = max(H_setpoint * Q_ratio, H_setpoint * 0.4)
            _, em = find_optimal_n(Qp_h, H_ml, Q_bep, eta_max)
            pm = power_kw(Qp_h, H_ml, em)
            P_base_h_day.append(pb)
            P_ml_h_day.append(pm)

        fig_h2 = go.Figure()
        fig_h2.add_trace(go.Scatter(x=list(range(24)), y=P_base_h_day,
                                    name=t("without_ml"),
                                    line=dict(color=BLUE_START, width=2, dash='dot')))
        fig_h2.add_trace(go.Scatter(x=list(range(24)), y=P_ml_h_day,
                                    name=t("with_ml"),
                                    line=dict(color=ORANGE_START, width=3),
                                    fill='tozeroy', fillcolor='rgba(251,176,64,0.1)'))

        col_left, col_right = st.columns(2)
        with col_left:
            fig_h.update_layout(
                title=dict(text=t("qh_curve"), font=dict(color=TEXT_LIGHT, size=16)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_LIGHT, family='Exo 2'),
                xaxis=dict(title=t("flow"), gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(title="H [bar]", gridcolor='rgba(255,255,255,0.06)'),
                height=300, margin=dict(t=40,b=40,l=60,r=140),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT))
            )
            
            fig_h.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            fig_h.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            
            st.plotly_chart(fig_h, use_container_width=True)

        with col_right:
            fig_h2.update_layout(
                title=dict(text=t("daily_profile"), font=dict(color=TEXT_LIGHT, size=16)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_LIGHT, family='Exo 2'),
                xaxis=dict(title="h", gridcolor='rgba(255,255,255,0.06)', tickvals=list(range(0,24,3))),
                yaxis=dict(title=t("power"), gridcolor='rgba(255,255,255,0.06)'),
                height=300, margin=dict(t=40,b=40,l=60,r=140),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT))
            )
            
            fig_h2.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            fig_h2.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            
            st.plotly_chart(fig_h2, use_container_width=True)

        saving_h_day = sum(P_base_h_day) - sum(P_ml_h_day)
        c1, c2, c3 = st.columns(3)
        for col, (val, lbl) in zip([c1,c2,c3], [
            (f"{saving_h_day:.2f} PLN", t("savings_day")),
            (f"{saving_h_day*30:.0f} PLN", t("savings_month")),
            (f"{saving_h_day*365:.0f} PLN", t("savings_year")),
        ]):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: CASCADE PUMPS
# ─────────────────────────────────────────────
elif st.session_state.page == "cascade":
    pump_power, num_pumps, hours, energy_price, control_mode, Q_profile, Q_max, Q_bep, eta_max, H_nom = get_params()

    st.markdown(f'<div class="section-header"><h2>{t("nav_cascade")}</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box-blue">{("Kalkulacja dla wybranego punktu pracy Q i H – ML dobiera optymalną liczbę pomp dla tych warunków" if lang=="PL" else "Calculations for selected operating point Q and H – ML selects the optimal number of pumps for these conditions")}</div>', unsafe_allow_html=True)

    col_sl1, col_sl2 = st.columns(2)
    with col_sl1:
        _q_total_max = float(Q_bep * num_pumps)   # Q_nom × num_pumps
        _q_nom_val = float(st.session_state.get("q_nom", Q_max))
        # Default = Q_nom × num_pumps, resets when Q_nom or num_pumps changes
        _q_total_key = f"q_total_{_q_nom_val:.0f}_{num_pumps}"
        if st.session_state.get("q_total_ref_key") != _q_total_key:
            st.session_state["q_total_slider"] = _q_total_max
            st.session_state["q_total_ref_key"] = _q_total_key
        _q_total_default = min(float(st.session_state.get("q_total_slider", _q_total_max)), _q_total_max)
        _q_total_default = max(_q_total_default, float(Q_max * 0.05))
        Q_total = st.slider(t("q_total"), float(Q_max * 0.05), _q_total_max,
                            _q_total_default, float(Q_max * 0.05), key="q_total_slider")
        with col_sl2:
                _curve_h = BRANCH_CURVES.get(st.session_state.get("industry", t("industries")[0]),
                                              {"H_max_range": 10.0})
                _h_cas_max = float(_curve_h["H_max_range"])
                _h_cas_pump_max = float(st.session_state.get("h_nom_bar", _h_cas_max))
                avg_Q_one = float(st.session_state.get("avg_Q_one", Q_bep))
                avg_Q_one = min(avg_Q_one, Q_max)
                _h_cas_default = m_to_bar(qh_curve(np.array([avg_Q_one]), H_nom=H_nom, Q_max=Q_max)[0])
                _h_cas_default = min(max(_h_cas_default, 0.1), _h_cas_pump_max)
                H_set_cas_bar = st.slider(t("h_setpoint"), 0.1, _h_cas_pump_max, _h_cas_default, 0.1, key="h_cascade")
                H_set_cas = bar_to_m(H_set_cas_bar)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    # ML: find best pump combination
    def cascade_optimization(Q_total, H_set, num_pumps, Q_max, Q_bep, eta_max):
        results = []
        for n_active in range(1, num_pumps + 1):
            Q_per_pump = Q_total / n_active
            # Filtr: Q_per musi być w realnym zakresie pracy pompy
            if Q_per_pump > Q_max * 0.9:
                continue
            if Q_per_pump < Q_max * 0.05:
                continue
            eta = efficiency_curve(Q_per_pump, Q_bep, eta_max)
            # H_nom stałe – PID pilnuje ciśnienia
            P_per_pump = power_kw(Q_per_pump, H_set, eta)
            P_total = P_per_pump * n_active
            if P_total <= 0 or eta <= 0:
                continue
            results.append({
                "n_active": n_active,
                "Q_per": Q_per_pump,
                "eta": eta,
                "P_total": P_total,
                "H": H_nom,
            })
        if not results:
            return None, []
        best = min(results, key=lambda x: x["P_total"])
        return best, results

    best, all_results = cascade_optimization(Q_total, H_set_cas, num_pumps, Q_max, Q_bep, eta_max)

    # Baseline: all pumps on
    Q_per_base = Q_total / num_pumps
    Q_per_base = min(Q_per_base, Q_max)
    eta_base_cas = baseline_efficiency(Q_per_base, control_mode, Q_bep, eta_max)
    P_per_base = power_kw(Q_per_base, H_set_cas, eta_base_cas)
    P_base_cas = P_per_base * num_pumps  # łączna moc wszystkich pomp

    if best:
        saving_cas = P_base_cas - best["P_total"]
        saving_pct_cas = saving_cas / P_base_cas * 100

        # Pump indicators
        col_base, col_ml = st.columns(2)
        with col_base:
            st.markdown(f"<b style='color:{BLUE_START};'>{t('without_ml')}</b>", unsafe_allow_html=True)
            pumps_html = "".join([f'<span class="pump-on">P{i+1} ●</span>' for i in range(num_pumps)])
            st.markdown(pumps_html, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="insight-box-blue" style="margin-top:8px;">
                η = {eta_base_cas*100:.0f}% &nbsp;|&nbsp; {'Moc łączna' if lang=='PL' else 'Total power'} = {P_base_cas:.1f} kW &nbsp;({num_pumps} {('pompa' if num_pumps==1 else 'pompy' if num_pumps in [2,3,4] else 'pomp') if lang=='PL' else ('pump' if num_pumps==1 else 'pumps')} × {P_per_base:.1f} kW)
            </div>""", unsafe_allow_html=True)

        with col_ml:
            st.markdown(f"<b style='color:{ORANGE_START};'>{t('with_ml')}</b>", unsafe_allow_html=True)
            pumps_html = ""
            for i in range(num_pumps):
                if i < best["n_active"]:
                    pumps_html += f'<span class="pump-on">P{i+1} ●</span>'
                else:
                    pumps_html += f'<span class="pump-off">P{i+1} ○</span>'
            st.markdown(pumps_html, unsafe_allow_html=True)
            P_per_ml = best["P_total"] / best["n_active"]
            st.markdown(f"""
            <div class="insight-box" style="margin-top:8px;">
                η = {best['eta']*100:.0f}% &nbsp;|&nbsp; {'Moc łączna' if lang=='PL' else 'Total power'} = {best['P_total']:.1f} kW &nbsp;({best['n_active']} {('pompa' if best['n_active']==1 else 'pompy' if best['n_active'] in [2,3,4] else 'pomp') if lang=='PL' else ('pump' if best['n_active']==1 else 'pumps')} × {P_per_ml:.1f} kW)
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

        # ML decision table
        st.markdown(f"<b style='color:{TEXT_MUTED}; font-size:1.1rem;'>{t('ml_checked')}</b>", unsafe_allow_html=True)
        rows = ""
        for r in all_results:
            is_best = r["n_active"] == best["n_active"]
            star = f'<span style="color:{ORANGE_START}; font-weight:800;"> {t("selected")}</span>' if is_best else ""
            check = "✓" if is_best else "✗"
            color = ORANGE_START if is_best else TEXT_MUTED
            rows += f"""<tr>
                <td style="color:{color};">{check} {r['n_active']} {('pompa' if r['n_active']==1 else 'pompy' if r['n_active'] in [2,3,4] else 'pomp') if lang=='PL' else ('pump' if r['n_active']==1 else 'pumps')}</td>
                <td>{r['Q_per']:.1f} m³/h</td>
                <td>{r['eta']*100:.0f}%</td>
                <td>{r['P_total']:.1f} kW{star}</td>
            </tr>"""

        headers = ["Pompy" if lang=="PL" else "Pumps",
                   "Q/pompa" if lang=="PL" else "Q/pump",
                   "Sprawność" if lang=="PL" else "Efficiency", "P total"]
        th = "".join(f"<th>{h}</th>" for h in headers)
        st.markdown(f"""
        <table class="comparison-table">
            <thead><tr>{th}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        saving_day_cas = saving_cas * hours * np.mean(TARIFF) * energy_price
        for col, (val, lbl) in zip([c1,c2,c3], [
            (f"{saving_pct_cas:.1f}%", "Oszczędność mocy" if lang=="PL" else "Power savings"),
            (f"{saving_day_cas:.0f} PLN", t("savings_day")),
            (f"{saving_day_cas*365:.0f} PLN", t("savings_year")),
        ]):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

        col_line, col_bar = st.columns([2,1])

        # LEFT: Staircase chart - uses same cascade_optimization as table
        with col_line:
            Q_range = np.linspace(Q_bep * 0.3, Q_bep * num_pumps, 150)
            P_base_list, P_ml_list_c = [], []

            for Qr in Q_range:
                # Baseline: wszystkie pompy, H_produced
                Qp = min(Qr / num_pumps, Q_max)
                Qp = max(Qp, Q_max * 0.05)
                eb = baseline_efficiency(Qp, control_mode, Q_bep, eta_max)
                P_base_list.append(power_kw(Qp, H_set_cas, eb) * num_pumps)

                # ML: minimum mocy spośród wszystkich kombinacji pomp
                best_P = 999
                for n in range(1, num_pumps + 1):
                    Qp_n = Qr / n
                    if Qp_n > Q_max * 0.9: continue
                    if Qp_n < Q_max * 0.05: continue
                    em = efficiency_curve(Qp_n, Q_bep, eta_max)
                    Pm = power_kw(Qp_n, H_set_cas, em) * n
                    if Pm < best_P:
                        best_P = Pm
                P_ml_list_c.append(best_P if best_P < 999 else P_base_list[-1])

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=Q_range, y=P_base_list,
                name="Bez ML" if lang=="PL" else "Without ML",
                line=dict(color=BLUE_START, width=2, dash='dot'), mode='lines'
            ))
            fig_line.add_trace(go.Scatter(
                x=Q_range, y=P_ml_list_c,
                name="Z ML" if lang=="PL" else "With ML",
                line=dict(color=ORANGE_START, width=3, shape='hv'),
                fill='tozeroy', fillcolor='rgba(251,176,64,0.08)', mode='lines'
            ))
            fig_line.add_vline(x=Q_total, line_dash="dash",
                               line_color="#ffffff", line_width=1,
                               annotation_text="Q aktualne" if lang=="PL" else "Current Q",
                               annotation_font_color=TEXT_MUTED,
                               annotation_font_size=14)
            fig_line.update_layout(
                title=dict(text="Moc łączna vs Q [kW]" if lang=="PL" else "Total power vs Q [kW]",
                           font=dict(color=TEXT_LIGHT, size=16)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_LIGHT, family='Exo 2'),
                xaxis=dict(title=t("q_total"), gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(title=t("power"), gridcolor='rgba(255,255,255,0.06)'),
                height=380, margin=dict(t=50, b=40, l=60, r=20),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT))
            )
            
            fig_line.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            fig_line.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            
            st.plotly_chart(fig_line, use_container_width=True)

        # RIGHT: Bar chart for current Q
        with col_bar:
            categories = [
                "Bez ML" if lang=="PL" else "Without ML",
                "Z ML"
            ]
            powers = [P_base_cas, best["P_total"]]
            etas = [eta_base_cas * 100, best["eta"] * 100]
            colors_bar = [BLUE_START, ORANGE_START]
            saving_bar = P_base_cas - best["P_total"]

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=categories,
                y=powers,
                marker_color=colors_bar,
                text=[f"{p:.1f} kW<br>η={e:.0f}%" for p, e in zip(powers, etas)],
                textposition='outside',
                textfont=dict(color=TEXT_LIGHT, size=16),
                width=0.5
            ))
            fig_bar.update_layout(
                title=dict(
                    text=f"{'Przy Q=' if lang=='PL' else 'At Q='}{Q_total:.0f} m³/h | {'Oszczędność' if lang=='PL' else 'Saving'}: {saving_bar:.1f} kW ({saving_pct_cas:.0f}%)",
                    font=dict(color=TEXT_LIGHT, size=16)
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_LIGHT, family='Exo 2'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
                yaxis=dict(title=t("power"), gridcolor='rgba(255,255,255,0.06)'),
                height=380, margin=dict(t=50, b=40, l=60, r=20),
                bargap=0.4, showlegend=False
            )
            
            fig_bar.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            fig_bar.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                    title_font=dict(size=14, color=TEXT_LIGHT))
            
            st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE: ROI
# ─────────────────────────────────────────────
elif st.session_state.page == "roi":
    pump_power, num_pumps, hours, energy_price, control_mode, Q_profile, Q_max, Q_bep, eta_max, H_nom = get_params()

    st.markdown(f'<div class="section-header"><h2>💰 {t("roi_title")}</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-box-blue">{("Kalkulacja dla całego roku – uwzględniaja dobowy profil zużycia branży i godzinowe ceny energii" if lang=="PL" else "Calculations for the full year – based on industry daily consumption profile and hourly energy prices")}</div>', unsafe_allow_html=True)
    # ── Pętla dobowa: moc bez ML i z ML dla każdej godziny ──
    # Baseline: wszystkie pompy pracują, sterowanie wg trybu z danych instalacji
    # ML: optymalna liczba pomp minimalizująca moc łączną (ta sama logika co Kaskada)
    P_base_day, P_ml_day = [], []

    for Q in Q_profile:
        # Godziny postoju — pompa nie pracuje, moc = 0
        if Q < Q_max * 0.02:
            P_base_day.append(0)
            P_ml_day.append(0)
            continue
        # Baseline: Q rozdzielone równo na wszystkie pompy
        Qp_r = min(Q / num_pumps, Q_max)
        Qp_r = max(Qp_r, Q_max * 0.02)
        H = max(qh_curve(np.array([Qp_r]), H_nom=H_nom, Q_max=Q_max)[0], 2.0)
        eb = baseline_efficiency(Qp_r, control_mode, Q_bep, eta_max)
        pb = power_kw(Qp_r, H, eb) * num_pumps
        # ML: szuka optymalnej liczby pomp (1 do num_pumps)
        # filtr zgodny z cascade_optimization: 0.05–0.9 Q_max per pompa
        best_P_ml_r = 999
        for n_opt in range(1, num_pumps + 1):
            Qp = Q / n_opt
            if Qp > Q_max * 0.9: continue
            if Qp < Q_max * 0.05: continue
            em = efficiency_curve(Qp, Q_bep, eta_max)
            Hm = max(qh_curve(np.array([Qp]), H_nom=H_nom, Q_max=Q_max)[0], 2.0)
            Pm = power_kw(Qp, Hm, em) * n_opt
            if Pm < best_P_ml_r: best_P_ml_r = Pm
        P_base_day.append(pb)
        P_ml_day.append(best_P_ml_r if best_P_ml_r < 999 else pb)

    # ── Energia roczna ──
    # sum(P_*_day) = energia dobowa [kWh] — zera z godzin postoju już uwzględnione
    # * 365 = energia roczna [kWh/rok]
    E_base_year = sum(P_base_day) * 365
    E_ml_year = sum(P_ml_day) * 365

    # ── Koszty roczne ──
    # np.mean(TARIFF) = znormalizowany współczynnik taryfy (średnia = 1.0)
    cost_base_year = sum(P_base_day[i] * TARIFF[i] * energy_price for i in range(24)) * 365
    cost_ml_year = sum(P_ml_day[i] * TARIFF[i] * energy_price for i in range(24)) * 365
    saving_year = cost_base_year - cost_ml_year
    saving_month = saving_year / 12

    # ── Sprawności i moce średnie do tabeli ──
    # Liczone tylko z godzin gdy pompa pracuje (bez zer)
    P_base_working = [p for p in P_base_day if p > 0]
    P_ml_working = [p for p in P_ml_day if p > 0]
    avg_base = np.mean(P_base_working) if P_base_working else 0
    avg_ml = np.mean(P_ml_working) if P_ml_working else 0

    # Sprawność z avg_Q tylko z godzin pracy — spójne z Analiza obecna
    Q_working_roi = [q for q in Q_profile if q > Q_max * 0.02]
    avg_Q_roi = np.mean(Q_working_roi) / num_pumps if Q_working_roi else Q_bep
    avg_Q_roi = min(avg_Q_roi, Q_max)
    eta_avg_base = baseline_efficiency(avg_Q_roi, control_mode, Q_bep, eta_max)
    _, eta_avg_ml = find_optimal_n(avg_Q_roi, Q_bep=Q_bep, eta_max=eta_max)

    # ── Koszt wdrożenia i zwrot ──
    impl_cost = num_pumps * (8000 + pump_power * 300)
    payback_months = impl_cost / saving_month if saving_month > 0 else 999

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, typ) in zip([c1,c2,c3,c4], [
        (f"{saving_year:,.0f} PLN", t("savings_year"), "orange"),
        (f"{saving_month:,.0f} PLN", t("savings_month"), "orange"),
        (f"{impl_cost:,.0f} PLN", t("investment"), "blue"),
        (f"{payback_months:.0f} {t('month')}", t("payback"), "blue"),
    ]):
        with col:
            cls = "metric-value" if typ == "orange" else "metric-value-blue"
            st.markdown(f'<div class="metric-card"><div class="{cls}">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    # Comparison table
    col_left, col_right = st.columns([1, 1])

    with col_left:
        rows = ""
        items = [
            (t("efficiency"), f"{eta_avg_base*100:.0f}%", f"{eta_avg_ml*100:.0f}%"),
            (t("avg_power"), f"{avg_base:.1f} kW", f"{avg_ml:.1f} kW"),
            (t("monthly_cost"), f"{cost_base_year/12:,.0f} PLN", f"{cost_ml_year/12:,.0f} PLN"),
            (t("yearly_cost"), f"{cost_base_year:,.0f} PLN", f"{cost_ml_year:,.0f} PLN"),
        ]
        for lbl, base, ml in items:
            rows += f"""<tr>
                <td style="text-align:left;">{lbl}</td>
                <td style="color:{BLUE_START};">{base}</td>
                <td><span class="highlight-orange">{ml}</span></td>
            </tr>"""

        th_base = t("without_ml")
        th_ml = t("with_ml")
        st.markdown(f"""
        <table class="comparison-table">
            <thead><tr>
                <th style="text-align:left;">Parametr</th>
                <th>{th_base}</th>
                <th>{th_ml}</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_right:
        # Wykres skumulowanych kosztów energii — 5 lat (60 miesięcy)
        # Bez ML: rosnące koszty energii bez inwestycji
        # Z ML: koszt wdrożenia na początku + niższe koszty energii
        months = list(range(0, 61))
        cost_base_cum = [m * cost_base_year / 12 for m in months]
        cost_ml_cum   = [impl_cost + m * cost_ml_year / 12 for m in months]

        # Punkt zwrotu — pierwszy miesiąc gdy linia ML przecina linię Bez ML
        breakeven = payback_months if payback_months < 60 else None

        fig_roi = go.Figure()
        fig_roi.add_trace(go.Scatter(
            x=months, y=cost_base_cum,
            name=t("without_ml"),
            line=dict(color=BLUE_START, width=3)
        ))
        fig_roi.add_trace(go.Scatter(
            x=months, y=cost_ml_cum,
            name=t("with_ml"),
            line=dict(color=ORANGE_START, width=3),
            fill='tonexty', fillcolor='rgba(0,189,242,0.05)'
        ))
        if breakeven:
            fig_roi.add_vline(x=breakeven, line_dash="dash",
                              line_color=ORANGE_END, line_width=2,
                              annotation_text=f"⭐ Zwrot" if lang=="PL" else "⭐ Breakeven",
                              annotation_font_size=14,
                              annotation_font_color=ORANGE_END)

        fig_roi.update_layout(
            title=dict(text="Skumulowane koszty energii – 5 lat [PLN]" if lang=="PL" else "Cumulative energy costs – 5 years [PLN]",
                       font=dict(color=TEXT_LIGHT, size=16)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT_LIGHT, family='Exo 2'),
            xaxis=dict(title="Miesiąc" if lang=="PL" else "Month",
                       gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(title=t("cumulative"), gridcolor='rgba(255,255,255,0.06)'),
            height=370, margin=dict(t=50,b=40,l=80,r=80),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT_LIGHT))
        )
        
        fig_roi.update_xaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        fig_roi.update_yaxes(tickfont=dict(size=14, color=TEXT_LIGHT),
                                title_font=dict(size=14, color=TEXT_LIGHT))
        
        st.plotly_chart(fig_roi, use_container_width=True)

    st.markdown('<div class="wave-divider"></div>', unsafe_allow_html=True)

    # Final message
    E_base_year = sum(P_base_day) * 365
    E_ml_year = sum(P_ml_day) * 365
    co2_saved = (E_base_year - E_ml_year) * 0.76 / 1000
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px;">
        <div class="insight-box">
            <b style="color:{ORANGE_START}; font-size:1.1rem;">💡 {saving_year:,.0f} PLN/rok</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"Oszczędność przy obecnych cenach energii" if lang=="PL" else "Savings at current energy prices"}
            </span>
        </div>
        <div class="insight-box-blue">
            <b style="color:{BLUE_START}; font-size:1.1rem;">🌱 {co2_saved:.1f} t CO₂/rok</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"Redukcja emisji – raportowanie ESG" if lang=="PL" else "Emission reduction – ESG reporting"}
            </span>
        </div>
        <div class="insight-box">
            <b style="color:{ORANGE_START}; font-size:1.1rem;">⚡ {payback_months:.1f} {t('month')}</b><br>
            <span style="color:{TEXT_MUTED}; font-size:1.1rem;">
                {"Czas zwrotu inwestycji" if lang=="PL" else "Investment payback period"}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
