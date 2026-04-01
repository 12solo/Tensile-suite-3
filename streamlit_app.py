import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
import os

# ==========================================
# 1. INITIALIZE SESSION STATE
# ==========================================
if 'tensile_df' not in st.session_state:
    st.session_state['tensile_df'] = pd.DataFrame()
if 'curve_dict' not in st.session_state:
    st.session_state['curve_dict'] = {}

# ==========================================
# 2. MECHANICAL DATA LOADER
# ==========================================
class TensileLoader:
    def process_files(self, uploaded_files, sample_name, width, thickness, gauge_len):
        summary_list = []
        curves = {}
        area = width * thickness  # mm^2

        for file in uploaded_files:
            try:
                # Load Data (Assumes Col 0: Extension mm, Col 1: Load N)
                df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
                df.columns = ['Extension_mm', 'Load_N']
                df = df.apply(pd.to_numeric, errors='coerce').dropna().reset_index(drop=True)

                # Calculations
                df['Strain_pct'] = (df['Extension_mm'] / gauge_len) * 100
                df['Stress_MPa'] = df['Load_N'] / area

                # Property Extraction
                uts = df['Stress_MPa'].max()
                elongation = df['Strain_pct'].max()
                
                # Young's Modulus (Simplified Linear Fit between 0.1% and 0.3% strain)
                linear_region = df[(df['Strain_pct'] > 0.1) & (df['Strain_pct'] < 0.3)]
                if len(linear_region) > 5:
                    slope, _ = np.polyfit(linear_region['Strain_pct']/100, linear_region['Stress_MPa'], 1)
                    modulus = slope / 1000 # Convert MPa to GPa
                else:
                    modulus = np.nan

                summary_list.append({
                    'Sample': sample_name,
                    'File': file.name,
                    'UTS_MPa': uts,
                    'Elongation_pct': elongation,
                    'Modulus_GPa': modulus
                })
                curves[file.name] = df
            except Exception as e:
                st.error(f"Error in {file.name}: {e}")
        return pd.DataFrame(summary_list), curves

# ==========================================
# 3. UI & SIDEBAR
# ==========================================
st.set_page_config(page_title="Mechanical Testing Lab", layout="wide")
st.title("🏗️ Scientific Tensile Analyzer")

with st.sidebar:
    st.header("1. Batch Upload")
    with st.form("tensile_form", clear_on_submit=True):
        s_id = st.text_input("Sample Batch ID", "Alloy-A")
        w = st.number_input("Width (mm)", value=10.0)
        t = st.number_input("Thickness (mm)", value=2.0)
        gl = st.number_input("Gauge Length (mm)", value=50.0)
        up_files = st.file_uploader("Upload Test Files (.csv, .xlsx)", accept_multiple_files=True)
        btn = st.form_submit_button("Analyze Samples")

    if btn and up_files:
        loader = TensileLoader()
        new_sum, new_curves = loader.process_files(up_files, s_id, w, t, gl)
        st.session_state['tensile_df'] = pd.concat([st.session_state['tensile_df'], new_sum], ignore_index=True)
        st.session_state['curve_dict'].update(new_curves)

    if st.button("Reset Lab"):
        st.session_state['tensile_df'] = pd.DataFrame()
        st.session_state['curve_dict'] = {}
        st.rerun()

# ==========================================
# 4. DASHBOARD
# ==========================================
df_m = st.session_state['tensile_df']
curves = st.session_state['curve_dict']

AXIS_STYLE = dict(
    mirror=True, ticks='outside', showline=True, linecolor='black', linewidth=2.5,
    title_font=dict(family="Times New Roman", size=22, color="black"),
    tickfont=dict(family="Times New Roman", size=18, color="black")
)

if not df_m.empty:
    tabs = st.tabs(["📊 Table", "📈 Stress-Strain Stack", "💾 Export"])
    
    with tabs[0]:
        st.subheader("Mechanical Properties Summary")
        st.dataframe(df_m, use_container_width=True)

    with tabs[1]:
        st.subheader("Representative Stress-Strain Curves")
        offset = st.slider("Horizontal Strain Offset (%)", 0, 50, 0)
        fig = go.Figure()

        unique_samples = sorted(df_m['Sample'].unique())
        for i, name in enumerate(unique_samples):
            sub = df_m[df_m['Sample'] == name]
            mean_uts = sub['UTS_MPa'].mean()
            std_uts = sub['UTS_MPa'].std()
            rep_file = sub.iloc[(sub['UTS_MPa'] - mean_uts).abs().argsort()[:1]]['File'].values[0]
            
            c_df = curves[rep_file]
            x_shift = i * offset
            
            # Plot Curve
            fig.add_trace(go.Scatter(
                x=c_df['Strain_pct'] + x_shift, y=c_df['Stress_MPa'],
                mode='lines', name=name, showlegend=False, line=dict(width=3)
            ))

            # Bold Times New Roman Legend
            label = f"<b>{name}</b><br><b>UTS: {mean_uts:.1f} ± {std_uts:.1f} MPa</b>"
            fig.add_annotation(
                x=(c_df['Strain_pct'] + x_shift).max(), y=c_df['Stress_MPa'].max(),
                text=label, showarrow=False, align="left", xanchor="left",
                font=dict(family="Times New Roman", size=16), yshift=15
            )

        fig.update_layout(
            template="simple_white", height=800,
            xaxis_title="<b>Engineering Strain (%)</b>",
            yaxis_title="<b>Engineering Stress (MPa)</b>",
            xaxis=AXIS_STYLE, yaxis=AXIS_STYLE
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.download_button("Download Summary CSV", df_m.to_csv(index=False).encode('utf-8'), "tensile_summary.csv")
else:
    st.info("👋 Upload tensile data to begin analysis.")
