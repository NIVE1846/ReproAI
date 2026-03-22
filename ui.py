"""
UI Components for ReproAI Streamlit Interface
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render_patient_input_form():
    """Render patient input form in sidebar"""
    st.sidebar.header("📋 Patient Information")
    
    patient_data = {}
    
    # Demographics
    st.sidebar.subheader("Demographics")
    patient_data['age'] = st.sidebar.slider("Age (years)", 25, 45, 32)
    patient_data['bmi'] = st.sidebar.number_input("BMI", 18.0, 45.0, 24.5, 0.1)
    
    # Hormones
    st.sidebar.subheader("Hormone Levels")
    patient_data['amh'] = st.sidebar.number_input("AMH (ng/mL)", 0.1, 30.0, 3.2, 0.1)
    patient_data['fsh'] = st.sidebar.number_input("FSH (mIU/mL)", 2.0, 20.0, 6.8, 0.1)
    patient_data['lh'] = st.sidebar.number_input("LH (mIU/mL)", 2.0, 25.0, 5.2, 0.1)
    patient_data['estradiol'] = st.sidebar.number_input("Estradiol (pg/mL)", 20.0, 100.0, 45.0, 1.0)
    
    # Ultrasound
    st.sidebar.subheader("Ultrasound Findings")
    patient_data['afc'] = st.sidebar.number_input("Antral Follicle Count", 2, 30, 12, 1)
    
    # Medical History
    st.sidebar.subheader("Medical History")
    patient_data['pcos'] = 1 if st.sidebar.checkbox("PCOS") else 0
    patient_data['endometriosis'] = 1 if st.sidebar.checkbox("Endometriosis") else 0
    patient_data['male_factor'] = 1 if st.sidebar.checkbox("Male Factor Infertility") else 0
    patient_data['previous_ivf_attempts'] = st.sidebar.selectbox(
        "Previous IVF Attempts", [0, 1, 2, 3, 4]
    )
    
    return patient_data

def display_safety_alerts(safety_results):
    """Display safety alerts and warnings"""
    st.subheader("🛡️ Clinical Safety Assessment")
    
    risk_level = safety_results['risk_level']
    
    # Risk level badge
    risk_colors = {
        'MINIMAL': 'green',
        'LOW': 'blue',
        'MODERATE': 'orange',
        'HIGH': 'red'
    }
    
    st.markdown(f"**Overall Risk Level:** :{risk_colors.get(risk_level, 'gray')}[{risk_level}]")
    
    # Alerts
    if safety_results['alerts']:
        st.error("⚠️ **Critical Alerts**")
        for alert in safety_results['alerts']:
            with st.expander(f"🔴 {alert['category']}: {alert['message']}", expanded=True):
                st.write(f"**Action Required:** {alert['action']}")
    
    # Warnings
    if safety_results['warnings']:
        st.warning("⚡ **Clinical Warnings**")
        for warning in safety_results['warnings']:
            with st.expander(f"🟡 {warning['category']}: {warning['message']}"):
                st.write(f"**Recommendation:** {warning['action']}")
    
    # Recommendations
    if safety_results['recommendations']:
        st.info("💡 **Clinical Recommendations**")
        for rec in safety_results['recommendations']:
            st.write(f"• {rec}")

def display_predictions(predictions):
    """Display ML predictions with advanced visualizations"""
    st.subheader("🤖 AI Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        preg_prob = predictions['pregnancy_prob']
        
        # Gauge chart for pregnancy probability
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=preg_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Pregnancy Success", 'font': {'size': 16}},
            delta={'reference': 45, 'suffix': "%"},
            gauge={
                'axis': {'range': [None, 100], 'ticksuffix': "%"},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': "#fee2e2"},
                    {'range': [30, 50], 'color': "#fef3c7"},
                    {'range': [50, 100], 'color': "#d1fae5"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        ohss_prob = predictions['ohss_prob']
        
        # Gauge for OHSS risk
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ohss_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "OHSS Risk", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [None, 50], 'ticksuffix': "%"},
                'bar': {'color': "#ef4444"},
                'steps': [
                    {'range': [0, 8], 'color': "#d1fae5"},
                    {'range': [8, 15], 'color': "#fef3c7"},
                    {'range': [15, 50], 'color': "#fee2e2"}],
                'threshold': {
                    'line': {'color': "darkred", 'width': 4},
                    'thickness': 0.75,
                    'value': 20}}))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        eggs = predictions['egg_yield']
        
        # Indicator for egg yield
        fig = go.Figure(go.Indicator(
            mode="number+delta",
            value=eggs,
            domain={'x': [0, 1], 'y': [0.3, 0.7]},
            title={'text': "Expected Eggs", 'font': {'size': 16}},
            delta={'reference': 10, 'relative': False},
            number={'font': {'size': 60, 'color': '#667eea'}}))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    # Confidence and risk summary
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confidence = predictions.get('confidence', 'Moderate')
        color = {'High': '🟢', 'Moderate': '🟡', 'Low': '🔴'}.get(confidence, '⚪')
        st.markdown(f"**Prediction Confidence:** {color} {confidence}")
    
    with col2:
        ohss_cat = predictions.get('ohss_category', 'Low Risk')
        st.markdown(f"**OHSS Category:** {ohss_cat}")
    
    with col3:
        if preg_prob > 0.5:
            st.markdown("**Prognosis:** 🟢 Favorable")
        elif preg_prob > 0.35:
            st.markdown("**Prognosis:** 🟡 Moderate")
        else:
            st.markdown("**Prognosis:** 🟠 Challenging")

def display_protocol_comparison(ranked_protocols):
    """Display protocol comparison with advanced visualizations"""
    st.subheader("🔬 Protocol Comparison")
    
    # Radar chart for protocol comparison
    protocols = [p['protocol'] for p in ranked_protocols]
    
    fig = go.Figure()
    
    for protocol in ranked_protocols:
        fig.add_trace(go.Scatterpolar(
            r=[
                protocol['success_probability'] * 100,
                (1 - protocol['ohss_risk']) * 100,
                protocol['estimated_eggs'] * 3.33,
                (1 - protocol['medication_dose'] / 450) * 100,
                (1 - protocol['cost_index'] / 3) * 100
            ],
            theta=['Success Rate', 'Safety', 'Egg Yield', 'Low Dose', 'Cost Effective'],
            fill='toself',
            name=protocol['protocol']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        height=400,
        title="Multi-Dimensional Protocol Comparison"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed comparison table
    comparison_data = []
    for protocol in ranked_protocols:
        comparison_data.append({
            'Rank': f"⭐" * protocol['rank'] if protocol['rank'] <= 3 else str(protocol['rank']),
            'Protocol': protocol['protocol'],
            'Success': f"{protocol['success_probability']:.1%}",
            'OHSS Risk': f"{protocol['ohss_risk']:.1%}",
            'Eggs': protocol['estimated_eggs'],
            'Dose': f"{protocol['medication_dose']} IU",
            'Cost': f"${protocol['cost_estimate']:,}",
            'Score': f"{protocol['optimization_score']:.3f}"
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Style the dataframe
    def highlight_top(row):
        if '⭐' in str(row['Rank']):
            return ['background-color: #d1fae5'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        df.style.apply(highlight_top, axis=1),
        use_container_width=True,
        hide_index=True
    )

def display_recommended_protocol(recommendation):
    """Display top recommended protocol"""
    st.subheader("✅ Recommended Protocol")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {recommendation['protocol']}")
        st.markdown(f"**Optimization Score:** {recommendation['score']:.3f}")
        
        st.markdown("**Rationale:**")
        for point in recommendation['rationale']:
            st.write(f"• {point}")
    
    with col2:
        st.markdown("**Key Metrics:**")
        for metric, value in recommendation['key_metrics'].items():
            st.metric(metric, value)

def display_cohort_analysis(cohort_summary):
    """Display similar patient cohort analysis with enhanced visuals"""
    st.subheader("👥 Similar Patient Cohort")
    
    stats = cohort_summary['statistics']
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Cohort Size", 
            stats['cohort_size'],
            help="Number of similar patients found"
        )
    
    with col2:
        success_rate = stats['success_rate']
        delta_color = "normal" if success_rate > 0.4 else "inverse"
        st.metric(
            "✅ Success Rate", 
            f"{success_rate:.1%}",
            delta=f"{(success_rate - 0.35):.1%} vs avg",
            delta_color=delta_color
        )
    
    with col3:
        st.metric(
            "🥚 Avg Eggs", 
            f"{stats['avg_eggs_retrieved']:.1f}",
            help="Average eggs retrieved in cohort"
        )
    
    with col4:
        ohss_rate = stats['ohss_rate']
        st.metric(
            "⚠️ OHSS Rate", 
            f"{ohss_rate:.1%}",
            delta=f"{(ohss_rate - 0.10):.1%} vs avg",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Cohort insights with visual indicators
    st.markdown("**💡 Cohort Insights:**")
    for insight in cohort_summary['interpretation']:
        if '✓' in insight or 'Favorable' in insight:
            st.success(insight)
        elif '⚠' in insight or 'High' in insight:
            st.warning(insight)
        else:
            st.info(insight)
    
    st.markdown("---")
    
    # Protocol distribution with pie chart
    if stats['protocol_distribution']:
        st.markdown("**📊 Protocol Distribution in Cohort:**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            protocol_df = pd.DataFrame(
                list(stats['protocol_distribution'].items()),
                columns=['Protocol', 'Count']
            )
            
            fig = px.pie(
                protocol_df, 
                values='Count', 
                names='Protocol',
                title='Protocols Used in Similar Patients',
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Protocol Counts:**")
            for protocol, count in stats['protocol_distribution'].items():
                percentage = (count / stats['cohort_size']) * 100
                st.markdown(f"**{protocol}:** {count} ({percentage:.0f}%)")
    
    # Age and AMH distribution
    st.markdown("---")
    st.markdown("**📈 Cohort Demographics:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Age Range:** {stats['age_range'][0]}-{stats['age_range'][1]} years")
        st.markdown(f"**Average Age:** {stats['avg_age']:.1f} years")
    
    with col2:
        st.markdown(f"**AMH Range:** {stats['amh_range'][0]:.2f}-{stats['amh_range'][1]:.2f} ng/mL")
        st.markdown(f"**Average AMH:** {stats['avg_amh']:.2f} ng/mL")

def display_explanation(explanation_report):
    """Display AI explanation"""
    st.subheader("🧠 AI Explanation")
    
    # Natural language explanation
    st.markdown("**Clinical Reasoning:**")
    st.info(explanation_report['natural_language_explanation'])
    
    # Key factors
    st.markdown("**Key Influencing Factors:**")
    
    for factor in explanation_report['key_factors']:
        impact_emoji = {
            'Positive': '✅',
            'Negative': '❌',
            'Neutral': '➖',
            'Mixed': '⚠️',
            'Caution': '⚠️'
        }
        
        emoji = impact_emoji.get(factor['impact'], '•')
        
        with st.expander(f"{emoji} {factor['factor']}: {factor['value']}"):
            st.write(f"**Impact:** {factor['impact']}")
            st.write(f"**Explanation:** {factor['explanation']}")

def display_digital_twin_results(simulations):
    """Display digital twin simulation results"""
    st.subheader("🔮 Digital Twin Simulation")
    
    st.markdown("Simulated patient response under different protocols:")
    
    for sim in simulations:
        with st.expander(f"{sim['protocol']} - Score: {sim.get('optimization_score', 0):.3f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {sim['description']}")
                st.write(f"**Expected Eggs:** {sim['estimated_eggs']} (range: {sim['egg_range'][0]}-{sim['egg_range'][1]})")
                st.write(f"**Success Probability:** {sim['success_probability']:.1%}")
                st.write(f"**OHSS Risk:** {sim['ohss_risk']:.1%} ({sim['ohss_category']})")
            
            with col2:
                st.write(f"**Medication Dose:** {sim['medication_dose']} IU")
                st.write(f"**Cost Estimate:** ${sim['cost_estimate']:,}")
                st.write(f"**Cost Index:** {sim['cost_index']}/3")
                st.write(f"**Suitability Score:** {sim['suitability_score']}/100")

def display_doctor_override_panel():
    """Display doctor override controls"""
    st.subheader("👨‍⚕️ Doctor Decision")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        accept = st.button("✅ Accept Recommendation", use_container_width=True, type="primary")
    
    with col2:
        modify = st.button("✏️ Modify Protocol", use_container_width=True)
    
    with col3:
        reject = st.button("❌ Reject Recommendation", use_container_width=True)
    
    decision = None
    if accept:
        decision = "ACCEPTED"
        st.success("✅ Recommendation accepted and logged")
    elif modify:
        decision = "MODIFIED"
        st.warning("✏️ Protocol modification requested")
        notes = st.text_area("Modification notes:")
    elif reject:
        decision = "REJECTED"
        st.error("❌ Recommendation rejected")
        reason = st.text_area("Rejection reason:")
    
    return decision

def create_feature_importance_chart(importance_df):
    """Create feature importance visualization"""
    if importance_df is None or importance_df.empty:
        return None
    
    fig = px.bar(
        importance_df.head(10),
        x='importance',
        y='feature',
        orientation='h',
        title='Top 10 Features Influencing Prediction',
        labels={'importance': 'Importance Score', 'feature': 'Feature'}
    )
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    return fig

def display_patient_summary(patient_data, summary):
    """Display patient clinical summary with visual cards"""
    st.subheader("📊 Patient Clinical Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        reserve = summary['ovarian_reserve']
        if 'Low' in reserve:
            color = "#fee2e2"
            icon = "🔴"
        elif 'High' in reserve or 'Good' in reserve:
            color = "#d1fae5"
            icon = "🟢"
        else:
            color = "#fef3c7"
            icon = "🟡"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 20px; border-radius: 12px; border-left: 4px solid #667eea;">
            <h4>{icon} Ovarian Reserve</h4>
            <p style="font-size: 1.2rem; font-weight: 600; margin: 0;">{reserve}</p>
            <p style="font-size: 0.9rem; color: #64748b; margin-top: 8px;">AMH: {patient_data['amh']:.2f} ng/mL | AFC: {patient_data['afc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        prognosis = summary['age_prognosis']
        if prognosis in ['Excellent', 'Good']:
            color = "#d1fae5"
            icon = "✅"
        elif prognosis == 'Fair':
            color = "#fef3c7"
            icon = "⚠️"
        else:
            color = "#fee2e2"
            icon = "❌"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 20px; border-radius: 12px; border-left: 4px solid #764ba2;">
            <h4>{icon} Age Prognosis</h4>
            <p style="font-size: 1.2rem; font-weight: 600; margin: 0;">{prognosis}</p>
            <p style="font-size: 0.9rem; color: #64748b; margin-top: 8px;">Age: {patient_data['age']} years</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pcos_status = summary['pcos_status']
        color = "#fee2e2" if pcos_status == 'Yes' else "#d1fae5"
        icon = "⚠️" if pcos_status == 'Yes' else "✅"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 20px; border-radius: 12px; border-left: 4px solid #f59e0b;">
            <h4>{icon} PCOS Status</h4>
            <p style="font-size: 1.2rem; font-weight: 600; margin: 0;">{pcos_status}</p>
            <p style="font-size: 0.9rem; color: #64748b; margin-top: 8px;">LH/FSH Ratio: {summary['lh_fsh_ratio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        lh_fsh_interp = summary['lh_fsh_interpretation']
        color = "#fee2e2" if 'Elevated' in lh_fsh_interp else "#d1fae5"
        icon = "🧪"
        
        st.markdown(f"""
        <div style="background: {color}; padding: 20px; border-radius: 12px; border-left: 4px solid #3b82f6;">
            <h4>{icon} Hormone Profile</h4>
            <p style="font-size: 1.2rem; font-weight: 600; margin: 0;">{lh_fsh_interp}</p>
            <p style="font-size: 0.9rem; color: #64748b; margin-top: 8px;">FSH: {patient_data['fsh']:.1f} | LH: {patient_data['lh']:.1f} mIU/mL</p>
        </div>
        """, unsafe_allow_html=True)


def display_welcome_screen():
    """Display welcome screen with feature cards"""
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 30px;">
        <p style="color:#64748b; font-size:1rem;">
            Enter patient data in the sidebar and click <strong style="color:#a78bfa;">Analyze Patient</strong> to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("🛡️", "Clinical Safety Rules", "Rule-based checks for OHSS risk, ovarian reserve, age factors, and BMI before any ML prediction."),
        ("🤖", "ML Predictions", "Random Forest models predict pregnancy success probability, OHSS risk, and expected egg yield."),
        ("🔮", "Digital Twin", "Simulate patient response across Mild, Antagonist, and Long Agonist protocols side-by-side."),
        ("👥", "Cohort Matching", "K-NN finds 50 most similar patients and shows their real outcomes and protocol distribution."),
        ("🎯", "Optimization Engine", "Multi-objective scoring ranks protocols by success, safety, dose, and cost simultaneously."),
        ("🧠", "AI Explainability", "Natural language explanations and feature importance charts make every recommendation transparent."),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#0d1b2a; border:1px solid #1e3a5f; border-radius:16px;
                        padding:28px 22px; text-align:center; margin-bottom:16px;">
                <div style="font-size:2.2rem; margin-bottom:10px;">{icon}</div>
                <div style="color:#e2e8f0; font-size:0.95rem; font-weight:700; margin-bottom:8px;">{title}</div>
                <div style="color:#64748b; font-size:0.8rem; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def display_optimization_breakdown(breakdown):
    """Display optimization score breakdown as a styled bar chart"""
    import plotly.graph_objects as go

    components = [k for k in breakdown if k != 'Total Score']
    values = [breakdown[k] for k in components]
    colors = ['#34d399' if v >= 0 else '#f87171' for v in values]

    fig = go.Figure(go.Bar(
        x=components,
        y=values,
        marker_color=colors,
        text=[f"{v:.3f}" for v in values],
        textposition='outside'
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,27,42,0.8)',
        font=dict(color='#94a3b8', family='Inter'),
        title=dict(text='Score Component Breakdown', font=dict(color='#e2e8f0', size=14)),
        xaxis=dict(gridcolor='#1e3a5f', tickfont=dict(color='#94a3b8')),
        yaxis=dict(gridcolor='#1e3a5f', tickfont=dict(color='#94a3b8')),
        height=320,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    total = breakdown['Total Score']
    color = '#34d399' if total > 0.2 else '#fbbf24' if total > 0.1 else '#f87171'
    st.markdown(f"""
    <div style="background:#0d1b2a; border:1px solid #1e3a5f; border-radius:12px;
                padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#94a3b8; font-weight:600;">Total Optimization Score</span>
        <span style="color:{color}; font-size:1.4rem; font-weight:800;">{total:.3f}</span>
    </div>
    """, unsafe_allow_html=True)


def display_decision_panel(recommendation, patient_data, log_decision_fn):
    """Display the doctor decision panel with styled buttons and logging"""
    import os, json

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1b2a,#1a1040); border:1px solid #3b4f6b;
                border-radius:16px; padding:24px; margin-bottom:20px;">
        <div style="color:#64748b; font-size:0.75rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:1px; margin-bottom:6px;">AI Recommendation</div>
        <div style="color:#a78bfa; font-size:1.6rem; font-weight:800;">{recommendation['protocol']}</div>
        <div style="color:#64748b; font-size:0.85rem; margin-top:4px;">
            Optimization Score: <strong style="color:#e2e8f0;">{recommendation['score']:.3f}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Success Probability", recommendation['key_metrics']['Success Probability'])
    with c2:
        st.metric("OHSS Risk", recommendation['key_metrics']['OHSS Risk'])
    with c3:
        st.metric("Expected Eggs", recommendation['key_metrics']['Expected Eggs'])

    st.markdown("---")
    st.markdown("#### Your Decision")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅  Accept Recommendation", use_container_width=True, type="primary"):
            log_decision_fn(patient_data, recommendation, "ACCEPTED")
            st.success("Recommendation accepted and logged.")
            st.balloons()

    with col2:
        if st.button("✏️  Modify Protocol", use_container_width=True):
            st.session_state['modify_mode'] = True
            st.session_state['reject_mode'] = False

    with col3:
        if st.button("❌  Reject Recommendation", use_container_width=True):
            st.session_state['reject_mode'] = True
            st.session_state['modify_mode'] = False

    if st.session_state.get('modify_mode', False):
        st.markdown("---")
        st.markdown("#### Modify Protocol")
        modified_protocol = st.selectbox("Select Alternative Protocol",
                                         ["Mild Stimulation", "Antagonist", "Long Agonist"])
        modification_notes = st.text_area("Modification Rationale:")
        if st.button("Save Modified Decision"):
            log_decision_fn(patient_data, recommendation, "MODIFIED",
                            f"Changed to {modified_protocol}: {modification_notes}")
            st.success("Modified decision logged.")
            st.session_state['modify_mode'] = False

    if st.session_state.get('reject_mode', False):
        st.markdown("---")
        st.markdown("#### Rejection Reason")
        rejection_reason = st.text_area("Please provide reason for rejection:")
        if st.button("Confirm Rejection"):
            log_decision_fn(patient_data, recommendation, "REJECTED", rejection_reason)
            st.error("Rejection logged.")
            st.session_state['reject_mode'] = False

    st.markdown("---")
    if st.checkbox("📋 View Decision Log"):
        log_file = 'decision_log.json'
        if os.path.exists(log_file):
            with open(log_file) as f:
                logs = json.load(f)
            st.markdown(f"**Total Decisions Logged:** {len(logs)}")
            for log in logs[-10:][::-1]:
                with st.expander(f"{log['timestamp']} — {log['decision']}"):
                    st.write(f"**Recommended:** {log['recommended_protocol']}")
                    st.write(f"**Patient Age:** {log['patient_age']} | **AMH:** {log['patient_amh']}")
                    if log.get('notes'):
                        st.write(f"**Notes:** {log['notes']}")
        else:
            st.info("No decisions logged yet.")
