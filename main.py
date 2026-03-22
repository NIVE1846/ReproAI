"""
ReproAI - Doctor-in-the-Loop Intelligent Fertility Decision Assistant
Main Streamlit Application — Premium UI
"""
import streamlit as st
import sys, os, json, pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.predictor import FertilityPredictor
from utils.preprocessing import FertilityPreprocessor
from app.safety_rules import SafetyRulesEngine
from app.similarity_engine import SimilarityEngine
from app.digital_twin import DigitalTwinSimulator
from app.optimization_engine import OptimizationEngine
from app.explainability import ExplainabilityEngine
from app.ui import *

st.set_page_config(
    page_title="ReproAI — Fertility Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── GLOBAL BACKGROUND ── */
.stApp { background: #0a0e1a; }
section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #1e2d40; }

/* ── HERO HEADER ── */
.hero-wrap {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a1040 50%, #0d1b2a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 40px 30px 30px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(102,126,234,0.15) 0%, transparent 70%);
}
.hero-title {
    font-size: 3.2rem; font-weight: 800; letter-spacing: -1px;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0; line-height: 1.1;
}
.hero-sub {
    font-size: 1rem; color: #64748b; margin-top: 10px; font-weight: 400; letter-spacing: 0.5px;
}
.hero-badge {
    display: inline-block; margin-top: 14px;
    background: rgba(102,126,234,0.15); border: 1px solid rgba(102,126,234,0.4);
    color: #a78bfa; padding: 5px 16px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
}

/* ── SIDEBAR STYLING ── */
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] label { color: #94a3b8 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
section[data-testid="stSidebar"] .stSlider > div > div { background: #1e3a5f !important; }
section[data-testid="stSidebar"] input { background: #0d1b2a !important; color: #e2e8f0 !important; border: 1px solid #1e3a5f !important; border-radius: 8px !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div { background: #0d1b2a !important; color: #e2e8f0 !important; border: 1px solid #1e3a5f !important; }

.sidebar-section {
    background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 12px;
}
.sidebar-section-title {
    color: #60a5fa; font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117; border-radius: 14px; padding: 6px; gap: 4px;
    border: 1px solid #1e2d40;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px; color: #64748b;
    font-weight: 600; font-size: 0.85rem; padding: 10px 20px; border: none;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(13,27,42,0.8);
    border: 1px solid #1e3a5f;
    border-radius: 16px; padding: 24px;
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
    transition: border-color 0.3s;
}
.glass-card:hover { border-color: #3b82f6; }

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(135deg, #0d1b2a, #1a1040);
    border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 22px 20px; text-align: center;
    transition: all 0.3s; position: relative; overflow: hidden;
}
.stat-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #667eea, #764ba2);
}
.stat-card:hover { border-color: #667eea; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(102,126,234,0.2); }
.stat-label { color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
.stat-value { color: #e2e8f0; font-size: 2rem; font-weight: 800; margin: 6px 0 2px; line-height: 1; }
.stat-sub { color: #475569; font-size: 0.78rem; }

/* ── PROTOCOL CARDS ── */
.protocol-card {
    background: #0d1b2a; border: 2px solid #1e3a5f;
    border-radius: 16px; padding: 22px; margin-bottom: 12px;
    transition: all 0.3s;
}
.protocol-card.top { border-color: #667eea; background: linear-gradient(135deg, #0d1b2a, #1a1040); }
.protocol-card:hover { border-color: #3b82f6; }
.protocol-name { color: #e2e8f0; font-size: 1.1rem; font-weight: 700; }
.protocol-badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
}
.badge-top { background: rgba(102,126,234,0.2); color: #a78bfa; border: 1px solid rgba(102,126,234,0.4); }
.badge-alt { background: rgba(100,116,139,0.2); color: #94a3b8; border: 1px solid rgba(100,116,139,0.3); }

/* ── ALERT CARDS ── */
.alert-card {
    border-radius: 12px; padding: 16px 18px; margin: 8px 0;
    border-left: 4px solid; display: flex; align-items: flex-start; gap: 12px;
}
.alert-critical { background: rgba(220,38,38,0.1); border-color: #dc2626; }
.alert-warning  { background: rgba(245,158,11,0.1); border-color: #f59e0b; }
.alert-info     { background: rgba(59,130,246,0.1); border-color: #3b82f6; }
.alert-success  { background: rgba(16,185,129,0.1); border-color: #10b981; }
.alert-icon { font-size: 1.3rem; margin-top: 2px; }
.alert-title { color: #e2e8f0; font-weight: 700; font-size: 0.9rem; }
.alert-body  { color: #94a3b8; font-size: 0.82rem; margin-top: 3px; }

/* ── RISK BADGE ── */
.risk-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 16px; border-radius: 20px; font-weight: 700;
    font-size: 0.85rem; letter-spacing: 0.5px;
}
.risk-minimal { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.risk-low     { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.risk-moderate{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.risk-high    { background: rgba(220,38,38,0.15);  color: #f87171; border: 1px solid rgba(220,38,38,0.3); }

/* ── FACTOR CARDS ── */
.factor-card {
    background: #0d1b2a; border: 1px solid #1e3a5f;
    border-radius: 12px; padding: 16px; margin: 6px 0;
    display: flex; align-items: center; gap: 14px;
}
.factor-icon { font-size: 1.5rem; }
.factor-label { color: #94a3b8; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.factor-value { color: #e2e8f0; font-size: 1rem; font-weight: 700; }
.factor-impact { font-size: 0.78rem; margin-top: 2px; }
.impact-pos { color: #34d399; }
.impact-neg { color: #f87171; }
.impact-mix { color: #fbbf24; }

/* ── DECISION BUTTONS ── */
.stButton > button {
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: 0.9rem !important; padding: 14px 20px !important;
    transition: all 0.3s !important; border: none !important;
    letter-spacing: 0.3px !important;
}
button[kind="primary"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}
button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important; }

/* ── METRICS ── */
div[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight: 800 !important; }
div[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.8rem !important; }
div[data-testid="stMetricDelta"] svg { display: none; }

/* ── DIVIDER ── */
hr { border-color: #1e2d40 !important; margin: 24px 0 !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: #0d1b2a !important; border: 1px solid #1e3a5f !important;
    border-radius: 10px !important; color: #94a3b8 !important; font-weight: 600 !important;
}
.streamlit-expanderContent { background: #0a0e1a !important; border: 1px solid #1e2d40 !important; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }
iframe { border-radius: 12px !important; }

/* ── WELCOME SCREEN ── */
.feature-card {
    background: #0d1b2a; border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 28px 24px; text-align: center; transition: all 0.3s;
}
.feature-card:hover { border-color: #667eea; transform: translateY(-4px); box-shadow: 0 12px 32px rgba(102,126,234,0.15); }
.feature-icon { font-size: 2.5rem; margin-bottom: 12px; }
.feature-title { color: #e2e8f0; font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
.feature-desc { color: #64748b; font-size: 0.82rem; line-height: 1.6; }

/* ── NL EXPLANATION BOX ── */
.nl-box {
    background: linear-gradient(135deg, #0d1b2a, #1a1040);
    border: 1px solid #3b4f6b; border-radius: 14px; padding: 22px;
    color: #cbd5e1; font-size: 0.95rem; line-height: 1.8;
    font-style: italic;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    try:
        predictor = FertilityPredictor()
        if not predictor.models:
            return None
        return predictor
    except:
        return None

@st.cache_resource
def initialize_engines():
    try:
        return (SafetyRulesEngine(), SimilarityEngine(),
                DigitalTwinSimulator(), OptimizationEngine())
    except:
        return None, None, None, None

def log_decision(patient_data, recommendation, decision, notes=""):
    entry = {
        'timestamp': datetime.now().isoformat(),
        'patient_age': patient_data['age'],
        'patient_amh': patient_data['amh'],
        'recommended_protocol': recommendation['protocol'],
        'decision': decision,
        'notes': notes
    }
    log_file = 'decision_log.json'
    try:
        logs = json.load(open(log_file)) if os.path.exists(log_file) else []
        logs.append(entry)
        json.dump(logs, open(log_file, 'w'), indent=2)
    except:
        pass

def main():
    # ── HERO ──
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">🧬 ReproAI</div>
        <div class="hero-sub">Doctor-in-the-Loop · Intelligent Fertility Decision Assistant</div>
        <div class="hero-badge">⚕ Clinical AI · v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    predictor = load_models()
    if predictor is None:
        st.markdown("""
        <div class="alert-card alert-critical">
            <div class="alert-icon">🔴</div>
            <div><div class="alert-title">System Not Ready</div>
            <div class="alert-body">Run: python data/generate_dataset.py → python models/train_model.py</div></div>
        </div>""", unsafe_allow_html=True)
        return

    safety_engine, similarity_engine, digital_twin, optimization_engine = initialize_engines()
    if None in [safety_engine, similarity_engine, digital_twin, optimization_engine]:
        st.error("Failed to initialize engines")
        return

    explainability_engine = ExplainabilityEngine(predictor)
    preprocessor = FertilityPreprocessor()

    # ── SIDEBAR ──
    patient_data = render_patient_input_form()

    st.sidebar.markdown("---")
    analyze = st.sidebar.button("🔍 Analyze Patient", type="primary", use_container_width=True)
    if analyze:
        st.session_state['analyzed'] = True
        st.session_state['patient_data'] = patient_data

    # ── MAIN CONTENT ──
    if st.session_state.get('analyzed', False):
        patient_data = st.session_state['patient_data']

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊  Overview",
            "🔬  Protocols",
            "👥  Cohort",
            "🧠  Explain",
            "⚕️  Decision"
        ])

        # ── TAB 1: OVERVIEW ──
        with tab1:
            summary = preprocessor.get_patient_summary(patient_data)
            display_patient_summary(patient_data, summary)
            st.markdown("---")
            safety_results = safety_engine.evaluate_patient(patient_data)
            display_safety_alerts(safety_results)
            st.markdown("---")
            predictions = predictor.predict_with_confidence(patient_data)
            st.session_state['predictions'] = predictions
            display_predictions(predictions)

        # ── TAB 2: PROTOCOLS ──
        with tab2:
            simulations = digital_twin.simulate_all_protocols(patient_data)
            ranked_protocols = optimization_engine.rank_protocols(simulations)
            st.session_state['ranked_protocols'] = ranked_protocols
            recommendation = optimization_engine.get_recommendation(ranked_protocols)
            st.session_state['recommendation'] = recommendation

            display_recommended_protocol(recommendation)
            st.markdown("---")
            display_protocol_comparison(ranked_protocols)
            st.markdown("---")
            display_digital_twin_results(ranked_protocols)
            st.markdown("---")

            st.markdown("#### 🎯 Sensitivity Analysis")
            sensitivity = optimization_engine.sensitivity_analysis(simulations)
            cols = st.columns(len(sensitivity))
            for i, (scenario, protocol) in enumerate(sensitivity.items()):
                with cols[i]:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">{scenario}</div>
                        <div class="stat-value" style="font-size:1rem;margin-top:8px;">{protocol}</div>
                    </div>""", unsafe_allow_html=True)

        # ── TAB 3: COHORT ──
        with tab3:
            cohort_summary = similarity_engine.get_cohort_summary(patient_data)
            display_cohort_analysis(cohort_summary)
            st.markdown("---")

            st.markdown("#### 📈 Protocol Outcomes in Similar Patients")
            protocol_comparison = similarity_engine.compare_protocols_in_cohort(
                cohort_summary['similar_patients'])
            if not protocol_comparison.empty:
                st.dataframe(protocol_comparison, use_container_width=True, hide_index=True)
            else:
                st.info("Insufficient data for protocol comparison in this cohort")

            st.markdown("---")
            st.markdown("#### 📊 Patient Percentile Rankings")
            percentiles = similarity_engine.get_percentile_rank(patient_data)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class="stat-card">
                    <div class="stat-label">AMH Percentile</div>
                    <div class="stat-value">{percentiles['amh']:.0f}<span style="font-size:1rem">th</span></div>
                    <div class="stat-sub">vs all patients</div></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="stat-card">
                    <div class="stat-label">Age Percentile</div>
                    <div class="stat-value">{percentiles['age']:.0f}<span style="font-size:1rem">th</span></div>
                    <div class="stat-sub">younger than peers</div></div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="stat-card">
                    <div class="stat-label">AFC Percentile</div>
                    <div class="stat-value">{percentiles['afc']:.0f}<span style="font-size:1rem">th</span></div>
                    <div class="stat-sub">follicle count rank</div></div>""", unsafe_allow_html=True)

        # ── TAB 4: EXPLAIN ──
        with tab4:
            predictions = st.session_state.get('predictions', {})
            recommendation = st.session_state.get('recommendation', {})
            cohort_summary = similarity_engine.get_cohort_summary(patient_data)
            explanation_report = explainability_engine.generate_report(
                patient_data, predictions, recommendation, cohort_summary)

            display_explanation(explanation_report)
            st.markdown("---")

            st.markdown("#### 📊 Feature Importance")
            importance = predictor.get_feature_importance('pregnancy')
            if importance is not None:
                fig = create_feature_importance_chart(importance)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.markdown("#### 🎯 Optimization Score Breakdown")
            if recommendation and st.session_state.get('ranked_protocols'):
                top_protocol = st.session_state['ranked_protocols'][0]
                breakdown = optimization_engine.get_optimization_breakdown(top_protocol)
                display_optimization_breakdown(breakdown)

        # ── TAB 5: DECISION ──
        with tab5:
            recommendation = st.session_state.get('recommendation', {})
            if recommendation:
                display_decision_panel(recommendation, patient_data, log_decision)

    else:
        display_welcome_screen()


if __name__ == "__main__":
    main()
