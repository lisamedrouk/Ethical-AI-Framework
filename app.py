import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Ethical AI Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assessments' not in st.session_state:
    st.session_state.assessments = []

# Sidebar navigation
st.sidebar.title("🤖 Ethical AI Framework")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "NIST Assessment", "ISO 42001 Assessment", "Reports", "Resources"]
)

# NIST AI RMF Categories
NIST_CATEGORIES = {
    "Govern": ["AI governance structure", "Risk management policies", "Stakeholder engagement"],
    "Map": ["Context identification", "Risk categorization", "Impact assessment"],
    "Measure": ["Performance metrics", "Bias testing", "Reliability measures"],
    "Manage": ["Risk mitigation", "Incident response", "Continuous monitoring"]
}

# ISO 42001 Controls
ISO_42001_CONTROLS = {
    "Planning": ["AI policy", "Objectives", "Risk assessment"],
    "Support": ["Resources", "Competence", "Documentation"],
    "Operation": ["Planning & control", "Impact assessment", "Data management"],
    "Performance": ["Monitoring", "Analysis", "Internal audit"],
    "Improvement": ["Nonconformity", "Corrective action", "Continual improvement"]
}

# Dashboard Page
if page == "Dashboard":
    st.markdown('<p class="main-header">🤖 Ethical AI Framework Dashboard</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", len(st.session_state.assessments))
    with col2:
        completed = sum(1 for a in st.session_state.assessments if a.get('status') == 'Completed')
        st.metric("Completed", completed)
    with col3:
        if st.session_state.assessments:
            avg_score = sum(a.get('score', 0) for a in st.session_state.assessments) / len(st.session_state.assessments)
            st.metric("Average Score", f"{avg_score:.1f}%")
        else:
            st.metric("Average Score", "N/A")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Quick Stats")
        if st.session_state.assessments:
            df = pd.DataFrame(st.session_state.assessments)
            st.dataframe(df[['name', 'framework', 'score', 'date']], use_container_width=True)
        else:
            st.info("No assessments yet. Start with NIST or ISO 42001 assessment!")
    
    with col2:
        st.subheader("🎯 Compliance Overview")
        st.info("**NIST AI RMF**: Risk Management Framework for AI systems")
        st.info("**ISO 42001**: AI Management System standard")
        st.success("Start your assessment from the sidebar!")

# NIST Assessment Page
elif page == "NIST Assessment":
    st.markdown('<p class="main-header">NIST AI Risk Management Framework</p>', unsafe_allow_html=True)
    
    st.info("📋 Assess your AI system across the four core NIST functions")
    
    # Rating guide
    with st.expander("📖 How to rate compliance (click to expand)"):
        st.markdown("""
        **Rating Scale Guide:**
        - **0-25%**: Minimal or no implementation - Critical gaps, no documented processes
        - **26-50%**: Partial implementation - Some processes in place, significant improvements needed
        - **51-75%**: Good implementation - Most requirements met, minor gaps remain
        - **76-100%**: Excellent implementation - Comprehensive processes, well-documented, regularly reviewed
        
        **Tips for accurate assessment:**
        - Be honest about current state, not aspirational goals
        - Consider both documentation AND actual practice
        - Lower scores identify improvement opportunities
        - Review criteria carefully before rating
        """)
    
    project_name = st.text_input("Project/AI System Name", placeholder="e.g., Customer Service Chatbot")
    assessor = st.text_input("Assessor Name", placeholder="Your name")
    
    st.markdown("---")
    st.subheader("Rate each category (0-100)")
    
    scores = {}
    
    # Govern
    st.markdown("### 📊 Govern")
    st.caption("**What to assess:** Do you have clear AI governance structure, documented policies, and stakeholder involvement?")
    with st.expander("View Govern criteria"):
        st.write("• AI governance structure - Clear roles and responsibilities")
        st.write("• Risk management policies - Documented AI risk policies and procedures")
        st.write("• Stakeholder engagement - Regular consultation with affected parties")
    scores["Govern"] = st.slider(
        "Govern Compliance Score",
        0, 100, 50,
        help="Rate governance maturity: policies, structure, accountability",
        key="nist_Govern"
    )
    st.markdown("")
    
    # Map
    st.markdown("### 📊 Map")
    st.caption("**What to assess:** Have you identified AI system context, categorized risks, and assessed potential impacts?")
    with st.expander("View Map criteria"):
        st.write("• Context identification - Understanding of AI system use cases and environment")
        st.write("• Risk categorization - Systematic classification of AI-related risks")
        st.write("• Impact assessment - Analysis of potential positive and negative impacts")
    scores["Map"] = st.slider(
        "Map Compliance Score",
        0, 100, 50,
        help="Rate risk identification: context understanding, categorization, impact analysis",
        key="nist_Map"
    )
    st.markdown("")
    
    # Measure
    st.markdown("### 📊 Measure")
    st.caption("**What to assess:** Do you have metrics for performance, bias testing procedures, and reliability measures?")
    with st.expander("View Measure criteria"):
        st.write("• Performance metrics - Defined and tracked AI system performance indicators")
        st.write("• Bias testing - Regular testing for unfair bias and discrimination")
        st.write("• Reliability measures - Assessment of system robustness and consistency")
    scores["Measure"] = st.slider(
        "Measure Compliance Score",
        0, 100, 50,
        help="Rate measurement practices: metrics, testing, evaluation",
        key="nist_Measure"
    )
    st.markdown("")
    
    # Manage
    st.markdown("### 📊 Manage")
    st.caption("**What to assess:** Are risk mitigation strategies implemented, incident response ready, and continuous monitoring active?")
    with st.expander("View Manage criteria"):
        st.write("• Risk mitigation - Active strategies to reduce identified risks")
        st.write("• Incident response - Documented procedures for AI system failures or issues")
        st.write("• Continuous monitoring - Ongoing oversight of AI system performance and risks")
    scores["Manage"] = st.slider(
        "Manage Compliance Score",
        0, 100, 50,
        help="Rate risk management: mitigation, response, monitoring",
        key="nist_Manage"
    )
    st.markdown("")
    
    st.markdown("---")
    notes = st.text_area("Additional Notes", placeholder="Any observations, specific gaps, or planned improvements...", height=100)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Submit Assessment", type="primary", use_container_width=True):
            if project_name and assessor:
                assessment = {
                    'name': project_name,
                    'framework': 'NIST AI RMF',
                    'assessor': assessor,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'scores': scores,
                    'score': sum(scores.values()) / len(scores),
                    'notes': notes,
                    'status': 'Completed'
                }
                st.session_state.assessments.append(assessment)
                st.success(f"✅ Assessment saved successfully! Overall score: {assessment['score']:.1f}%")
            else:
                st.error("⚠️ Please fill in project name and assessor name")

# ISO 42001 Assessment Page
elif page == "ISO 42001 Assessment":
    st.markdown('<p class="main-header">ISO 42001 AI Management System</p>', unsafe_allow_html=True)
    
    st.info("📋 Evaluate your AI management system compliance")
    
    # Rating guide
    with st.expander("📖 How to rate compliance (click to expand)"):
        st.markdown("""
        **Rating Scale Guide:**
        - **0-25%**: Minimal or no implementation - No formal processes, ad-hoc approach
        - **26-50%**: Partial implementation - Some controls in place, lacking consistency
        - **51-75%**: Good implementation - Most controls implemented, some documentation gaps
        - **76-100%**: Excellent implementation - Fully documented, implemented, and maintained
        
        **Tips for accurate assessment:**
        - Consider both policy existence AND practical implementation
        - Check if processes are documented and regularly reviewed
        - Assess evidence of effectiveness, not just intent
        - Identify specific gaps for improvement planning
        """)
    
    project_name = st.text_input("AI System Name", placeholder="e.g., Recommendation Engine")
    assessor = st.text_input("Assessor Name", placeholder="Your name")
    
    st.markdown("---")
    st.subheader("Rate each control area (0-100)")
    
    scores = {}
    
    # Planning
    st.markdown("### 📊 Planning")
    st.caption("**What to assess:** Do you have AI-specific policies, clear objectives, and risk assessment procedures?")
    with st.expander("View Planning controls"):
        st.write("• AI policy - Documented organizational AI policy and scope")
        st.write("• Objectives - Clear, measurable AI management objectives")
        st.write("• Risk assessment - Systematic process for identifying AI risks")
    scores["Planning"] = st.slider(
        "Planning Compliance Score",
        0, 100, 50,
        help="Rate planning maturity: policies, objectives, risk planning",
        key="iso_Planning"
    )
    st.markdown("")
    
    # Support
    st.markdown("### 📊 Support")
    st.caption("**What to assess:** Are adequate resources allocated, staff competent, and documentation maintained?")
    with st.expander("View Support controls"):
        st.write("• Resources - Sufficient resources (people, budget, tools) for AI management")
        st.write("• Competence - Staff training and qualification for AI roles")
        st.write("• Documentation - Controlled documents and records for AI systems")
    scores["Support"] = st.slider(
        "Support Compliance Score",
        0, 100, 50,
        help="Rate support infrastructure: resources, competence, documentation",
        key="iso_Support"
    )
    st.markdown("")
    
    # Operation
    st.markdown("### 📊 Operation")
    st.caption("**What to assess:** Are AI operations planned, impacts assessed, and data properly managed?")
    with st.expander("View Operation controls"):
        st.write("• Planning & control - Operational planning for AI system lifecycle")
        st.write("• Impact assessment - Regular assessment of AI system impacts")
        st.write("• Data management - Data quality, privacy, and governance controls")
    scores["Operation"] = st.slider(
        "Operation Compliance Score",
        0, 100, 50,
        help="Rate operational controls: planning, impact assessment, data management",
        key="iso_Operation"
    )
    st.markdown("")
    
    # Performance
    st.markdown("### 📊 Performance")
    st.caption("**What to assess:** Is performance monitored, analyzed, and internally audited?")
    with st.expander("View Performance controls"):
        st.write("• Monitoring - Regular monitoring of AI management system performance")
        st.write("• Analysis - Data analysis and evaluation of effectiveness")
        st.write("• Internal audit - Systematic audits of AI management system")
    scores["Performance"] = st.slider(
        "Performance Compliance Score",
        0, 100, 50,
        help="Rate performance evaluation: monitoring, analysis, auditing",
        key="iso_Performance"
    )
    st.markdown("")
    
    # Improvement
    st.markdown("### 📊 Improvement")
    st.caption("**What to assess:** Are nonconformities addressed, corrective actions taken, and continuous improvement active?")
    with st.expander("View Improvement controls"):
        st.write("• Nonconformity - Process for identifying and managing issues")
        st.write("• Corrective action - Systematic approach to prevent recurrence")
        st.write("• Continual improvement - Ongoing enhancement of AI management system")
    scores["Improvement"] = st.slider(
        "Improvement Compliance Score",
        0, 100, 50,
        help="Rate improvement processes: issue management, corrections, enhancement",
        key="iso_Improvement"
    )
    st.markdown("")
    
    st.markdown("---")
    notes = st.text_area("Additional Notes", placeholder="Document specific gaps, improvement priorities, or compliance observations...", height=100)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💾 Submit Assessment", type="primary", use_container_width=True):
            if project_name and assessor:
                assessment = {
                    'name': project_name,
                    'framework': 'ISO 42001',
                    'assessor': assessor,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'scores': scores,
                    'score': sum(scores.values()) / len(scores),
                    'notes': notes,
                    'status': 'Completed'
                }
                st.session_state.assessments.append(assessment)
                st.success(f"✅ Assessment saved successfully! Overall score: {assessment['score']:.1f}%")
            else:
                st.error("⚠️ Please fill in project name and assessor name")

# Reports Page
elif page == "Reports":
    st.markdown('<p class="main-header">📄 Assessment Reports</p>', unsafe_allow_html=True)
    
    if not st.session_state.assessments:
        st.info("No assessments available yet. Complete an assessment first!")
    else:
        # Filter options
        framework_filter = st.selectbox(
            "Filter by Framework",
            ["All", "NIST AI RMF", "ISO 42001"]
        )
        
        filtered = st.session_state.assessments
        if framework_filter != "All":
            filtered = [a for a in filtered if a['framework'] == framework_filter]
        
        st.markdown("---")
        
        for idx, assessment in enumerate(filtered):
            with st.expander(f"📋 {assessment['name']} - {assessment['framework']} ({assessment['date']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Assessor:** {assessment['assessor']}")
                    st.write(f"**Overall Score:** {assessment['score']:.1f}%")
                    st.write(f"**Status:** {assessment['status']}")
                
                with col2:
                    st.write("**Category Scores:**")
                    for category, score in assessment['scores'].items():
                        st.write(f"• {category}: {score}%")
                
                if assessment.get('notes'):
                    st.markdown("**Notes:**")
                    st.info(assessment['notes'])
                
                # Download button
                json_str = json.dumps(assessment, indent=2)
                st.download_button(
                    "📥 Download Report (JSON)",
                    json_str,
                    file_name=f"{assessment['name']}_{assessment['date']}.json",
                    mime="application/json",
                    key=f"download_{idx}"
                )

# Resources Page
elif page == "Resources":
    st.markdown('<p class="main-header">📚 Resources & Documentation</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["NIST AI RMF", "ISO 42001", "Best Practices"])
    
    with tab1:
        st.subheader("🇺🇸 NIST AI Risk Management Framework")
        st.markdown("""
        The NIST AI RMF provides a structured approach to managing AI risks:
        
        **Core Functions:**
        - **Govern**: Establish AI governance and accountability
        - **Map**: Understand AI system context and risks
        - **Measure**: Assess AI system performance and impacts
        - **Manage**: Allocate resources and monitor risks
        
        **Resources:**
        - [NIST AI RMF Official Site](https://www.nist.gov/itl/ai-risk-management-framework)
        - [AI RMF Playbook](https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook)
        """)
    
    with tab2:
        st.subheader("🌍 ISO/IEC 42001 AI Management System")
        st.markdown("""
        ISO 42001 provides requirements for establishing, implementing, and maintaining an AI management system:
        
        **Key Areas:**
        - Planning and policy development
        - Resource allocation and competence
        - Operational planning and control
        - Performance monitoring
        - Continuous improvement
        
        **Resources:**
        - [ISO 42001 Overview](https://www.iso.org/standard/81230.html)
        - Implementation guides and templates
        """)
    
    with tab3:
        st.subheader("✨ Best Practices")
        st.markdown("""
        **Getting Started:**
        1. Identify your AI systems and use cases
        2. Assess current governance maturity
        3. Choose appropriate framework (NIST, ISO, or both)
        4. Conduct regular assessments
        5. Document findings and track improvements
        
        **Key Principles:**
        - ✅ Transparency and explainability
        - ✅ Fairness and bias mitigation
        - ✅ Privacy and data protection
        - ✅ Security and robustness
        - ✅ Human oversight and accountability
        
        **Free Tools:**
        - This Streamlit app for assessments
        - Google Sheets for tracking
        - GitHub for documentation
        - Markdown for reports
        """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Ethical AI Framework v1.0 | "
    "Built with Streamlit | Free & Open Source</p>",
    unsafe_allow_html=True
)