import streamlit as st
import requests
import os
import base64
import datetime
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="LexAssist AI - Modern Legal Document Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom Styling (The "Quantum-Luxe" Theme) ---
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    :root {
        --primary-bg: #0a0e1a;
        --card-bg: rgba(255, 255, 255, 0.05);
        --accent-cyan: #00f2ff;
        --accent-magenta: #ff00ff;
        --accent-blue: #3b82f6;
        --text-color: #ffffff;
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    body, .stApp {
        background: radial-gradient(circle at top right, #1a237e, #0a0e1a);
        color: var(--text-color);
        font-family: 'Outfit', sans-serif;
        overflow-x: hidden;
    }

    /* Global Scanline Effect */
    body::before {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
        z-index: 10000;
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
        opacity: 0.15;
    }

    /* Cinematic Background Orbits */
    .bg-orbit {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        z-index: -1;
        opacity: 0.4;
        animation: float 20s infinite alternate ease-in-out;
    }
    .orbit-1 { width: 400px; height: 400px; background: rgba(0, 242, 255, 0.15); top: -100px; right: -100px; }
    .orbit-2 { width: 600px; height: 600px; background: rgba(255, 0, 255, 0.1); bottom: -200px; left: -200px; animation-delay: -5s; }
    
    @keyframes float {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(50px, 100px) scale(1.1); }
    }

    /* Page Entrance Animation */
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(20px); filter: blur(10px); }
        to { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .stApp > div { animation: fadeInSlide 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }

    /* Glassmorphism Refinement (Noise & Depth) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 2.5rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.02);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('https://grainy-gradients.vercel.app/noise.svg');
        opacity: 0.05;
        pointer-events: none;
    }
    .glass-card:hover {
        border-color: rgba(0, 242, 255, 0.3);
        box-shadow: 0 30px 60px rgba(0, 242, 255, 0.1);
        transform: translateY(-8px) scale(1.01);
    }

    /* Fixed Header Styling */
    .fixed-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 70px;
        background: rgba(10, 14, 26, 0.9);
        backdrop-filter: blur(20px);
        z-index: 999;
    }

    .brand { 
        font-size: 1.8rem !important; 
        font-weight: 800 !important; 
        color: #00f2ff !important; 
        letter-spacing: -1px; 
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }
    
    /* Hero Section */
    .hero-title {
        font-size: clamp(2rem, 8vw, 4rem);
        font-weight: 700;
        text-align: center;
        margin-top: 5rem;
        background: linear-gradient(90deg, #fff, var(--accent-cyan), #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        text-align: center;
        color: #aaa;
        font-size: clamp(0.9rem, 3vw, 1.3rem);
        margin-bottom: 4rem;
    }

    /* Custom File Uploader */
    .stFileUploader {
        background: var(--card-bg) !important;
        border: 2px dashed rgba(0, 242, 255, 0.2) !important;
        border-radius: 24px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader:hover {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2) !important;
        transform: translateY(-2px);
    }

    /* Risk Circle & Metric Cards */
    .risk-circle-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
    .circle-svg { transform: rotate(-90deg); width: 220px; }
    .circle-bg { fill: none; stroke: #1a1a1a; stroke-width: 8; }
    .circle-progress { fill: none; stroke-width: 10; stroke-linecap: round; transition: stroke-dashoffset 1.5s ease; }
    
    .metric-value { font-size: 1.6rem; font-weight: 700; }

    /* Metric Bar ( Mockup Style ) */
    .metric-bar {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(0, 242, 255, 0.3);
        transform: translateY(-5px);
    }
    .metric-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .metric-card:hover .metric-icon {
        transform: scale(1.1) rotate(-5deg);
        box-shadow: 0 0 15px currentColor;
    }

    /* Glossy Card Overlay */
    .glass-card::after {
        content: "";
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
        pointer-events: none;
        z-index: 1;
    }
    /* High-End Risk Gauge */
    /* High-End Risk Gauge */
    .risk-gauge-container {
        position: relative;
        width: 250px;
        height: 180px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }
    .gauge-svg {
        filter: drop-shadow(0 0 15px rgba(0, 242, 255, 0.4));
        margin-top: 10px;
    }
    .gauge-bg {
        fill: none;
        stroke: rgba(255, 255, 255, 0.05);
        stroke-width: 10;
        stroke-linecap: round;
    }
    .gauge-fill {
        fill: none;
        stroke: url(#gauge-gradient);
        stroke-width: 12;
        stroke-linecap: round;
        transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .risk-value {
        margin-top: -72px;
        font-size: 3.4rem;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 0 30px var(--accent-cyan);
        z-index: 2;
    }
    .risk-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: var(--accent-cyan);
        opacity: 0.9;
        margin-top: 5px;
        font-weight: 700;
    }

    /* Premium Buttons (Magnetic & Neon) */
    .stButton > button {
        border-radius: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
        padding: 0.6rem 1.8rem !important;
    }
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 10px 25px rgba(0, 242, 255, 0.3) !important;
        background: rgba(0, 242, 255, 0.08) !important;
    }
    .stButton > button[type="primary"] {
        background: linear-gradient(135deg, var(--accent-cyan), #00a8ff) !important;
        border: none !important;
        color: #000 !important;
        font-weight: 800 !important;
        box-shadow: 0 5px 20px rgba(0, 242, 255, 0.4) !important;
    }
    .stButton > button[type="primary"]:hover {
        box-shadow: 0 10px 40px rgba(0, 242, 255, 0.6) !important;
        transform: translateY(-6px) scale(1.05) !important;
    }

    /* Glass-Focus Inputs & Selectboxes */
    div[data-baseweb="input"], div[data-baseweb="select"], .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3) !important;
        background: rgba(0, 242, 255, 0.05) !important;
    }

    /* Staggered Card Animations */
    .stagger-1 { animation: fadeInSlide 0.6s ease-out forwards; animation-delay: 0.1s; opacity: 0; }
    .stagger-2 { animation: fadeInSlide 0.6s ease-out forwards; animation-delay: 0.2s; opacity: 0; }
    .stagger-3 { animation: fadeInSlide 0.6s ease-out forwards; animation-delay: 0.3s; opacity: 0; }
    .metric-info {
        display: flex;
        flex-direction: column;
    }
    .metric-value { font-size: 1.6rem; font-weight: 700; line-height: 1; }
    .metric-label { font-size: 0.75rem; color: #888; }
    .metric-sublabel { font-size: 0.65rem; color: #555; }

    /* Clause Breakdown Table ( Mockup Style ) */
    .breakdown-table {
        width: 100%;
        border-collapse: collapse;
    }
    .breakdown-table th {
        text-align: left;
        color: #444;
        font-size: 0.85rem;
        font-weight: 400;
        padding-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .breakdown-table td {
        padding: 1.8rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .clause-row { display: flex; align-items: center; gap: 12px; }
    .clause-icon { 
        width: 32px; 
        height: 32px; 
        background: rgba(255,255,255,0.05); 
        border-radius: 6px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        color: #888; 
    }
    .clause-name { 
        font-size: 0.85rem; 
        font-weight: 600; 
        color: #fff;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .clause-type { font-size: 0.7rem; color: #555; }

    .risk-badge-mini {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .status-badge-mini {
        padding: 4px 15px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        background: rgba(255,255,255,0.05);
        color: #aaa;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Key Points & Suggestions */
    .key-points-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 2rem; color: #fff; }
    .suggestion-panel {
        background: rgba(0, 255, 136, 0.03);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid var(--accent-green);
        margin-top: 2rem;
    }
    
    .high-risk-alert {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid rgba(255, 75, 75, 0.2);
        border-radius: 20px;
        padding: 8px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    /* Stat Cards */
    .stat-card {
        text-align: center;
        padding: 1.8rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--glass-border);
    }
    .stat-value { font-size: 2.22rem; font-weight: 700; color: var(--accent-cyan); }
    .stat-label { font-size: 0.95rem; color: #888; }

    /* Tables */
    table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
    th { text-align: left; padding: 1.2rem; color: #666; font-size: 0.85rem; text-transform: uppercase; }
    td { padding: 1.5rem 1.2rem; border-top: 1px solid var(--glass-border); }
    
    .risk-badge { padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 0.8rem; }
    .risk-high { color: #ff4b4b; background: rgba(255, 75, 75, 0.15); border: 1px solid rgba(255, 75, 75, 0.3); }
    .risk-med { color: #ff8c00; background: rgba(255, 140, 0, 0.15); border: 1px solid rgba(255, 140, 0, 0.3); }

    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 1rem;
        margin-top: 5rem;
        border-top: 1px solid var(--glass-border);
        color: #666;
    }
    .footer-highlight { color: var(--accent-cyan); font-weight: 600; }

    /* Profile Chip (Circle Style) with Pulse */
    .stButton > button[key*="nav_profile"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid var(--accent-cyan) !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: var(--accent-cyan) !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3) !important;
        animation: pulse 3s infinite ease-in-out;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 15px rgba(0, 242, 255, 0.2); transform: scale(1); }
        50% { box-shadow: 0 0 30px rgba(0, 242, 255, 0.5); transform: scale(1.05); }
    }
    .stButton > button[key*="nav_profile"]:hover {
        background: var(--accent-cyan) !important;
        color: #0a0e1a !important;
        box-shadow: 0 0 40px rgba(0, 242, 255, 0.6) !important;
        transform: scale(1.15) rotate(10deg) !important;
        animation: none;
    }

    /* Specialized Buttons & Danger Zone */
    .btn-remove button {
        color: #ff4b4b !important;
        border-color: rgba(255, 75, 75, 0.2) !important;
        background: rgba(255, 75, 75, 0.05) !important;
    }
    .btn-danger button {
        background: rgba(255, 75, 75, 0.15) !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        color: #ff4b4b !important;
        font-weight: 700 !important;
    }
    .danger-title { color: #ff4b4b; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; }

    /* Settings Layout specific */
    [data-testid="stVerticalBlockBordered"] h3 {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #fff !important;
        margin-bottom: 1rem !important;
    }
    .settings-label { font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem; }

    /* Responsiveness */
    @media (max-width: 768px) {
        .fixed-header { height: auto; padding: 10px 0; }
        .hero-title { font-size: 2.2rem; }
        .block-container { padding-top: 8rem !important; }
    }

    /* Nuclear CSS to hide Streamlit header and top decoration line */
    [data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton, footer { display: none !important; visibility: hidden !important; }
    [data-testid="stDecoration"] { display: none !important; height: 0 !important; opacity: 0 !important; }
    #root > div:nth-child(1) > div > div > div > div > section > header { display: none !important; }
    header { background: transparent !important; border: none !important; box-shadow: none !important; }
    .block-container { padding-top: 5rem !important; }

    /* Custom st.download_button to match breadcrumb style */
    .stDownloadButton > button {
        background: var(--accent-blue) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 5px 15px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        line-height: 1.5 !important;
    }
    .stDownloadButton > button:hover {
        background: #2563eb !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }

    /* Statutory Comparison Styles */
    .statutory-card {
        background: linear-gradient(135deg, rgba(0, 242, 255, 0.05) 0%, rgba(255, 0, 255, 0.05) 100%);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .statutory-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--accent-cyan);
    }
    .statutory-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
    }
    .statutory-section-tag {
        background: rgba(0, 242, 255, 0.1); color: var(--accent-cyan); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; border: 1px solid rgba(0, 242, 255, 0.2);
    }
    .statutory-concept { font-size: 1rem; font-weight: 700; color: #fff; }
    .statutory-provision { font-size: 0.85rem; color: #ccc; line-height: 1.5; margin: 10px 0; font-style: italic; }
    .statutory-note { font-size: 0.75rem; color: var(--accent-magenta); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    
    .legal-btn {
        background: transparent !important;
        border: 1px solid var(--accent-cyan) !important;
        color: var(--accent-cyan) !important;
        padding: 5px 15px !important;
        border-radius: 30px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .legal-btn:hover {
        background: var(--accent-cyan) !important;
        color: #0a0e1a !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }

    /* Risk Indicator Chips */
    .risk-indicator-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 12px;
        background: rgba(255, 75, 75, 0.05);
        border: 1px solid rgba(255, 75, 75, 0.3);
        color: #ff4b4b;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 4px;
        box-shadow: 0 0 10px rgba(255, 75, 75, 0.1);
        animation: pulse-danger 2s infinite ease-in-out;
    }
    @keyframes pulse-danger {
        0%, 100% { border-color: rgba(255, 75, 75, 0.3); box-shadow: 0 0 10px rgba(255, 75, 75, 0.1); }
        50% { border-color: rgba(255, 75, 75, 0.6); box-shadow: 0 0 20px rgba(255, 75, 75, 0.2); }
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# --- Components ---
def render_header():
    # Inject background orbits visually
    st.markdown('<div class="bg-orbit orbit-1"></div><div class="bg-orbit orbit-2"></div>', unsafe_allow_html=True)
    st.markdown('<div class="fixed-header"></div>', unsafe_allow_html=True)
    cols = st.columns([2, 5, 2])
    
    with cols[0]:
        st.markdown('<div style="height: 60px; display: flex; align-items: center; position: relative; z-index: 1001;"><div class="brand">LexAssist AI</div></div>', unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown('<div style="position: relative; z-index: 1001; height: 60px; display: flex; align-items: center;">', unsafe_allow_html=True)
        nav_cols = st.columns(3)
        if nav_cols[0].button("Dashboard", use_container_width=True, key="nav_dash"):
            st.session_state.page = "Dashboard"
            st.session_state.pop('analysis_done', None)
            st.rerun()
        if nav_cols[1].button("History", use_container_width=True, key="nav_hist"):
            st.session_state.page = "History"
            st.rerun()
        if nav_cols[2].button("Settings", use_container_width=True, key="nav_sett"):
            st.session_state.page = "Settings"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with cols[2]:
        st.markdown('<div style="display: flex; justify-content: flex-end; align-items: center; height: 60px; position: relative; z-index: 1001;">', unsafe_allow_html=True)
        user_name = st.session_state.get('user_name', 'Arpit Gupta')
        initials = "".join([n[0] for n in user_name.split()])[:2].upper()
        # Circular button with just initials
        if st.button(initials, key="nav_profile", help=f"Logged in as {user_name}"):
            st.session_state.page = "Profile"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_risk_gauge(score, level):
    dash_array = 565.48 # circumference for radius 90
    offset = dash_array - (score / 100) * dash_array
    color = "var(--accent-cyan)" if score < 40 else ("var(--accent-orange)" if score < 70 else "var(--accent-red)")
    
    st.markdown(f"""
<div class="risk-circle-container">
    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 10px; width: 100%; margin-bottom: 2rem; font-weight: 600; font-size: 0.85rem; color: #fff;">
        Document Risk Assessment
    </div>
    <div style="position: relative; display: flex; align-items: center; justify-content: center;">
        <svg class="circle-svg" viewBox="0 0 200 200">
            <circle class="circle-bg" cx="100" cy="100" r="90"></circle>
            <circle class="circle-progress" cx="100" cy="100" r="90" 
                style="stroke-dasharray: {dash_array}; stroke-dashoffset: {offset}; stroke: {color};"></circle>
        </svg>
        <div style="position: absolute; text-align: center;">
            <div style="font-size: 3.5rem; font-weight: 700; color: #fff; line-height: 1;">{score}%</div>
            <div style="background: {color}22; color: {color}; border: 1px solid {color}44; padding: 2px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; margin-top: 10px;">
                <i class="fas fa-circle" style="font-size: 0.4rem; vertical-align: middle; margin-right: 5px;"></i> {level} Risk
            </div>
        </div>
    </div>
    <div style="display: flex; gap: 15px; margin-top: 1.5rem; justify-content: center; opacity: 0.5; font-size: 0.8rem;">
        <span><i class="far fa-file-pdf"></i> PDF</span>
        <span><i class="far fa-file-word"></i> DOCX</span>
        <span><i class="far fa-file-alt"></i> TXT</span>
    </div>
</div>
""", unsafe_allow_html=True)

def render_footer():
    st.markdown("""
<div class="footer">
    <p>© 2026 <span class="footer-highlight">LexAssist AI</span> • Your privacy is our priority.</p>
    <p style="font-size: 0.8rem; margin-top: 5px;">
        <i class="fas fa-shield-alt"></i> We do <span class="footer-highlight">not store</span> your document data or analysis results after the session ends.
    </p>
</div>
""", unsafe_allow_html=True)

# --- App Logic ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "history" not in st.session_state:
    st.session_state.history = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Arpit Gupta"
if "user_email" not in st.session_state:
    st.session_state.user_email = "john.doe@example.com"

inject_custom_css()
render_header()

# Main Container
container = st.container()

with container:
    if st.session_state.page == "Dashboard":
        if 'analysis_done' not in st.session_state:
            st.markdown('<h1 class="hero-title">Understand Legal Documents in Seconds</h1>', unsafe_allow_html=True)
            st.markdown('<p class="hero-subtitle">Upload your documents safely and get AI-powered insights instantly.</p>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                uploaded_file = st.file_uploader("Drag & Drop your document here", type=["pdf", "txt", "docx"])
                
                if uploaded_file is not None:
                    with st.spinner("Analyzing contract..."):
                        # Call Backend
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        try:
                            response = requests.post("http://127.0.0.1:8000/upload-contract", files=files)
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.result = result
                                st.session_state.analysis_done = True
                                
                                # Add to History
                                history_entry = {
                                    "filename": uploaded_file.name,
                                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "risk_score": result['risk_analysis']['risk_score'],
                                    "risk_level": result['risk_analysis']['risk_level'],
                                    "result": result
                                }
                                st.session_state.history.insert(0, history_entry)
                                st.rerun()
                            else:
                                st.error("Failed to analyze document.")
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")

            # Summary Stats
            st.markdown("<br><br>", unsafe_allow_html=True)
            s1, s2, s3, s4 = st.columns(4)
            s1.markdown('<div class="stat-card"><div class="stat-value">42</div><div class="stat-label">Documents Analyzed</div></div>', unsafe_allow_html=True)
            s2.markdown('<div class="stat-card"><div class="stat-value">56%</div><div class="stat-label">Avg Risk Score</div></div>', unsafe_allow_html=True)
            s3.markdown('<div class="stat-card"><div class="stat-value">128</div><div class="stat-label">Clauses Detected</div></div>', unsafe_allow_html=True)
            s4.markdown('<div class="stat-card"><div class="stat-value">23</div><div class="stat-label">Compliance Alerts</div></div>', unsafe_allow_html=True)

        else:
            # RESULTS VIEW (3-COLUMN MOCKUP LAYOUT)
            res = st.session_state.result
            risk_score = res['risk_analysis']['risk_score']
            risk_level = res['risk_analysis']['risk_level']
            
            # Breadcrumbs row
            bc_col1, bc_col2 = st.columns([5, 1.2])
            with bc_col1:
                st.markdown(f'''
                <div style="font-size: 0.85rem; color: #555; height: 38px; display: flex; align-items: center;">
                    <i class="fas fa-home"></i> / Dashboard / <span style="color: #888;">Analysis</span>
                </div>
                ''', unsafe_allow_html=True)
            with bc_col2:
                # Prepare the clean text report
                report_text = f"""LEXASSIST AI - LEGAL ANALYSIS REPORT
=======================================
Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
Document: {res.get("filename", "unknown_contract.pdf")}
Risk Score: {res['risk_analysis']['risk_score']}%
Risk Level: {res['risk_analysis']['risk_level']}

FINAL ANALYSIS SUMMARY:
-----------------------
{res["summary"]}

-----------------------
Generated by LexAssist AI - Modern Legal Document Analysis
"""
                st.download_button(
                    label="⬇️ Download Report",
                    data=report_text,
                    file_name=f"LexAssist_Report_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            st.markdown('<br>', unsafe_allow_html=True)

            col_left, col_center, col_right = st.columns([1, 2, 1.2])

            with col_left:
                st.markdown(f'''
                <div class="glass-card stagger-1" style="height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem;">
                    <div class="risk-gauge-container">
                        <svg class="gauge-svg" viewBox="0 0 100 65">
                            <defs>
                                <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" style="stop-color:#00f2ff;stop-opacity:1" />
                                    <stop offset="100%" style="stop-color:#ff00ff;stop-opacity:1" />
                                </linearGradient>
                            </defs>
                            <!-- Semi-circle path: center 50, radius 40 -->
                            <path class="gauge-bg" d="M 10 50 A 40 40 0 0 1 90 50" />
                            <path class="gauge-fill" d="M 10 50 A 40 40 0 0 1 90 50" 
                                  style="stroke-dasharray: 126; stroke-dashoffset: {126 - (float(risk_score)/100 * 126)};" />
                        </svg>
                        <div class="risk-value">{risk_score}%</div>
                        <div class="risk-label">RISK LEVEL</div>
                    </div>
                    <div style="margin-top: 25px; text-align: center;">
                        <span style="padding: 8px 20px; border-radius: 30px; background: rgba(0, 242, 255, 0.1); border: 1px solid rgba(0, 242, 255, 0.3); color: var(--accent-cyan); font-weight: 700; font-size: 0.85rem; letter-spacing: 1px;">
                            OVERALL ASSESSMENT
                        </span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                # Risk Indicators Section
                if res['risk_analysis']['detected_clauses']:
                    st.markdown('<div style="text-align: center; margin-top: 1.5rem;"><div style="font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-weight: 700;">Critical Indicators</div>', unsafe_allow_html=True)
                    risk_chips_html = '<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 5px;">'
                    for clause in res['risk_analysis']['detected_clauses']:
                        risk_chips_html += f'<div class="risk-indicator-chip"><i class="fas fa-exclamation-triangle"></i> {clause}</div>'
                    risk_chips_html += '</div></div>'
                    st.markdown(risk_chips_html, unsafe_allow_html=True)

                st.markdown('<br>', unsafe_allow_html=True)
                if st.button("Analyze Contract", use_container_width=True, type="primary"):
                    st.rerun()

            with col_center:
                # Mockup Style Metric Bar
                st.markdown(f'''
<div class="metric-bar stagger-2">
    <div class="metric-card">
        <div class="metric-icon" style="background: rgba(0, 242, 255, 0.1); color: var(--accent-cyan);"><i class="fas fa-bolt"></i></div>
        <div class="metric-info"><div class="metric-value">73</div><div class="metric-label">Efficiency</div><div class="metric-sublabel">Score rank</div></div>
    </div>
    <div class="metric-card">
        <div class="metric-icon" style="background: rgba(255, 0, 255, 0.1); color: var(--accent-magenta);"><i class="fas fa-shield-virus"></i></div>
        <div class="metric-info"><div class="metric-value">1</div><div class="metric-label">Critical Risk</div><div class="metric-sublabel">High priority</div></div>
    </div>
    <div class="metric-card">
        <div class="metric-icon" style="background: rgba(0, 255, 136, 0.1); color: #00ff88;"><i class="fas fa-check-double"></i></div>
        <div class="metric-info"><div class="metric-value">4</div><div class="metric-label">Secure</div><div class="metric-sublabel">Safe clauses</div></div>
    </div>
    <div class="metric-card">
        <div class="metric-icon" style="background: rgba(255, 255, 255, 0.05); color: #fff;"><i class="fas fa-layer-group"></i></div>
        <div class="metric-info"><div class="metric-value">6</div><div class="metric-label">Coverage</div><div class="metric-sublabel">Total clauses</div></div>
    </div>
</div>
''', unsafe_allow_html=True)

                # Compare with Law Section
                st.markdown('<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;"><h3 style="margin: 0; font-size: 1.1rem; color: #fff; display: flex; align-items: center; gap: 10px;"><i class="fas fa-balance-scale" style="color: var(--accent-cyan);"></i> Statutory Comparison</h3></div>', unsafe_allow_html=True)
                
                if 'show_compare' not in st.session_state:
                    st.session_state.show_compare = False

                if st.button("Compare with Law", type="secondary", use_container_width=True):
                    st.session_state.show_compare = not st.session_state.show_compare
                    st.rerun()

                if st.session_state.show_compare:
                    stat_html = '<div class="stagger-3">'
                    for item in res.get('statutory_comparison', []):
                        stat_html += f'''
                        <div class="statutory-card">
                            <div class="statutory-header">
                                <div class="statutory-concept">{item['concept']}</div>
                                <div class="statutory-section-tag">{item['section']}</div>
                            </div>
                            <div class="statutory-provision">"{item['legal_provision']}"</div>
                            <div class="statutory-note"><i class="fas fa-info-circle"></i> {item['compliance_note']}</div>
                        </div>'''
                    stat_html += '</div>'
                    st.markdown(stat_html, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Clause Breakdown Card - Standardized Rendering
                clause_card_html = f'''<div class="glass-card stagger-3" style="padding: 1.5rem;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">Clause Breakdown</h3>
    <span style="color: var(--accent-cyan); font-size: 0.75rem; opacity: 0.8;">Verification Status <i class="fas fa-check-circle"></i></span>
</div>
<table class="breakdown-table">
    <tr><th>Clause / Provision</th><th>Safety Index</th><th>Status</th></tr>'''
                
                for ent in res['entities']:
                    b_color = "var(--accent-orange)" if "Compliance" in ent['type'] else ("var(--accent-green)" if "Financial" in ent['type'] else "var(--accent-red)")
                    b_bg = b_color + "1a"
                    s_label = "Reported" if "Compliance" in ent['type'] else ("Verified" if "Financial" in ent['type'] else "Flagged")
                    
                    clause_card_html += f'''
<tr>
    <td>
        <div class="clause-row">
            <div class="clause-icon"><i class="fas fa-file-signature"></i></div>
            <div><div class="clause-name">{ent['text']}</div><div class="clause-type">{ent['type']}</div></div>
        </div>
    </td>
    <td><span class="risk-badge-mini" style="background: {b_bg}; color: {b_color}; border: 1px solid {b_color}33;"><i class="fas fa-circle" style="font-size: 0.35rem;"></i> {ent['type']}</span></td>
    <td><span class="status-badge-mini">{s_label}</span></td>
</tr>'''
                
                clause_card_html += '</table></div>'
                st.markdown(clause_card_html, unsafe_allow_html=True)

            with col_right:
                # Key Points Summary - Unified Markdown Call
                summary_html = f'''<div class="glass-card stagger-3" style="height: 100%; display: flex; flex-direction: column;">
<div class="key-points-title">Key Points Summary</div>
<div class="high-risk-alert">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 28px; height: 28px; background: rgba(255,75,75,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--accent-red);"><i class="fas fa-redo" style="font-size: 0.7rem;"></i></div>
        <span style="font-size: 0.85rem; font-weight: 600;">Non-Compete</span>
    </div>
    <span style="color: var(--accent-red); font-weight: 800; font-size: 0.75rem;">High</span>
</div>
<div style="font-size: 0.95rem; color: #ccc; line-height: 1.7; margin-bottom: 2rem; overflow-wrap: break-word; word-break: break-word; font-style: italic;">
    {res["summary"]}
</div>
<div class="suggestion-panel" style="margin-top: auto;">
    <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;"><i class="far fa-lightbulb" style="color: var(--accent-green);"></i> Suggestion</div>
    <div style="font-size: 0.8rem; color: #aaa;">Review the liability clause 4.2; it contradicts section 1.1 regarding damage caps.</div>
</div>
<br>
'''
                st.markdown(summary_html, unsafe_allow_html=True)
                
                if st.button("Reset Analysis", use_container_width=True):
                    st.session_state.pop('analysis_done', None)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "History":
        st.markdown('<h1 class="hero-title">Analysis History</h1>', unsafe_allow_html=True)
        if not st.session_state.history:
            st.markdown('<div class="glass-card"><p>No previous history found.</p></div>', unsafe_allow_html=True)
        else:
            for i, entry in enumerate(st.session_state.history):
                st.markdown(f'''
                <div class="glass-card" style="margin-bottom: 1rem; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: #fff;">{entry['filename']}</h3>
                        <p style="margin: 5px 0; color: #888; font-size: 0.9rem;">{entry['timestamp']}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2rem; font-weight: 700; color: #00f2ff;">{entry['risk_score']}% Risk</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"View Report #{i}", key=f"view_{i}"):
                    st.session_state.result = entry['result']
                    st.session_state.analysis_done = True
                    st.session_state.page = "Dashboard"
                    st.rerun()

    elif st.session_state.page == "Profile":
        # Removed the big Hero Title to match "Upper Side" request
        
        # Profile View - Full width Container for better "Upper Side" presence
        with st.container(border=True):
            p_ext_col1, p_ext_col2 = st.columns([2, 1])
            with p_ext_col1:
                st.subheader("👤 Profile Information")
                pi_col_left, pi_col_right = st.columns([0.8, 2])
                with pi_col_left:
                    avatar_p = r"C:\Users\arpit\.gemini\antigravity\brain\0ce79af3-ea2c-4227-a27d-7786c2b6cc41\user_profile_avatar_1773247479711.png"
                    if os.path.exists(avatar_p):
                        st.image(avatar_p, use_container_width=True)
                    else:
                        st.markdown('<div style="width: 100px; height: 100px; border-radius: 12px; background: #333; display: flex; align-items: center; justify-content: center; font-size: 2rem;">👤</div>', unsafe_allow_html=True)
                    
                    st.markdown('<br>', unsafe_allow_html=True)
                    st.button("📷 Change Avatar", use_container_width=True, key="p_change_avatar")
                    st.markdown('<div class="btn-remove">', unsafe_allow_html=True)
                    st.button("🗑️ Remove", use_container_width=True, key="p_remove_avatar")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with pi_col_right:
                    new_name = st.text_input("Full Name", value=st.session_state.user_name)
                    new_email = st.text_input("Email Address", value=st.session_state.user_email)
                    st.selectbox("Organization", ["LegalTech Labs", "Lex Partners", "Individual"], index=0)
                    st.selectbox("Designation", ["Lawyer", "Para-legal", "Researcher", "Student"], index=0)
                    st.markdown('<br>', unsafe_allow_html=True)
                    act_col1, act_col2 = st.columns(2)
                    if act_col1.button("💾 Save Changes", use_container_width=True, type="primary", key="p_save"):
                        st.session_state.user_name = new_name
                        st.session_state.user_email = new_email
                        st.success("Profile updated successfully!")
                        st.rerun()
                    act_col2.button("🔑 Change Password", use_container_width=True, key="p_pass")

            with p_ext_col2:
                st.markdown('<div style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">', unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown('<p class="danger-title">Danger Zone</p>', unsafe_allow_html=True)
                    st.markdown('<p style="font-size: 0.85rem; color: #888;">Permanently delete your account and all associated data.</p>', unsafe_allow_html=True)
                    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                    st.button("🗑️ Delete Account", use_container_width=True, key="p_delete")
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "Settings":
        st.markdown('<div style="margin-bottom: 2rem;"><h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">Settings</h1><p style="color: #888;">Configure your AI analysis and application preferences.</p></div>', unsafe_allow_html=True)
        
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            with st.container(border=True):
                st.subheader("AI Analysis & Processing")
                st.selectbox("Model Selection", ["Legal-BERT (Recommended)", "GPT-4 Legal", "Claude 3 Sonnet"], index=0)
                st.markdown('<p class="settings-label">Risk Detection Intensity:</p>', unsafe_allow_html=True)
                risk_lvl_cols = st.columns(3)
                risk_lvl_cols[0].button("Low", use_container_width=True, key="s_risk_low")
                risk_lvl_cols[1].button("Medium", use_container_width=True, type="primary", key="s_risk_med")
                risk_lvl_cols[2].button("High", use_container_width=True, key="s_risk_high")
                st.markdown('<br>', unsafe_allow_html=True)
                st.checkbox("Enable OCR for scanned documents", value=True)
                st.checkbox("Auto-highlight high-risk clauses", value=True)
                st.checkbox("Extended liability detection", value=True)
                st.button("Update Preferences", key="s_save_ai", use_container_width=True, type="primary")

        with s_col2:
            with st.container(border=True):
                st.subheader("Global Settings")
                st.selectbox("Primary Compliance Region", ["Indian Contract Act", "GDPR (Europe)", "CCPA (California)"])
                st.checkbox("Email alerts for critical analysis", value=True)
                st.checkbox("Receive weekly report summary", value=True)
                st.button("Save System Settings", key="s_save_app", use_container_width=True)

render_footer()
