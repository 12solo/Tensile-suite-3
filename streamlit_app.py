import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import requests
import re
import os
import base64

# ==========================================
# PAGE CONFIG — must be first Streamlit call
# ==========================================
st.set_page_config(
    page_title="Tensile Pro Suite | Solomon Scientific",
    page_icon="LOGO.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# GLOBAL CUSTOM CSS — Midnight Navy & Gold Theme
# ==========================================
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── CSS Variables ────────────────────────────── */
:root {
    /* Bold & Elegant Dark Mode Colors */
    --bg-main:    #0b1120; /* Deep Midnight Navy */
    --bg-panel:   #111827; /* Slightly lighter navy for cards/panels */
    --text-main:  #f8fafc; /* Crisp off-white for primary text */
    --text-muted: #94a3b8; /* Slate gray for secondary text */
    --gold:       #c9a84c; /* Signature Gold */
    --gold-dim:   #9c7a32;
    --border-color: rgba(201, 168, 76, 0.25); /* Subtle gold borders */
    
    --font-head:  'Playfair Display', Georgia, serif;
    --font-mono:  'IBM Plex Mono', 'Courier New', monospace;
    --font-body:  'IBM Plex Sans', 'Segoe UI', sans-serif;
}

/* ── Base & Body ──────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body);
    color: var(--text-main);
}
.stApp { background: var(--bg-main); }
.stApp::before { display: none; }

[data-testid="block-container"] {
    padding-top: 2rem !important; 
    padding-bottom: 2rem !important;
}

/* ── Sidebar ──────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border-color);
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: var(--text-main) !important;
    font-family: var(--font-body);
}
.material-symbols-rounded,
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded" !important;
    color: var(--gold) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--gold) !important;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] hr { border-color: var(--border-color); margin: 1rem 0; }

[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="number"],
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {
    background: var(--bg-main) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 4px !important;
    color: var(--text-main) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}

[data-testid="stFileUploadDropzone"] {
    background-color: var(--bg-main) !important;
    border: 2px dashed var(--gold-dim) !important;
    border-radius: 6px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--gold) !important;
    background-color: rgba(201, 168, 76, 0.05) !important;
}

/* ── Main Area Inputs ─────────────────────────── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 4px !important;
    color: var(--text-main) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}

/* ── Buttons ──────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: var(--bg-main) !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: var(--font-body) !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold), #e2c97e) !important;
    box-shadow: 0 4px 15px rgba(201,168,76,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #8b1a1a, #e05252) !important;
    color: white !important;
}

[data-testid="stDownloadButton"] > button {
    background: var(--bg-panel) !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold-dim) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(201, 168, 76, 0.1) !important;
}

/* ── Tabs & DataFrames ─────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border-color);
    gap: 0; padding: 0;
}
[data-testid="stTabs"] [role="tab"] {
    color: var(--text-muted) !important;
    font-family: var(--font-body) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.2rem !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
    background: var(--bg-main) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    background: var(--bg-panel) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg-main) !important;
    color: var(--gold) !important;
    border-bottom: 1px solid var(--border-color) !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-main) !important;
}

[data-testid="stExpander"] {
    border: 1px solid var(--border-color) !important;
    border-radius: 4px !important;
    background: var(--bg-panel) !important;
}
[data-testid="stExpander"] summary {
    color: var(--gold) !important;
    font-weight: 700 !important;
}

/* ── Alerts ───────────────────────────────────── */
[data-testid="stAlert"] { 
    background: rgba(61,184,122,0.1) !important; 
    color: var(--text-main) !important; 
    border: 1px solid rgba(61,184,122,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER COMPONENTS
# ==========================================
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def render_header():
    logo_path = "LOGO.png"
    img_b64 = get_base64_of_bin_file(logo_path)
    if img_b64:
        icon_html = f'<img src="data:image/png;base64,{img_b64}" style="width: 54px; height: 54px; border-radius: 8px; background: white; object-fit: contain;">'
    else:
        icon_html = '<div style="width: 54px; height: 54px; background: #c9a84c; border-radius: 8px; display: flex; align-items: center; justify-content: center;">🔬</div>'

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #111827 0%, #1a2540 100%); padding: 1.5rem; border-radius: 8px; border: 1px solid rgba(201,168,76,0.3); display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2rem;">
        {icon_html}
        <div>
            <div style="font-family: 'Playfair Display'; font-size: 1.75rem; font-weight: 700; color: #f0f4fb;">Tensile Extrapolation Suite</div>
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 2px;">Solomon Scientific · © 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, unit=""):
    return f"""
    <div style="background: #111827; border: 1px solid rgba(201,168,76,0.25); border-radius: 6px; padding: 1rem; border-top: 3px solid #c9a84c;">
        <div style="font-size:0.68rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">{label}</div>
        <div style="font-size:1.35rem; color:#f8fafc; font-weight:700;">{value}<span style="font-size:0.7rem; color:#94a3b8; margin-left:4px;">{unit}</span></div>
    </div>
    """

def render_sidebar_brand():
    logo_path = "LOGO.png"
    img_b64 = get_base64_of_bin_file(logo_path)
    if img_b64:
        icon_html = f'<img src="data:image/png;base64,{img_b64}" style="width: 52px; height: 52px; margin: 0 auto 0.75rem auto; border-radius: 10px; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.5); object-fit: contain; background: white;">'
    else:
        icon_html = '<div style="width:52px; height:52px; margin:0 auto 0.75rem auto; background:#c9a84c; border-radius:10px; display:flex;align-items:center;justify-content:center; font-size:1.5rem;">🔬</div>'

    st.markdown(f"""
    <div style="padding: 1.25rem 0 0.5rem 0; text-align:center;">
        {icon_html}
        <div style="font-size:0.65rem; color:#c9a84c; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:4px; font-weight:700;">Solomon Scientific</div>
        <div style="font-family: 'Playfair Display'; font-size:1.1rem; font-weight:700; color:#f8fafc;">Extrapolation <span style="color:#c9a84c;">Pro</span></div>
        <div style="margin-top:0.75rem; padding-top:0.75rem; border-top:1px solid rgba(201,168,76,0.25); font-size:0.68rem; color:#94a3b8;">
            Advanced Modeling Tools<br>
            <a href='mailto:your.solomon.duf@gmail.com' style='color:#c9a84c;text-decoration:none;'>✉ Contact Developer</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PROCESSING ENGINE
# ==========================================
def robust_load(file):
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            raw_bytes = file.getvalue().decode("utf-8", errors="ignore")
            sep = '\t' if '\t' in raw_bytes else (',' if ',' in raw_bytes else r'\s+')
            df = pd.read_csv(io.StringIO(raw_bytes), sep=sep, engine='python', on_bad_lines='skip')
        df.columns = [str(c).strip() for c in df.columns]
        return df.apply(pd.to_numeric, errors='coerce').dropna(subset=df.columns[:2])
    except: return None

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    render_sidebar_brand()
    
    st.markdown("### 🔗 Related Tools")
    st.link_button(
        "Batch Master App", 
        "https://solomon--tensile-test-batch-analysis-33vrgvcpcctqwxnuez5pci.streamlit.app/",
        use_container_width=True
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📂 Project Metadata")
    project_name = st.text_input("Project Name", "PBAT/PLA")
    batch_id = st.text_input("Batch ID", "Batch-001")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Extrapolation Parameters")
    target_def = st.number_input("Target Final Deformation (mm)", value=395.54, step=10.0)
    area = st.number_input("Cross-sectional Area (mm²)", value=16.0, step=0.5)
    gauge_length = st.number_input("Initial Gauge Length (mm)", value=25.0, step=1.0)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📏 Modulus & Yield Setup")
    ym_start = st.number_input("Modulus Start (%)", value=0.2, step=0.1)
    ym_end = st.number_input("Modulus End (%)", value=1.2, step=0.1)
    calc_yield = st.checkbox("Calculate Yield Point", value=True)
    yield_search_max = st.number_input("Max Strain to Search (%)", value=35.0, step=5.0)
    ref_points = st.number_input("Extrapolation Ref Points", value=50, step=5)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🔍 Zoom Graph Position")
    inset_x = st.slider("Inset X Position", 0.0, 0.8, 0.55, 0.05)
    inset_y = st.slider("Inset Y Position", 0.0, 0.8, 0.05, 0.05)
    inset_w = st.slider("Width", 0.2, 0.6, 0.40, 0.05)
    inset_h = st.slider("Height", 0.2, 0.6, 0.40, 0.05)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Advanced Settings")
    apply_noise = st.checkbox("Apply Plateau Noise", value=True)
    noise_std = st.number_input("Noise Std Dev (N)", value=0.1, step=0.05)


# ==========================================
# MAIN DASHBOARD
# ==========================================
render_header()

st.markdown("""
<div style="background:rgba(58,123,213,0.08); border-left:4px solid #3a7bd5; border-radius:4px; padding:0.75rem 1rem; margin-bottom: 2rem; font-size:0.85rem; color:#f8fafc; font-weight:500;">
    <span style="color:#3a7bd5; font-weight:bold; margin-right:0.5rem;">ℹ</span>
    Optimized for biodegradable polymers (PBAT/PLA). The framework automatically detects the maximum stress point, strictly truncates the failure drop-off, and extrapolates the drawing plateau to characterize mechanical performance.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Tensile Data (Excel, CSV, or TXT)", type=['csv', 'xlsx', 'xls', 'txt'])

if uploaded_file is not None:
    df = robust_load(uploaded_file)
    if df is not None:
        cols = df.columns.tolist()
        c1, c2 = st.columns(2)
        with c1:
            force_col = st.selectbox("Force/Load Column", cols, index=0)
        with c2:
            def_col = st.selectbox("Deformation/Extension Column", cols, index=1 if len(cols)>1 else 0)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚙️ Calculate & Generate Analysis", use_container_width=True):
            # --- PRE-PROCESSING ---
            df[force_col] = pd.to_numeric(df[force_col], errors='coerce')
            df[def_col] = pd.to_numeric(df[def_col], errors='coerce')
            df = df.dropna(subset=[force_col, def_col])

            # --- AUTO-DETECTION OF PEAK STRESS & TRUNCATION ---
            idx_max = df[force_col].idxmax()
            
            # STRICLY TRUNCATE DATA AT THE PEAK STRESS POINT to eliminate the break line
            df_trimmed = df.loc[:idx_max].copy()

            # --- EXTRAPOLATION LOGIC ---
            last_n = df_trimmed.tail(int(ref_points))
            slope, intercept = np.polyfit(last_n[def_col].values, last_n[force_col].values, 1)
            
            D_stop = df_trimmed[def_col].iloc[-1] 
            L_stop = df_trimmed[force_col].iloc[-1]
            avg_step = np.mean(np.diff(df_trimmed[def_col].tail(10).values))
            
            D_new = np.arange(D_stop + avg_step, target_def + avg_step, avg_step)
            if len(D_new) > 0 and D_new[-1] > target_def: D_new[-1] = target_def
            
            np.random.seed(42)
            noise = np.random.normal(0, noise_std, len(D_new)) if apply_noise else 0
            L_new = L_stop + slope * (D_new - D_stop) + noise
            
            # Combine Data
            df_orig = pd.DataFrame({'Force (N)': df_trimmed[force_col], 'Deformation (mm)': df_trimmed[def_col], 'Type': 'Original'})
            df_ext = pd.DataFrame({'Force (N)': L_new, 'Deformation (mm)': D_new, 'Type': 'Extrapolated'})
            df_combined = pd.concat([df_orig, df_ext], ignore_index=True)
            
            df_combined['Stress (MPa)'] = df_combined['Force (N)'] / area
            df_combined['Strain (%)'] = (df_combined['Deformation (mm)'] / gauge_length) * 100
            
            # --- CONSTITUTIVE CALCULATIONS WITH SAFETY CHECK ---
            mask_ym = (df_combined['Strain (%)'] >= ym_start) & (df_combined['Strain (%)'] <= ym_end)
            
            if mask_ym.any():
                E, inter_ym = np.polyfit(df_combined.loc[mask_ym, 'Deformation (mm)']/gauge_length, df_combined.loc[mask_ym, 'Stress (MPa)'], 1)
                
                y_mask = df_combined['Strain (%)'] <= yield_search_max
                y_idx = df_combined.loc[y_mask, 'Stress (MPa)'].idxmax()
                y_stress, y_strain = df_combined.loc[y_idx, 'Stress (MPa)'], df_combined.loc[y_idx, 'Strain (%)']

                # Numpy 2.0 Trapz update
                try: 
                    work_j = np.trapezoid(df_combined['Force (N)'], df_combined['Deformation (mm)']) / 1000.0
                except AttributeError: 
                    work_j = np.trapz(df_combined['Force (N)'], df_combined['Deformation (mm)']) / 1000.0

                # --- DASHBOARD METRICS ---
                st.markdown("<hr>", unsafe_allow_html=True)
                
                m1, m2, m3, m4, m5, m6 = st.columns(6)
                m1.markdown(metric_card("Modulus (E)", f"{E:.1f}", "MPa"), unsafe_allow_html=True)
                m2.markdown(metric_card("Yield Stress", f"{y_stress:.2f}", "MPa"), unsafe_allow_html=True)
                m3.markdown(metric_card("Yield Strain", f"{y_strain:.2f}", "%"), unsafe_allow_html=True)
                m4.markdown(metric_card("Stress @ Peak", f"{df_combined['Stress (MPa)'].iloc[idx_max]:.2f}", "MPa"), unsafe_allow_html=True)
                m5.markdown(metric_card("Strain @ Break", f"{df_combined['Strain (%)'].iloc[-1]:.1f}", "%"), unsafe_allow_html=True)
                m6.markdown(metric_card("Work Done", f"{work_j:.2f}", "J"), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # --- MATPLOTLIB STYLING (JOURNAL QUALITY) ---
                plt.rcParams.update({
                    'font.family': 'sans-serif',
                    'font.sans-serif': ['Arial'],
                    'axes.linewidth': 2,
                    'axes.edgecolor': 'black',
                    'xtick.major.width': 2,
                    'ytick.major.width': 2,
                    'xtick.direction': 'in',
                    'ytick.direction': 'in',
                    'axes.labelweight': 'bold',
                    'axes.titleweight': 'bold'
                })

                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Bold & Elegant Colors
                COLOR_ORIG = '#0b1120' # Deep Navy/Black
                COLOR_EXT  = '#c9a84c' # Rich Gold
                COLOR_FIT  = '#3a7bd5' # Accent Blue
                COLOR_PEAK = '#e05252' # Bright Red
                COLOR_YLD  = '#3db87a' # Bright Green
                
                # 1. Original Data
                ax.plot(df_combined.loc[df_combined['Type']=='Original', 'Strain (%)'], 
                        df_combined.loc[df_combined['Type']=='Original', 'Stress (MPa)'], 
                        label='Original (to Peak)', color=COLOR_ORIG, lw=3)
                
                # 2. Extrapolated Data
                ax.plot(df_combined.loc[df_combined['Type']=='Extrapolated', 'Strain (%)'], 
                        df_combined.loc[df_combined['Type']=='Extrapolated', 'Stress (MPa)'], 
                        label='Extrapolated Plateau', color=COLOR_EXT, ls='--', alpha=0.9, lw=2.5)
                
                # 3. Elastic Fit
                xfv = np.linspace(0, ym_end/100 * 1.5, 50)
                yfv = E * xfv + inter_ym
                ax.plot(xfv * 100, yfv, color=COLOR_FIT, ls=':', label='Elastic Fit', lw=2.5)
                
                # 4. Max Stress
                peak_strain = df_combined['Strain (%)'].iloc[idx_max]
                peak_stress = df_combined['Stress (MPa)'].iloc[idx_max]
                ax.plot(peak_strain, peak_stress, '*', color=COLOR_PEAK, markersize=14, label='Max Stress', zorder=5)
                ax.axvline(x=peak_strain, color='black', linestyle='--', alpha=0.3, lw=1.5)
                
                # 5. Yield Point
                if calc_yield: 
                    ax.plot(y_strain, y_stress, 'o', color=COLOR_YLD, markersize=8, label='Yield Point', markeredgecolor='black', zorder=6)
                
                ax.set_xlabel('Strain (%)', fontsize=14)
                ax.set_ylabel('Stress (MPa)', fontsize=14)
                
                # Clean Legend
                ax.legend(loc='lower right', frameon=True, edgecolor='black', fancybox=False, fontsize=12)
                
                # Inset Zoom
                axins = ax.inset_axes([inset_x, inset_y, inset_w, inset_h])
                axins.plot(df_combined['Strain (%)'].iloc[:len(df_orig)], df_combined['Stress (MPa)'].iloc[:len(df_orig)], color=COLOR_ORIG, lw=2)
                axins.plot(xfv * 100, yfv, color=COLOR_FIT, ls=':', lw=2)
                if calc_yield:
                    axins.plot(y_strain, y_stress, 'o', color=COLOR_YLD, markersize=6, markeredgecolor='black')
                    
                z_lim = max(ym_end + 1.5, y_strain + 1.5 if calc_yield else 0)
                axins.set_xlim(0, z_lim)
                axins.set_ylim(0, df_combined.loc[df_combined['Strain (%)'] <= z_lim, 'Stress (MPa)'].max() * 1.3)
                
                # Inset borders
                for spine in axins.spines.values():
                    spine.set_linewidth(1.5)
                axins.tick_params(width=1.5, direction='in')
                
                ax.indicate_inset_zoom(axins, edgecolor="black", linewidth=1.5)
                
                st.pyplot(fig)

                # --- EXPORT ---
                st.markdown("<hr>", unsafe_allow_html=True)
                
                summary_data = {
                    "Property": ["Project", "Batch", "Modulus (E)", "Yield Stress", "Yield Strain", "Peak Stress", "Strain @ Break", "Work Done"],
                    "Value": [project_name, batch_id, f"{E:.2f}", f"{y_stress:.2f}", f"{y_strain:.2f}", f"{peak_stress:.2f}", f"{df_combined['Strain (%)'].iloc[-1]:.2f}", f"{work_j:.4f}"],
                    "Unit": ["-", "-", "MPa", "MPa", "%", "MPa", "%", "J"]
                }
                df_summary = pd.DataFrame(summary_data)

                img_data = io.BytesIO()
                fig.savefig(img_data, format='png', dpi=300, bbox_inches='tight') # High-res saving
                img_data.seek(0)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_combined.to_excel(writer, index=False, sheet_name="Full Dataset")
                    worksheet1 = writer.sheets["Full Dataset"]
                    
                    # Auto-fit sheet 1
                    for i in range(df_combined.shape[1]):
                        col_name = str(df_combined.columns[i])
                        data_len = df_combined.iloc[:, i].fillna("").astype(str).str.len().max() if len(df_combined)>0 else 0
                        max_len = max(len(col_name), data_len) + 2
                        worksheet1.set_column(i, i, max_len)

                    df_summary.to_excel(writer, index=False, sheet_name="Summary Report", startrow=1, startcol=1)
                    worksheet2 = writer.sheets["Summary Report"]
                    
                    # Auto-fit sheet 2
                    for i in range(df_summary.shape[1]):
                        col_name = str(df_summary.columns[i])
                        data_len = df_summary.iloc[:, i].fillna("").astype(str).str.len().max() if len(df_summary)>0 else 0
                        max_len = max(len(col_name), data_len) + 2
                        worksheet2.set_column(i+1, i+1, max_len) 

                    worksheet2.insert_image('F2', 'plot.png', {'image_data': img_data, 'x_scale': 0.7, 'y_scale': 0.7})

                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        label=f"📥 Download Full Report (.xlsx)", 
                        data=output.getvalue(), 
                        file_name=f"{batch_id}_Extrapolation_Report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with c2:
                    st.download_button(
                        label=f"📸 Download High-Res Plot (.png)", 
                        data=img_data, 
                        file_name=f"{batch_id}_Plot.png",
                        mime="image/png",
                        use_container_width=True
                    )

            else:
                st.error(f"⚠️ **Range Error:** No data points found between {ym_start}% and {ym_end}% strain. Please check your Gauge Length or expand the Modulus Elongation range in the sidebar.")
